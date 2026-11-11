"""Flask-приложение: REST API + дашборд для методистов."""
from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, render_template, request, send_file

from .analysis import HoursConfig, full_report
from .data_gen import generate

MAX_UPLOAD_MB = 20


class State:
    """Хранилище текущего набора данных (в памяти процесса)."""

    def __init__(self) -> None:
        self.results: pd.DataFrame | None = None
        self.curriculum: pd.DataFrame | None = None
        self.source = "demo"

    def load_demo(self) -> None:
        self.results, self.curriculum = generate()
        self.source = "demo"


def _read_csv(file_storage) -> pd.DataFrame:
    raw = file_storage.read()
    for enc in ("utf-8-sig", "cp1251"):
        try:
            return pd.read_csv(io.StringIO(raw.decode(enc)), sep=None, engine="python")
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    raise ValueError("Не удалось прочитать CSV (ожидается UTF-8 или Windows-1251)")


def _cfg_from_request() -> HoursConfig:
    def num(name, default, cast=float):
        try:
            return cast(request.args.get(name, default))
        except ValueError:
            return default

    return HoursConfig(
        max_change=min(max(num("max_change", 0.35), 0.05), 0.8),
        sensitivity=min(max(num("sensitivity", 1.0), 0.0), 3.0),
        min_hours=max(num("min_hours", 2, int), 1),
    )


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024
    state = State()
    state.load_demo()

    def report():
        return full_report(state.results, state.curriculum, _cfg_from_request())

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        return {"status": "ok", "source": state.source}

    @app.get("/api/report")
    def api_report():
        try:
            rep = report()
        except ValueError as e:
            return jsonify(error=str(e)), 422
        rep["source"] = state.source
        return jsonify(rep)

    @app.post("/api/upload")
    def upload():
        f_res = request.files.get("results")
        f_cur = request.files.get("curriculum")
        if not f_res:
            return jsonify(error="Нужен файл результатов (поле 'results')"), 400
        try:
            res = _read_csv(f_res)
            cur = _read_csv(f_cur) if f_cur else None
            full_report(res, cur)  # проверка до замены данных
        except ValueError as e:
            return jsonify(error=str(e)), 422
        state.results, state.curriculum, state.source = res, cur, "upload"
        return jsonify(ok=True)

    @app.post("/api/demo")
    def demo():
        state.load_demo()
        return jsonify(ok=True)

    @app.get("/api/export.xlsx")
    def export_xlsx():
        try:
            rep = report()
        except ValueError as e:
            return jsonify(error=str(e)), 422
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as xw:
            pd.DataFrame([rep["summary"]]).to_excel(xw, sheet_name="Сводка", index=False)
            pd.DataFrame(rep["topics"]).to_excel(xw, sheet_name="Темы", index=False)
            pd.DataFrame(rep["textbooks"]["overall"]).to_excel(xw, sheet_name="Учебники", index=False)
            tb_topics = pd.DataFrame(rep["textbooks"]["by_topic"]).drop(columns=["means"])
            tb_topics.to_excel(xw, sheet_name="Учебники по темам", index=False)
            pd.DataFrame(rep["hours"]["rows"]).to_excel(xw, sheet_name="Рекомендации по часам", index=False)
        buf.seek(0)
        return send_file(
            buf,
            as_attachment=True,
            download_name="data_driven_curriculum_report.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    @app.get("/api/template/<name>.csv")
    def template(name: str):
        if name == "results":
            df = generate(n_students=3)[0].head(6)
        elif name == "curriculum":
            df = generate(n_students=1)[1]
        else:
            return jsonify(error="unknown template"), 404
        buf = io.BytesIO(df.to_csv(index=False).encode("utf-8-sig"))
        return send_file(buf, as_attachment=True, download_name=f"template_{name}.csv", mimetype="text/csv")

    return app


app = create_app()

