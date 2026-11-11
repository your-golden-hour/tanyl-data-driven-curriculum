"""Build GitHub Pages / Cloudflare Pages assets from the shared application."""
from pathlib import Path
import shutil
import hashlib

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'dist'
out.mkdir(exist_ok=True)
shutil.copytree(ROOT / 'app/static', out / 'static', dirs_exist_ok=True)
(out / 'python').mkdir(exist_ok=True)
for name in ('__init__.py', 'analysis.py', 'data_gen.py', 'browser.py'):
    shutil.copyfile(ROOT / 'app' / name, out / 'python' / name)
shutil.copytree(ROOT / 'data', out / 'data', dirs_exist_ok=True)
html = (ROOT / 'app/templates/index.html').read_text(encoding='utf-8')
for name in ('style.css', 'app.js'):
    digest = hashlib.sha256((ROOT / 'app/static' / name).read_bytes()).hexdigest()[:10]
    html = html.replace("{{ url_for('static', filename='" + name + "') }}", 'static/' + name + '?v=' + digest)
html = html.replace('<main>', '<main><p id="runtime-status" role="status">Подготавливаем аналитику…</p>')
runtime_digest = hashlib.sha256((ROOT / 'app/static/browser-runtime.js').read_bytes()).hexdigest()[:10]
html = html.replace('<script src="static/app.js?', '<script src="static/browser-runtime.js?v=' + runtime_digest + '"></script>\n<script src="static/app.js?')
html = html.replace('/api/template/results.csv', 'data/sample_results.csv').replace('/api/template/curriculum.csv', 'data/sample_curriculum.csv')
html = html.replace('href="data/', 'download href="data/')
(out / 'index.html').write_text(html, encoding='utf-8')
(out / '.nojekyll').touch()
print('Static site built:', out)
