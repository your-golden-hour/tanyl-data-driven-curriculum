(() => {
  const worker = new Worker('static/worker.js');
  let serial = 0;
  const pending = new Map();
  worker.onmessage = ({data}) => {
    if (data.status) { document.getElementById('runtime-status').textContent = data.status; return; }
    const task = pending.get(data.id);
    if (!task) return;
    clearTimeout(task.timer);
    pending.delete(data.id);
    if (data.error) task.reject(new Error(data.error)); else task.resolve(data.result);
  };
  worker.onerror = () => {
    for (const task of pending.values()) { clearTimeout(task.timer); task.reject(new Error('Не удалось запустить аналитику. Проверьте интернет и обновите страницу.')); }
    pending.clear();
  };
  function call(payload) {
    return new Promise((resolve, reject) => {
      const id = ++serial;
      const timer = setTimeout(() => { pending.delete(id); reject(new Error('Загрузка занимает слишком долго. Проверьте интернет и обновите страницу.')); }, 180000);
      pending.set(id, {resolve, reject, timer});
      worker.postMessage({id, payload});
    });
  }
  async function encodeFile(file) {
    if (!file || !file.size) return null;
    if (file.size > 20 * 1024 * 1024) throw new Error('Максимальный размер CSV — 20 МБ');
    const bytes = new Uint8Array(await file.arrayBuffer());
    let str = '';
    for (let i = 0; i < bytes.length; i += 8192) str += String.fromCharCode(...bytes.subarray(i, i + 8192));
    return btoa(str);
  }
  const nativeFetch = window.fetch.bind(window);
  window.fetch = async (url, options = {}) => {
    if (typeof url !== 'string' || !url.startsWith('/api/')) return nativeFetch(url, options);
    try {
      const parsed = new URL(url, location.origin);
      const action = parsed.pathname.split('/').pop();
      const payload = {action, ...Object.fromEntries(parsed.searchParams)};
      if (action === 'upload') {
        payload.results = await encodeFile(options.body.get('results'));
        payload.curriculum = await encodeFile(options.body.get('curriculum'));
      }
      return Response.json(await call(payload));
    } catch (error) { return Response.json({error: error.message}, {status: 422}); }
  };
  document.querySelector('[data-i18n="export"]').addEventListener('click', async (event) => {
    event.preventDefault();
    const errorBox = document.getElementById('error');
    try {
      const output = await call({action: 'export', max_change: document.getElementById('max_change').value, sensitivity: document.getElementById('sensitivity').value});
      const bytes = Uint8Array.from(atob(output.base64), c => c.charCodeAt(0));
      const url = URL.createObjectURL(new Blob([bytes], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}));
      const link = Object.assign(document.createElement('a'), {href: url, download: 'Tanyl_curriculum_report.xlsx'});
      link.click(); setTimeout(() => URL.revokeObjectURL(url), 10000);
    } catch (error) { errorBox.hidden = false; errorBox.textContent = error.message; }
  });
})();
