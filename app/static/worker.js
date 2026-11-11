/* Python analytics runs off the UI thread and never uploads data. */
let runtime;
async function initialize() {
  postMessage({status: 'Загружаем вычислительные библиотеки. Первый запуск может занять около минуты…'});
  importScripts('https://cdn.jsdelivr.net/pyodide/v0.28.3/full/pyodide.js');
  const py = await loadPyodide();
  await py.loadPackage(['pandas', 'scipy', 'micropip']);
  await py.runPythonAsync('import micropip\nawait micropip.install("openpyxl==3.1.5")');
  py.FS.mkdir('/app');
  for (const name of ['__init__.py', 'analysis.py', 'data_gen.py', 'browser.py']) {
    const response = await fetch('../python/' + name);
    if (!response.ok) throw new Error('Не удалось загрузить аналитический модуль');
    py.FS.writeFile('/app/' + name, await response.text());
  }
  py.runPython('import sys, json\nsys.path.insert(0, "/")\nfrom app.browser import BrowserSession\nbrowser_session = BrowserSession()');
  postMessage({status: 'Готово. Вычисления выполняются в вашем браузере.'});
  return py;
}
let queue = Promise.resolve();
onmessage = ({data}) => {
  queue = queue.then(async () => {
    try {
      runtime ||= initialize();
      const py = await runtime;
      py.globals.set('request_json', JSON.stringify(data.payload));
      const result = py.runPython('browser_session.handle(json.loads(request_json))');
      postMessage({id: data.id, result: JSON.parse(result)});
    } catch (error) {
      postMessage({id: data.id, error: String(error.message || error)});
    }
  });
};
