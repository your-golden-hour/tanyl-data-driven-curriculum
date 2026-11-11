const I18N = {
  ru: {
    intro_title: "Решения для учебной программы на основе данных", intro_description: "Посмотрите, какие темы даются ученикам труднее, сравните результаты по учебникам и проверьте, как перераспределить часы без увеличения общей нагрузки.", intro_note: "На старте показаны синтетические данные. Результаты сравнения не доказывают причинный эффект; итоговое решение принимает методист.",
    tab_topics: "Темы и сложность", tab_books: "Учебники", tab_hours: "Рекомендации по часам", tab_data: "Данные",
    export: "Экспорт в Excel",
    h_topics: "Результаты по темам", hint_topics: "Индекс сложности 0–100: чем выше, тем труднее тема. Уровень считается относительно всех тем программы.",
    h_books: "Эффективность учебников", h_sections: "Средний балл по разделам и учебникам",
    h_best: "Лучший учебник по каждой теме", hint_best: "«Значимо» — различие подтверждено статистически (t-тест Уэлча, p < 0,01).",
    h_hours: "Рекомендуемое распределение часов", c_change: "Макс. изменение по теме:", c_sens: "Чувствительность к сложности:",
    h_upload: "Загрузка данных", hint_upload: "CSV с результатами тестов (обязательно) и учебным планом (необязательно). Без загрузки используются демо-данные.",
    f_results: "Результаты тестов", f_cur: "Учебный план", upload: "Загрузить", demo: "Вернуть демо-данные",
    tpl_res: "Шаблон результатов", tpl_cur: "Шаблон учебного плана",
    k_students: "Учеников", k_records: "Результатов", k_mean: "Средний балл", k_mastery: "Доля освоивших", k_crit: "Критических тем",
    th_topic: "Тема", th_section: "Раздел", th_mean: "Ср. балл", th_mastery: "Освоили, %", th_diff: "Сложность", th_level: "Уровень", th_n: "N",
    th_book: "Учебник", th_students: "Учеников", th_adj: "Эффект с поправкой", th_p: "p",
    th_best: "Лучший", th_worst: "Худший", th_gap: "Разрыв", th_d: "d Коэна", th_sig: "Значимо",
    th_cur: "Сейчас, ч", th_rec: "Рекомендуем, ч", th_delta: "Δ", th_why: "Обоснование", th_conf: "Надёжность",
    critical: "критическая", elevated: "повышенная", normal: "норма", yes: "да", no: "нет",
    books_hint_adj: "Рейтинг по эффекту с поправкой на исходный уровень учеников (регрессия). Эффект — в баллах относительно среднего по учебникам.",
    books_hint_raw: "Рейтинг по среднему баллу (исходный уровень учеников не передан, поправка не применена).",
    anova: "Различие между учебниками на уровне учеников (ANOVA): p =", chart_mean: "Средний балл", chart_mastery: "Доля освоивших, %",
    cur: "Сейчас", rec: "Рекомендуем", src_demo: "Источник: демо-данные.", src_up: "Источник: загруженные файлы.",
    moved: "Перераспределено часов:", of: "из",
  },
  kk: {
    intro_title: "Оқу бағдарламасына арналған деректерге негізделген шешімдер", intro_description: "Оқушыларға қиын тақырыптарды анықтаңыз, оқулықтар бойынша нәтижелерді салыстырыңыз және жалпы жүктемені арттырмай сағаттарды қайта бөлуді тексеріңіз.", intro_note: "Бастапқыда синтетикалық деректер көрсетіледі. Салыстыру себеп-салдар байланысын дәлелдемейді; соңғы шешімді әдіскер қабылдайды.",
    tab_topics: "Тақырыптар және қиындық", tab_books: "Оқулықтар", tab_hours: "Сағат бойынша ұсыныстар", tab_data: "Деректер",
    export: "Excel-ге экспорт",
    h_topics: "Тақырыптар бойынша нәтижелер", hint_topics: "Қиындық индексі 0–100: жоғары болған сайын тақырып қиынырақ. Деңгей бағдарламаның барлық тақырыбына қатысты есептеледі.",
    h_books: "Оқулықтардың тиімділігі", h_sections: "Бөлімдер мен оқулықтар бойынша орташа балл",
    h_best: "Әр тақырып бойынша үздік оқулық", hint_best: "«Маңызды» — айырмашылық статистикалық расталған (Уэлч t-тесті, p < 0,01).",
    h_hours: "Сағаттарды бөлудің ұсынылатын жоспары", c_change: "Тақырып бойынша ең көп өзгеріс:", c_sens: "Қиындыққа сезімталдық:",
    h_upload: "Деректерді жүктеу", hint_upload: "Тест нәтижелері бар CSV (міндетті) және оқу жоспары (міндетті емес). Жүктемесеңіз, демо-деректер қолданылады.",
    f_results: "Тест нәтижелері", f_cur: "Оқу жоспары", upload: "Жүктеу", demo: "Демо-деректерді қайтару",
    tpl_res: "Нәтижелер үлгісі", tpl_cur: "Оқу жоспарының үлгісі",
    k_students: "Оқушылар", k_records: "Нәтижелер", k_mean: "Орташа балл", k_mastery: "Меңгерген үлес", k_crit: "Критикалық тақырыптар",
    th_topic: "Тақырып", th_section: "Бөлім", th_mean: "Орт. балл", th_mastery: "Меңгерген, %", th_diff: "Қиындық", th_level: "Деңгей", th_n: "N",
    th_book: "Оқулық", th_students: "Оқушылар", th_adj: "Түзетілген әсер", th_p: "p",
    th_best: "Үздік", th_worst: "Әлсіз", th_gap: "Айырма", th_d: "Коэн d", th_sig: "Маңызды",
    th_cur: "Қазір, сағ", th_rec: "Ұсыныс, сағ", th_delta: "Δ", th_why: "Негіздеме", th_conf: "Сенімділік",
    critical: "критикалық", elevated: "жоғары", normal: "норма", yes: "иә", no: "жоқ",
    books_hint_adj: "Рейтинг оқушылардың бастапқы деңгейіне түзетілген әсер бойынша (регрессия). Әсер — оқулықтардың орташасына қатысты баллмен.",
    books_hint_raw: "Рейтинг орташа балл бойынша (бастапқы деңгей берілмеген, түзету қолданылмады).",
    anova: "Оқулықтар арасындағы айырма, оқушы деңгейінде (ANOVA): p =", chart_mean: "Орташа балл", chart_mastery: "Меңгерген үлес, %",
    cur: "Қазір", rec: "Ұсыныс", src_demo: "Дереккөз: демо-деректер.", src_up: "Дереккөз: жүктелген файлдар.",
    moved: "Қайта бөлінген сағат:", of: "бастап",
  },
};

