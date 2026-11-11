import io

import numpy as np
import pandas as pd
import pytest

from app.analysis import (HoursConfig, compare_textbooks, full_report, hard_topics,
                          prepare_results, recommend_hours, topic_stats)
from app.data_gen import generate
from app.web import create_app


@pytest.fixture(scope="module")
def data():
    return generate(n_students=300, seed=7)


def test_prepare_requires_columns():
    with pytest.raises(ValueError):
        prepare_results(pd.DataFrame({"student_id": [1], "score": [5]}))


def test_prepare_normalizes_and_drops_bad_rows():
    df = pd.DataFrame({
        "student_id": ["a", "b", "c"], "textbook": ["X"] * 3, "topic": ["T"] * 3,
        "score": [8, "oops", 5], "max_score": [10, 10, 0],
    })
    out = prepare_results(df)
    assert len(out) == 1 and out["pct"].iloc[0] == 80


def test_hard_topics_flags_known_hard_topic(data):
    res, _ = data
    ht = hard_topics(topic_stats(prepare_results(res)))
    top3 = set(ht.head(3)["topic"])
    assert "Функции и графики" in top3          # самая сложная в генераторе
    assert ht.iloc[-1]["topic"] == "Среднее и медиана"  # самая лёгкая
    assert ht["level"].isin({"critical", "elevated", "normal"}).all()


def test_textbook_comparison_finds_geometry_leader(data):
    res, _ = data
    cmp = compare_textbooks(prepare_results(res))
    geo = [r for r in cmp["by_topic"] if r["section"] == "Геометрия"]
    assert all(r["best"] == "Атамұра" for r in geo)
    assert cmp["ranking_metric"] == "adj_effect"
    effects = [o["adj_effect"] for o in cmp["overall"]]
    assert abs(sum(effects)) < 0.1              # эффекты центрированы


def test_adjustment_removes_cohort_bias():
    """Учебник без реального эффекта, но с сильным контингентом, не должен «выигрывать»."""
    rng = np.random.default_rng(0)
    rows = []
    for tb, shift in (("A", 0), ("B", 15)):     # у B ученики сильнее на 15 баллов
        for i in range(150):
            prior = 55 + shift + rng.normal(0, 8)
            for topic in ("t1", "t2"):
                rows.append({"student_id": f"{tb}{i}", "textbook": tb, "topic": topic,
                             "score": prior + rng.normal(0, 5), "prior_score": prior})
    cmp = compare_textbooks(prepare_results(pd.DataFrame(rows)))
    eff = {o["textbook"]: o["adj_effect"] for o in cmp["overall"]}
    assert abs(eff["A"] - eff["B"]) < 3          # без поправки разрыв был бы ~15


def test_hours_total_preserved_and_bounded(data):
    res, cur = data
    rep = full_report(res, cur, HoursConfig(max_change=0.35))
    h = rep["hours"]
    assert sum(r["recommended"] for r in h["rows"]) == h["total_hours"] == cur["hours"].sum()
    for r in h["rows"]:
        assert r["recommended"] >= 2
        assert abs(r["recommended"] - r["hours"]) <= max(1, round(0.35 * r["hours"]) + 1)
    hardest = max(h["rows"], key=lambda r: r["difficulty"])
    easiest = min(h["rows"], key=lambda r: r["difficulty"])
    assert hardest["delta"] > 0 and easiest["delta"] < 0


def test_hours_without_curriculum_uses_defaults(data):
    res, _ = data
    rep = full_report(res, None)
    assert rep["hours"]["total_hours"] == 5 * rep["summary"]["topics"]


# ------------------------------------------------------------------ API
@pytest.fixture()
def client():
    return create_app().test_client()


def test_api_report_and_index(client):
    assert client.get("/").status_code == 200
    r = client.get("/api/report")
    assert r.status_code == 200 and r.json["summary"]["topics"] == 12


def test_api_upload_roundtrip_and_validation(client, data):
    res, cur = data
    ok = client.post("/api/upload", data={
        "results": (io.BytesIO(res.head(600).to_csv(index=False).encode()), "r.csv"),
        "curriculum": (io.BytesIO(cur.to_csv(index=False).encode()), "c.csv"),
    }, content_type="multipart/form-data")
    assert ok.status_code == 200
    assert client.get("/api/report").json["source"] == "upload"

    bad = client.post("/api/upload", data={
        "results": (io.BytesIO(b"a,b\n1,2\n"), "bad.csv")}, content_type="multipart/form-data")
    assert bad.status_code == 422
    assert client.get("/api/report").json["source"] == "upload"  # старые данные не потеряны


def test_api_export_and_templates(client):
    x = client.get("/api/export.xlsx")
    assert x.status_code == 200 and x.data[:2] == b"PK"
    assert client.get("/api/template/results.csv").status_code == 200
    assert client.get("/api/template/nope.csv").status_code == 404
