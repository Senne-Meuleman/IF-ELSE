/* =====================================================================
   DECK ENGINE — no dependencies. Keys:
   → / Space / PageDown next   ← / PageUp prev   Home/End   F fullscreen
   N presenter notes window    number + Enter jump   A/R autopilot/reset on demo
   ===================================================================== */
const STATIC = new URLSearchParams(location.search).has('static');
if (STATIC) document.documentElement.classList.add('static');
const stage = document.getElementById('stage');
const slides = [...document.querySelectorAll('.slide')];
let cur = 0, step = 0;

function fit() {
  const s = Math.min(innerWidth / 1920, innerHeight / 1080);
  stage.style.setProperty('--s', s); window.__deckScale = s;
}
addEventListener('resize', fit); fit();

// data-delay / data-stagger → CSS var --d
document.querySelectorAll('[data-delay]').forEach(el => el.style.setProperty('--d', el.dataset.delay + 'ms'));
document.querySelectorAll('[data-stagger]').forEach(p => [...p.children].forEach((c, i) => {
  const base = parseInt(c.dataset.delay || p.dataset.delay || 0);
  c.style.setProperty('--d', base + i * parseInt(p.dataset.stagger) + 'ms');
}));
// data-split → words/chars with --i
document.querySelectorAll('[data-split]').forEach(el => {
  if (el.dataset.delay) el.style.setProperty('--d', el.dataset.delay + 'ms');
  let i = 0;
  el.innerHTML = el.textContent.trim().split(/\s+/).map(w =>
    `<span class="word">${[...w].map(ch => `<span class="char" style="--i:${i++}">${ch}</span>`).join('')}</span>`
  ).join(' ');
});

const maxStep = s => Math.max(0, ...[...s.querySelectorAll('[data-step]')].map(e => +e.dataset.step));
function applySteps() {
  slides[cur].querySelectorAll('[data-step]').forEach(e => e.classList.toggle('shown', +e.dataset.step <= step));
}

// Animated counters: data-count, data-prefix, data-suffix, data-decimals
function runCounters(slide) {
  slide.querySelectorAll('[data-count]').forEach(el => {
    const end = parseFloat(el.dataset.count), dec = +(el.dataset.decimals || 0);
    const fmt = v => (el.dataset.prefix || '') + v.toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + (el.dataset.suffix || '');
    if (STATIC) { el.textContent = fmt(end); return; }
    const t0 = performance.now() + 400, dur = 1800;
    const tick = now => {
      const t = Math.min(1, Math.max(0, (now - t0) / dur)), e = 1 - Math.pow(2, -10 * t);
      el.textContent = fmt(t >= 1 ? end : end * e);
      if (t < 1 && slides[cur] === slide) requestAnimationFrame(tick);
    };
    el.textContent = fmt(0); requestAnimationFrame(tick);
  });
}

function go(n, { toStep = 0 } = {}) {
  n = Math.max(0, Math.min(slides.length - 1, n));
  const changed = n !== cur;
  cur = n;
  slides.forEach((s, i) => { s.classList.toggle('active', i === cur); s.classList.toggle('past', i < cur); });
  step = toStep === 'max' ? maxStep(slides[cur]) : toStep;
  if (STATIC) step = maxStep(slides[cur]);
  applySteps();
  const hue = slides[cur].dataset.hue; if (hue) document.documentElement.style.setProperty('--hue', hue);
  if (changed || !go.ran) runCounters(slides[cur]);
  go.ran = true;
  document.dispatchEvent(new CustomEvent('slidechange', { detail: { index: cur, slide: slides[cur] } }));
  history.replaceState(null, '', location.pathname + location.search + '#' + (cur + 1));
  updateChrome(); updateNotes();
}
function next() { if (step < maxStep(slides[cur])) { step++; applySteps(); updateChrome(); } else go(cur + 1); }
function prev() { if (step > 0) { step--; applySteps(); updateChrome(); } else if (cur > 0) go(cur - 1, { toStep: 'max' }); }
function updateChrome() {
  const m = maxStep(slides[cur]);
  document.getElementById('progress').style.setProperty('--p', (cur + (m ? step / (m + 1) : 0)) / Math.max(1, slides.length - 1));
  document.getElementById('counter').textContent = `${cur + 1} / ${slides.length}`;
}

let jump = '';
function onKey(e) {
  if (e.target.matches?.('input, textarea')) { if (e.key === 'Escape') e.target.blur(); return; }
  const k = e.key;
  if (['ArrowRight', 'ArrowDown', ' ', 'PageDown'].includes(k)) { e.preventDefault(); next(); }
  else if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(k)) { e.preventDefault(); prev(); }
  else if (k === 'Home') go(0); else if (k === 'End') go(slides.length - 1);
  else if (k === 'f' || k === 'F') document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
  else if (k === 'n' || k === 'N') openNotes();
  else if (/^\d$/.test(k)) jump += k;
  else if (k === 'Enter' && jump) { go(parseInt(jump) - 1); jump = ''; }
  else document.dispatchEvent(new CustomEvent('deckkey', { detail: k }));
}
addEventListener('keydown', onKey);
let tx = null;
addEventListener('touchstart', e => tx = e.touches[0].clientX, { passive: true });
addEventListener('touchend', e => { if (tx === null) return; const dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) dx < 0 ? next() : prev(); tx = null; });

// 3D tilt + spotlight for [data-tilt]
let tilted = null;
addEventListener('pointermove', e => {
  const el = e.target.closest?.('[data-tilt]');
  if (tilted && tilted !== el) { tilted.style.transform = ''; tilted = null; }
  if (!el || STATIC) return;
  const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
  el.style.transition = 'transform .2s ease-out';
  el.style.transform = `perspective(1000px) rotateY(${(x - .5) * 14}deg) rotateX(${(.5 - y) * 14}deg) translateZ(10px)`;
  el.style.setProperty('--mx', x * 100 + '%'); el.style.setProperty('--my', y * 100 + '%');
  tilted = el;
});

// Presenter notes window (N) — also forwards keys back to the deck
let nw = null, t0 = null;
function openNotes() {
  nw = window.open('', 'deck-notes', 'width=760,height=560');
  if (!nw) return;
  t0 = t0 || Date.now();
  nw.document.write(`<!doctype html><title>Presenter notes</title><style>body{margin:0;padding:32px;background:#111;color:#eee;font:20px/1.5 system-ui}#t{font:700 44px system-ui;color:#9f8cff}#h{font-size:30px;margin:12px 0}#n{font-size:24px;white-space:pre-wrap}#nx{color:#888;margin-top:28px}</style><div id=t></div><div id=h></div><div id=n></div><div id=nx></div>`);
  nw.document.close();
  nw.document.addEventListener('keydown', onKey);
  updateNotes();
}
const titleOf = s => s ? (s.dataset.title || s.querySelector('h1,h2')?.textContent || '') : '— end —';
function updateNotes() {
  if (!nw || nw.closed) return;
  const d = nw.document;
  d.getElementById('h').textContent = `${cur + 1}/${slides.length} · ${titleOf(slides[cur])}` + (maxStep(slides[cur]) ? `  (step ${step}/${maxStep(slides[cur])})` : '');
  d.getElementById('n').textContent = slides[cur].querySelector('.notes')?.textContent.trim() || '';
  d.getElementById('nx').textContent = 'Next: ' + titleOf(slides[cur + 1]);
}
setInterval(() => {
  if (!nw || nw.closed || !t0) return;
  const s = Math.floor((Date.now() - t0) / 1000);
  nw.document.getElementById('t').textContent = `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
}, 500);