let lang = localStorage.getItem("lang") || "ru";
let report = null;
const charts = {};
const t = (k) => I18N[lang][k] ?? k;
const esc = (v) => String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const $ = (id) => document.getElementById(id);
const COLORS = ["#2f5fd0", "#e39b1e", "#2e9b6a", "#9b59b6", "#d64545"];
const LEVEL_COLOR = { critical: "#d64545", elevated: "#e39b1e", normal: "#2e9b6a" };

function fmtP(p) { return p == null ? "—" : p < 0.001 ? "<0.001" : p.toFixed(3); }
function sign(n) { return n > 0 ? `+${n}` : `${n}`; }

function applyI18n() {
  document.documentElement.lang = lang === "kk" ? "kk" : "ru";
  document.querySelectorAll("[data-i18n]").forEach((el) => (el.textContent = t(el.dataset.i18n)));
  $("lang").textContent = lang === "ru" ? "ҚАЗ" : "РУС";
}

function setChart(id, config) {
  Chart.defaults.color = "#425571";
  Chart.defaults.borderColor = "#e2eaf5";
  Chart.defaults.font.family = 'system-ui, -apple-system, "Segoe UI", sans-serif';
  if (charts[id]) charts[id].destroy();
  charts[id] = new Chart($(id), config);
}

async function load() {
  const q = new URLSearchParams({ max_change: $("max_change").value, sensitivity: $("sensitivity").value });
  const r = await fetch("/api/report?" + q);
  const data = await r.json();
  const err = $("error");
  if (!r.ok) { err.hidden = false; err.textContent = data.error; return; }
  err.hidden = true;
  report = data;
  render();
}

function render() {
  if (!report) return;
  applyI18n();
  const s = report.summary;
  $("kpis").innerHTML = [
    [t("k_students"), s.students], [t("k_records"), s.records],
    [t("k_mean"), s.mean + "%"], [t("k_mastery"), s.mastery_rate + "%"], [t("k_crit"), s.critical],
  ].map(([l, v]) => `<div class="kpi"><b>${esc(v)}</b><span>${esc(l)}</span></div>`).join("");
  $("source").textContent = report.source === "demo" ? t("src_demo") : t("src_up");
  renderTopics(); renderBooks(); renderHours();
}

function renderTopics() {
  const rows = report.topics;
  setChart("chTopics", {
    type: "bar",
    data: {
      labels: rows.map((r) => r.topic),
      datasets: [
        { label: t("chart_mean"), data: rows.map((r) => r.mean), backgroundColor: rows.map((r) => LEVEL_COLOR[r.level]) },
        { label: t("chart_mastery"), data: rows.map((r) => r.mastery_rate), backgroundColor: "#9aa7ba55", borderColor: "#9aa7ba", borderWidth: 1 },
      ],
    },
    options: { indexAxis: "y", maintainAspectRatio: false, scales: { x: { min: 0, max: 100 } } },
  });
  $("tblTopics").innerHTML =
    `<tr><th>${t("th_topic")}</th><th>${t("th_section")}</th><th>${t("th_mean")}</th><th>${t("th_mastery")}</th><th>${t("th_diff")}</th><th>${t("th_level")}</th><th>${t("th_n")}</th></tr>` +
    rows.map((r) => `<tr><td>${esc(r.topic)}</td><td>${esc(r.section)}</td><td>${r.mean}</td><td>${r.mastery_rate}</td><td>${r.difficulty}</td>
      <td><span class="badge ${esc(r.level)}">${t(r.level)}</span></td><td>${r.n}</td></tr>`).join("");
}

