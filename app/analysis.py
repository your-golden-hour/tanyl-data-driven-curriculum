"""Аналитическое ядро платформы.

Четыре задачи кейса:
  1. topic_stats        — анализ результатов по темам
  2. hard_topics        — выявление сложных разделов
  3. compare_textbooks  — сравнение эффективности учебников
  4. recommend_hours    — рекомендации по распределению часов
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
import pandas as pd
from scipy import stats

REQUIRED_RESULT_COLS = {"student_id", "textbook", "topic", "score"}
MASTERY_THRESHOLD = 60.0  # % — порог освоения темы
MIN_N = 30  # минимум наблюдений для уверенного вывода


# ---------------------------------------------------------------- подготовка
def prepare_results(df: pd.DataFrame) -> pd.DataFrame:
    """Валидация и нормализация сырых результатов тестов."""
    missing = REQUIRED_RESULT_COLS - set(df.columns)
    if missing:
        raise ValueError(f"В файле результатов не хватает колонок: {sorted(missing)}")
    out = df.copy()
    if "max_score" not in out:
        out["max_score"] = 100.0
    if "section" not in out:
        out["section"] = "Без раздела"
    out['section'] = out['section'].fillna('Без раздела').replace(r'^\s*$', 'Без раздела', regex=True)
    out["score"] = pd.to_numeric(out["score"], errors="coerce")
    out["max_score"] = pd.to_numeric(out["max_score"], errors="coerce")
    out = out.dropna(subset=["score", "max_score", "topic", "textbook"])
    out = out[out["max_score"] > 0]
    out["pct"] = (out["score"] / out["max_score"] * 100).clip(0, 100)
    if "prior_score" in out:
        out["prior_score"] = pd.to_numeric(out["prior_score"], errors="coerce")
    if out.empty:
        raise ValueError("После очистки не осталось корректных строк")
    return out


def prepare_curriculum(cur: pd.DataFrame | None, results: pd.DataFrame) -> pd.DataFrame:
    """Если учебный план не загружен — берём темы из результатов (по 5 ч на тему)."""
    if cur is None or cur.empty:
        topics = results[["section", "topic"]].drop_duplicates().reset_index(drop=True)
        topics["hours"] = 5
        return topics
    missing = {"topic", "hours"} - set(cur.columns)
    if missing:
        raise ValueError(f"В учебном плане не хватает колонок: {sorted(missing)}")
    out = cur.copy()
    if "section" not in out:
        out["section"] = "Без раздела"
    out["hours"] = pd.to_numeric(out["hours"], errors="coerce")
    if (out['topic'].isna().any() or out['topic'].duplicated().any()
            or not np.isfinite(out['hours']).all()
            or (out['hours'] <= 0).any() or (out['hours'] % 1 != 0).any()):
        raise ValueError('Темы плана должны быть уникальны; часы — положительные целые числа')
    return out.reset_index(drop=True)


# ------------------------------------------------------------ 1. по темам
def topic_stats(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby(["section", "topic"])["pct"]
    t = g.agg(n="count", mean="mean", median="median", std="std").reset_index()
    t["mastery_rate"] = (
        df.assign(ok=df["pct"] >= MASTERY_THRESHOLD)
        .groupby(["section", "topic"])["ok"].mean().values * 100
    )
    sem = t["std"].fillna(0) / np.sqrt(t["n"].clip(lower=1))
    t["ci_low"] = t["mean"] - 1.96 * sem
    t["ci_high"] = t["mean"] + 1.96 * sem
    return t.round(2)


# --------------------------------------------------- 2. сложные разделы
def hard_topics(ts: pd.DataFrame) -> pd.DataFrame:
    """Индекс сложности 0–100 и уровень: критический / повышенный / норма.

    difficulty = 0.6·(100 − средний балл) + 0.4·(100 − доля освоивших)
    Уровень задаётся относительно распределения по всем темам (z-score),
    а также абсолютным порогом по доле освоения.
    """
    t = ts.copy()
    t["difficulty"] = 0.6 * (100 - t["mean"]) + 0.4 * (100 - t["mastery_rate"])
    sd = t["difficulty"].std(ddof=0) or 1.0
    t["z"] = (t["difficulty"] - t["difficulty"].mean()) / sd

    def level(r):
        if r["z"] >= 1.0 or r["mastery_rate"] < 50:
            return "critical"
        if r["z"] >= 0.4 or r["mastery_rate"] < 65:
            return "elevated"
        return "normal"

    t["level"] = t.apply(level, axis=1)
    return t.sort_values("difficulty", ascending=False).round(2).reset_index(drop=True)


# --------------------------------------------------- 3. учебники
def _cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return float("nan")
    pooled = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    return float((a.mean() - b.mean()) / pooled) if pooled else float("nan")


def _adjusted_effects(df: pd.DataFrame) -> dict[str, dict]:
    """Эффект учебника с поправкой на исходный уровень учеников (prior_score).

    OLS на уровне ученика: mean_pct ~ учебник + prior_score.
    Без поправки лучший результат может объясняться «сильным контингентом»,
    а не учебником.
    """
    if "prior_score" not in df or df["prior_score"].isna().all():
        return {}
    s = (
        df.groupby("student_id")
        .agg(y=("pct", "mean"), prior=("prior_score", "first"), tb=("textbook", "first"))
        .dropna()
    )
    books = sorted(s["tb"].unique())
    if len(books) < 2 or len(s) < 20:
        return {}
    X = np.column_stack(
        [np.ones(len(s)), s["prior"].values]
        + [(s["tb"] == b).astype(float).values for b in books[1:]]
    )
    y = s["y"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = max(len(y) - X.shape[1], 1)
    cov = (resid @ resid / dof) * np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    # коэффициенты учебников: эталон = 0, остальные — столбцы 2..; контраст
    # «учебник минus среднее по всем учебникам» даёт центрированный эффект и его p-value
    K = len(books)
    book_idx = [None] + list(range(2, 2 + len(books) - 1))  # индекс в beta (None = эталон)
    out = {}
    for k, b in enumerate(books):
        c = np.zeros(X.shape[1])
        for j, idx in enumerate(book_idx):
            if idx is not None:
                c[idx] -= 1 / K
        if book_idx[k] is not None:
            c[book_idx[k]] += 1
        eff = float(c @ beta)
        se_c = float(np.sqrt(max(c @ cov @ c, 1e-12)))
        p = 2 * (1 - stats.t.cdf(abs(eff / se_c), dof))
        out[b] = {"adj_effect": round(eff, 2), "p": round(float(p), 4)}
    return out


def compare_textbooks(df: pd.DataFrame) -> dict:
    books = sorted(df["textbook"].unique())

    overall = (
        df.groupby("textbook")
        .agg(
            students=("student_id", "nunique"),
            mean=("pct", "mean"),
            std=("pct", "std"),
        )
        .reset_index()
    )
    overall["mastery_rate"] = (
        df.assign(ok=df["pct"] >= MASTERY_THRESHOLD).groupby("textbook")["ok"].mean().values * 100
    )
    adj = _adjusted_effects(df)
    overall["adj_effect"] = overall["textbook"].map(lambda b: adj.get(b, {}).get("adj_effect"))
    overall["adj_p"] = overall["textbook"].map(lambda b: adj.get(b, {}).get("p"))

    # межшкольная ANOVA на уровне ученика
    per_student = df.groupby(["student_id", "textbook"])["pct"].mean().reset_index()
    groups = [g["pct"].values for _, g in per_student.groupby("textbook")]
    anova_p = float(stats.f_oneway(*groups).pvalue) if len(groups) > 1 else None

    # по темам: лучший учебник, разрыв и значимость
    by_topic = []
    for (section, topic), g in df.groupby(["section", "topic"]):
        means = g.groupby("textbook")["pct"].mean()
        best, worst = means.idxmax(), means.idxmin()
        a = g.loc[g["textbook"] == best, "pct"].values
        b = g.loc[g["textbook"] == worst, "pct"].values
        pval = float(stats.ttest_ind(a, b, equal_var=False).pvalue) if len(a) > 1 and len(b) > 1 else None
        by_topic.append(
            {
                "section": section,
                "topic": topic,
                "best": best,
                "worst": worst,
                "gap": round(float(means.max() - means.min()), 2),
                "cohens_d": round(_cohens_d(a, b), 2),
                "p": None if pval is None else round(pval, 4),
                "significant": bool(pval is not None and pval < 0.01),
                "means": {k: round(float(v), 2) for k, v in means.items()},
            }
        )

    matrix = (
        df.groupby(["section", "textbook"])["pct"].mean().unstack().round(2).reset_index()
    )
    ranking_key = "adj_effect" if overall["adj_effect"].notna().any() else "mean"
    overall = overall.sort_values(ranking_key, ascending=False).round(2)

    return {
        "overall": overall.to_dict("records"),
        "by_topic": sorted(by_topic, key=lambda r: -r["gap"]),
        "section_matrix": matrix.to_dict("records"),
        "anova_p": None if anova_p is None else round(anova_p, 6),
        "ranking_metric": ranking_key,
        "books": books,
    }


# --------------------------------------------------- 4. часы
@dataclass
class HoursConfig:
    max_change: float = 0.35   # не более ±35 % к текущим часам по теме
    sensitivity: float = 1.0   # сила реакции на сложность
    min_hours: int = 2


def recommend_hours(ht: pd.DataFrame, cur: pd.DataFrame, cfg: HoursConfig | None = None) -> dict:
    """Перераспределение часов при неизменной общей нагрузке.

    1. Потребность ∝ текущие_часы · (1 + k · относительное_отклонение_сложности)
    2. Ограничиваем изменение по теме ±max_change.
    3. Нормируем к исходному итогу, округляем методом наибольшего остатка.
    """
    cfg = cfg or HoursConfig()
    if ht['topic'].duplicated().any():
        raise ValueError('Используйте уникальные названия тем во всех разделах')
    if set(ht['topic']) != set(cur['topic']):
        raise ValueError('Список тем учебного плана должен совпадать с темами результатов')
    d = ht.merge(cur[["topic", "hours"]], on="topic", how="inner").reset_index(drop=True)
    if d.empty:
        raise ValueError("Темы из результатов не совпадают с темами учебного плана")
    total = int(round(d["hours"].sum()))
    if total < len(d) * cfg.min_hours:
        raise ValueError('Недостаточно часов для заданного минимума на каждую тему')
    mean_diff = d["difficulty"].mean() or 1.0

    dev = (d["difficulty"] - mean_diff) / mean_diff
    raw = d["hours"] * (1 + cfg.sensitivity * dev)
    raw = raw.clip(d["hours"] * (1 - cfg.max_change), d["hours"] * (1 + cfg.max_change))
    raw = raw.clip(lower=cfg.min_hours)
    scaled = raw / raw.sum() * total

    floor = np.floor(scaled).astype(int)
    lower = np.maximum(np.ceil(d['hours'] * (1 - cfg.max_change) - 1e-9).astype(int), cfg.min_hours)
    upper = np.floor(d['hours'] * (1 + cfg.max_change) + 1e-9).astype(int)
    if (lower > upper).any() or lower.sum() > total or upper.sum() < total:
        raise ValueError('Ограничения часов несовместимы с общей нагрузкой')
    floor = np.clip(floor, lower, upper)
    diff = total - int(floor.sum())
    i = 0
    while diff != 0 and i < 10_000:
        step = 1 if diff > 0 else -1
        eligible = floor < upper if step > 0 else floor > lower
        if not eligible.any():
            break
        priority = (scaled - floor) * step
        idx = priority[eligible].idxmax()
        floor[idx] += step
        diff -= step
        i += 1

    if diff:
        raise ValueError('Не удалось распределить часы в заданных границах')

    d["recommended"] = floor.values
    d["delta"] = d["recommended"] - d["hours"].round().astype(int)

    def reason(r):
        if r["delta"] > 0:
            return (f"Освоение {r['mastery_rate']:.0f}%, средний балл {r['mean']:.0f}: "
                    f"тема сложнее среднего — добавить часы на отработку.")
        if r["delta"] < 0:
            return (f"Освоение {r['mastery_rate']:.0f}%, средний балл {r['mean']:.0f}: "
                    f"тема усваивается легко — часть времени можно перенести.")
        return "Нагрузка соответствует результатам — без изменений."

    d["reason"] = d.apply(reason, axis=1)
    d["confidence"] = np.where(d["n"] >= MIN_N, "высокая", "низкая (мало данных)")
    cols = ["section", "topic", "hours", "recommended", "delta", "difficulty",
            "mean", "mastery_rate", "n", "level", "confidence", "reason"]
    d = d[cols].sort_values("delta", ascending=False)
    return {
        "total_hours": total,
        "rows": d.round(2).to_dict("records"),
        "moved": int(d.loc[d["delta"] > 0, "delta"].sum()),
    }


# --------------------------------------------------- сводка
def _finite_json(value):
    if isinstance(value, dict):
        return {k: _finite_json(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_finite_json(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def full_report(results: pd.DataFrame, curriculum: pd.DataFrame | None = None,
                cfg: HoursConfig | None = None) -> dict:
    df = prepare_results(results)
    cur = prepare_curriculum(curriculum, df)
    ts = topic_stats(df)
    ht = hard_topics(ts)
    return _finite_json({
        "summary": {
            "students": int(df["student_id"].nunique()),
            "records": int(len(df)),
            "topics": int(df["topic"].nunique()),
            "textbooks": int(df["textbook"].nunique()),
            "mean": round(float(df["pct"].mean()), 2),
            "mastery_rate": round(float((df["pct"] >= MASTERY_THRESHOLD).mean() * 100), 2),
            "critical": int((ht["level"] == "critical").sum()),
        },
        "topics": ht.to_dict("records"),
        "textbooks": compare_textbooks(df),
        "hours": recommend_hours(ht, cur, cfg),
    })
