"""Генератор реалистичных демо-данных.

Создаёт два набора:
  * results    — результаты тестов учеников по темам (long format)
  * curriculum — темы программы с текущим числом часов

Структура данных совпадает с форматом CSV, который принимает платформа,
поэтому демо-данные можно заменить реальными без изменения кода.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# (раздел, тема, текущие часы, "истинная" сложность 0..1)
TOPICS = [
    ("Арифметика", "Обыкновенные дроби", 8, 0.45),
    ("Арифметика", "Десятичные дроби", 7, 0.35),
    ("Арифметика", "Проценты", 6, 0.50),
    ("Алгебра", "Линейные уравнения", 9, 0.40),
    ("Алгебра", "Системы уравнений", 8, 0.70),
    ("Алгебра", "Степени и многочлены", 8, 0.65),
    ("Алгебра", "Функции и графики", 7, 0.75),
    ("Геометрия", "Углы и треугольники", 8, 0.45),
    ("Геометрия", "Площади фигур", 6, 0.55),
    ("Геометрия", "Теорема Пифагора", 5, 0.60),
    ("Статистика", "Среднее и медиана", 4, 0.25),
    ("Статистика", "Вероятность", 5, 0.68),
]

TEXTBOOKS = ["Атамұра", "Мектеп", "Просвещение-KZ"]

# Сдвиг эффективности учебника по разделам (в баллах из 100).
# Намеренно разный: ни один учебник не лучший во всём — как в жизни.
TEXTBOOK_EFFECT = {
    "Атамұра": {"Арифметика": 2, "Алгебра": -3, "Геометрия": 6, "Статистика": 0},
    "Мектеп": {"Арифметика": 0, "Алгебра": 4, "Геометрия": -2, "Статистика": 3},
    "Просвещение-KZ": {"Арифметика": -3, "Алгебра": -1, "Геометрия": -1, "Статистика": -5},
}


def generate(n_students: int = 540, seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)

    curriculum = pd.DataFrame(
        [{"section": s, "topic": t, "hours": h} for s, t, h, _ in TOPICS]
    )

    schools = [f"Школа №{i}" for i in range(1, 7)]
    rows = []
    for sid in range(1, n_students + 1):
        school = schools[(sid - 1) % len(schools)]
        class_id = f"7{'АБВ'[(sid // 7) % 3]}-{school[-1]}"
        # учебник закреплён за школой (как на практике), а не за учеником
        textbook = TEXTBOOKS[schools.index(school) % len(TEXTBOOKS)]
        ability = rng.normal(0, 1)
        prior = float(np.clip(62 + 12 * ability + rng.normal(0, 5), 15, 100))
        for section, topic, _, diff in TOPICS:
            base = 90 - 34 * diff + 8 * ability
            base += TEXTBOOK_EFFECT[textbook][section]
            score = float(np.clip(base + rng.normal(0, 11), 0, 100))
            rows.append(
                {
                    "student_id": f"S{sid:04d}",
                    "school": school,
                    "class_id": class_id,
                    "textbook": textbook,
                    "section": section,
                    "topic": topic,
                    "score": round(score, 1),
                    "max_score": 100,
                    "prior_score": round(prior, 1),
                }
            )
    return pd.DataFrame(rows), curriculum


if __name__ == "__main__":
    res, cur = generate()
    res.to_csv("data/sample_results.csv", index=False)
    cur.to_csv("data/sample_curriculum.csv", index=False)
    print(f"results: {len(res)} rows, curriculum: {len(cur)} topics")