function renderBooks() {
  const tb = report.textbooks;
  const adj = tb.ranking_metric === "adj_effect";
  $("booksHint").textContent = (adj ? t("books_hint_adj") : t("books_hint_raw")) + (tb.anova_p != null ? ` ${t("anova")} ${fmtP(tb.anova_p)}.` : "");
  $("tblBooks").innerHTML =
    `<tr><th>#</th><th>${t("th_book")}</th><th>${t("th_students")}</th><th>${t("th_mean")}</th><th>${t("th_mastery")}</th>${adj ? `<th>${t("th_adj")}</th><th>${t("th_p")}</th>` : ""}</tr>` +
    tb.overall.map((o, i) => `<tr><td>${i + 1}</td><td><b>${esc(o.textbook)}</b></td><td>${o.students}</td><td>${o.mean}</td><td>${o.mastery_rate}</td>${
      adj ? `<td class="${o.adj_effect >= 0 ? "pos" : "neg"}">${sign(o.adj_effect)}</td><td>${fmtP(o.adj_p)}</td>` : ""}</tr>`).join("");

  const sections = tb.section_matrix.map((r) => r.section);
  setChart("chSections", {
    type: "bar",
    data: {
      labels: sections,
      datasets: tb.books.map((b, i) => ({ label: b, backgroundColor: COLORS[i % COLORS.length], data: tb.section_matrix.map((r) => r[b]) })),
    },
    options: { maintainAspectRatio: false, scales: { y: { min: 40, max: 100 } } },
  });

  $("tblBest").innerHTML =
    `<tr><th>${t("th_topic")}</th><th>${t("th_best")}</th><th>${t("th_worst")}</th><th>${t("th_gap")}</th><th>${t("th_d")}</th><th>${t("th_p")}</th><th>${t("th_sig")}</th></tr>` +
    tb.by_topic.map((r) => `<tr><td>${esc(r.topic)}</td><td class="pos">${esc(r.best)}</td><td>${esc(r.worst)}</td><td>${r.gap}</td><td>${r.cohens_d}</td><td>${fmtP(r.p)}</td><td>${r.significant ? t("yes") : t("no")}</td></tr>`).join("");
}

function renderHours() {
  const h = report.hours;
  const rows = [...h.rows].sort((a, b) => b.difficulty - a.difficulty);
  setChart("chHours", {
    type: "bar",
    data: {
      labels: rows.map((r) => r.topic),
      datasets: [
        { label: t("cur"), data: rows.map((r) => r.hours), backgroundColor: "#9aa7ba" },
        { label: t("rec"), data: rows.map((r) => r.recommended), backgroundColor: "#2f5fd0" },
      ],
    },
    options: { maintainAspectRatio: false, plugins: { subtitle: { display: true, text: `${t("moved")} ${h.moved} ${t("of")} ${h.total_hours}` } } },
  });
  $("tblHours").innerHTML =
    `<tr><th>${t("th_topic")}</th><th>${t("th_cur")}</th><th>${t("th_rec")}</th><th>${t("th_delta")}</th><th>${t("th_conf")}</th><th>${t("th_why")}</th></tr>` +
    h.rows.map((r) => `<tr><td>${esc(r.topic)}</td><td>${r.hours}</td><td><b>${r.recommended}</b></td>
      <td class="${r.delta > 0 ? "pos" : r.delta < 0 ? "neg" : ""}">${r.delta ? sign(r.delta) : "0"}</td><td>${esc(r.confidence)}</td><td class="wrap">${esc(r.reason)}</td></tr>`).join("");
}

// ---- события
document.querySelectorAll(".tab").forEach((b) => b.addEventListener("click", () => {
  document.querySelectorAll(".tab").forEach((x) => x.classList.toggle("active", x === b));
  document.querySelectorAll(".panel").forEach((p) => (p.hidden = p.id !== "tab-" + b.dataset.tab));
  const showKpi = b.dataset.tab !== "data"; $("kpis").hidden = !showKpi;
}));
$("lang").addEventListener("click", () => { lang = lang === "ru" ? "kk" : "ru"; localStorage.setItem("lang", lang); render(); });
["max_change", "sensitivity"].forEach((id) => $(id).addEventListener("change", () => {
  $("vChange").textContent = Math.round($("max_change").value * 100) + "%";
  $("vSens").textContent = Number($("sensitivity").value).toFixed(1);
  load();
}));
$("upForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const r = await fetch("/api/upload", { method: "POST", body: new FormData(e.target) });
  const d = await r.json();
  if (!r.ok) { $("error").hidden = false; $("error").textContent = d.error; return; }
  await load();
});
$("demoBtn").addEventListener("click", async () => { await fetch("/api/demo", { method: "POST" }); await load(); });

applyI18n();
load();
