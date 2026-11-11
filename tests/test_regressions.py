import io
import json

import pandas as pd
import pytest

from app.analysis import HoursConfig, full_report
from app.data_gen import generate
from app.web import create_app


def test_sparse_report_is_standard_json():
    df = pd.DataFrame([dict(student_id='one', textbook='A', topic='T', score=50)])
    json.dumps(full_report(df), allow_nan=False)


def test_infeasible_minimum_is_rejected():
    res, cur = generate(30)
    with pytest.raises(ValueError):
        full_report(res, cur, HoursConfig(min_hours=100))


@pytest.mark.parametrize('hours', [-1, 0, float('inf'), 2.5])
def test_invalid_curriculum_hours_are_rejected(hours):
    res, cur = generate(30)
    cur['hours'] = float(hours)
    with pytest.raises(ValueError):
        full_report(res, cur)


def test_duplicate_topics_are_rejected():
    res, cur = generate(30)
    cur = pd.concat([cur, cur.iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError):
        full_report(res, cur)


def test_unmeasured_curriculum_is_not_silently_discarded():
    res, cur = generate(30)
    cur.loc[0, 'topic'] = 'No measurements'
    with pytest.raises(ValueError):
        full_report(res, cur)


def test_export_uses_requested_settings():
    client = create_app().test_client()
    response = client.get('/api/export.xlsx?sensitivity=0')
    assert response.status_code == 200
    sheet = pd.read_excel(io.BytesIO(response.data), sheet_name='Рекомендации по часам')
    assert (sheet.hours == sheet.recommended).all()


def test_integer_hours_respect_small_percentage_limit():
    df = pd.DataFrame([dict(student_id='a', textbook='A', topic='Hard', score=0),
                       dict(student_id='b', textbook='A', topic='Easy', score=100)])
    report = full_report(df, cfg=HoursConfig(max_change=.1))
    assert [row['recommended'] for row in report['hours']['rows']] == [5, 5]


def test_blank_optional_sections_are_kept():
    df = pd.DataFrame([dict(student_id='a', textbook='A', topic='T', score=50, section=None)])
    report = full_report(df)
    assert report['topics'][0]['n'] == 1
