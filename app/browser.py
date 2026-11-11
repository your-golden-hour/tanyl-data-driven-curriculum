"""Browser-only adapter. Shares the original Python analytics; no network I/O."""
import base64
import io
import json

import pandas as pd

from .analysis import HoursConfig, full_report
from .data_gen import generate


def read_csv(encoded):
    raw = base64.b64decode(encoded)
    if len(raw) > 20 * 1024 * 1024:
        raise ValueError('Максимальный размер CSV — 20 МБ')
    for encoding in ('utf-8-sig', 'cp1251'):
        try:
            return pd.read_csv(io.StringIO(raw.decode(encoding)), sep=None, engine='python')
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    raise ValueError('Не удалось прочитать CSV')


class BrowserSession:
    def __init__(self):
        self.results, self.curriculum = generate()
        self.source = 'demo'

    def handle(self, request):
        action = request.get('action', 'report')
        cfg = HoursConfig(max_change=float(request.get('max_change', .35)),
                          sensitivity=float(request.get('sensitivity', 1)))
        if action == 'demo':
            self.results, self.curriculum = generate()
            self.source = 'demo'
            return json.dumps({'ok': True})
        if action == 'upload':
            results = read_csv(request['results'])
            curriculum = read_csv(request['curriculum']) if request.get('curriculum') else None
            full_report(results, curriculum)
            self.results, self.curriculum, self.source = results, curriculum, 'upload'
            return json.dumps({'ok': True})
        rep = full_report(self.results, self.curriculum, cfg)
        rep['source'] = self.source
        if action == 'export':
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                sheets = {'Сводка': [rep['summary']], 'Темы': rep['topics'],
                          'Учебники': rep['textbooks']['overall'],
                          'Учебники по темам': rep['textbooks']['by_topic'],
                          'Рекомендации по часам': rep['hours']['rows']}
                for name, rows in sheets.items():
                    frame = pd.DataFrame(rows).drop(columns=['means'], errors='ignore')
                    frame.to_excel(writer, sheet_name=name, index=False)
                # Uploaded labels are text, never Excel formulae.
                for sheet in writer.book:
                    for row in sheet:
                        for cell in row:
                            if cell.data_type == 'f':
                                cell.data_type = 's'
            return json.dumps({'base64': base64.b64encode(buf.getvalue()).decode()})
        return json.dumps(rep, ensure_ascii=False, allow_nan=False)
