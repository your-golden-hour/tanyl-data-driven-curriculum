import base64
import io
import json

import pandas as pd


def test_browser_upload_report_export_and_failed_upload():
    from app.browser import BrowserSession
    session = BrowserSession()
    assert json.loads(session.handle({'action': 'report'}))['summary']['students'] == 540
    csv = 'student_id,textbook,topic,score\na,A,T,50\nb,A,T,70\n'
    payload = base64.b64encode(csv.encode()).decode()
    session.handle({'action': 'upload', 'results': payload})
    rep = json.loads(session.handle({'action': 'report'}))
    assert rep['source'] == 'upload' and rep['summary']['students'] == 2
    try:
        session.handle({'action': 'upload', 'results': base64.b64encode(b'x,y\n1,2').decode()})
    except ValueError:
        pass
    assert json.loads(session.handle({'action': 'report'}))['summary']['students'] == 2
    output = json.loads(session.handle({'action': 'export', 'sensitivity': 0}))
    xlsx = base64.b64decode(output['base64'])
    sheet = pd.read_excel(io.BytesIO(xlsx), sheet_name='Рекомендации по часам')
    assert sheet.recommended.tolist() == [5]
    other = BrowserSession()
    assert json.loads(other.handle({'action': 'report'}))['source'] == 'demo'
    session.handle({'action': 'demo'})
    assert json.loads(session.handle({'action': 'report'}))['source'] == 'demo'
