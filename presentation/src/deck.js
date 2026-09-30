
/* =====================================================================
   HOOK: a wall of identical phones that each come alive on the build step
   ===================================================================== */
(() => {
  const wall = document.querySelector('[data-wall]');
  if (!wall) return;
  const HUES = ['#8B5CF6', '#00AEEF', '#F59E0B', '#14B8A6', '#5B8DEF', '#006A9E'];
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  wall.innerHTML = Array.from({ length: 80 }, () => {
    const c = HUES[Math.floor(rnd() * HUES.length)], h = 22 + Math.round(rnd() * 34);
    const w = () => 35 + Math.round(rnd() * 65) + '%';
    return `<i class="mp${rnd() < .12 ? ' alert' : ''}" style="--c:${c};--h:${h}px;--w1:${w()};--w2:${w()};--w3:${w()};--d:${Math.round(rnd() * 900)}ms"><b></b><s></s><s></s><s></s></i>`;
  }).join('');
})();

/* =====================================================================
   DEMO: real screenshots of the running app (captured from the live engine),
   stepped through by a time-travel control and clickable hotspots.
   Hotspot x/y are fractions of the screen image.
   ===================================================================== */
const PERSONAS = ['Student', 'Young professional', 'Young family', 'Freelancer', 'Retiree'];
const FRAMES = {
  'lotte-2018': { img: 'assets/lotte-2018.jpg', date: '15 Oct 2018', mix: { Student: 100 }, reason: '<b>Runway hero</b>: student-job income and an allowance. €20,56 a day until 1 Nov.' },
  'lotte-2021': { img: 'assets/lotte-2021.jpg', date: '20 Jul 2021', mix: { Student: 62, 'Young professional': 38 }, reason: '<b>First salary</b> arrived: the app <b>suggests</b> a savings tile instead of rearranging hers.' },
  'lotte-2022': { img: 'assets/lotte-2022.jpg', date: '20 Apr 2022', mix: { 'Young professional': 59, Student: 41 }, reason: '<b>Balance hero</b>. A notary payment on 15 Mar 2022 → "New home, new bills".' },
  'lotte-2024': { img: 'assets/lotte-2024.jpg', date: '15 Mar 2024', mix: { 'Young family': 100 }, reason: '<b>Family budget hero</b>: Groeipakket and baby spending. The feed spots a protection gap.' },
  'lotte-2026-02': { img: 'assets/lotte-2026-02.jpg', date: '20 Feb 2026', mix: { 'Young family': 59, Freelancer: 41 }, reason: '<b>First invoice paid</b>: the app suggests Tax reserve as her main tile. She decides.' },
  'lotte-2026': { img: 'assets/lotte-2026.jpg', date: '30 Sep 2026', mix: { Freelancer: 59, 'Young family': 41 }, reason: '<b>Tax-reserve hero</b>: €2.457 to set aside, VAT due in 20 days.' },
  'sara': { img: 'assets/sara.jpg', date: '30 Sep 2026', mix: { Freelancer: 59, 'Young family': 41 }, reason: '<b>Five cards, ranked</b>: the car-insurance renewal in 12 days comes first.',
    hots: [{ x: .78, y: .448, to: 'sara-why' }, { x: .645, y: .62, to: 'sara-kate' }] },
  'sara-why': { img: 'assets/sara-why.jpg', date: '30 Sep 2026', mix: { Freelancer: 59, 'Young family': 41 }, reason: '<b>Why am I seeing this?</b> The payments behind the card, plus stage, impact and confidence.',
    hots: [{ x: .645, y: .62, to: 'sara-kate' }] },
  'sara-kate': { img: 'assets/sara-kate.jpg', date: '30 Sep 2026', mix: { Freelancer: 59, 'Young family': 41 }, reason: '<b>Ask Kate</b>: grounded in the same card. Rules by default; an optional LLM only rephrases.',
    hots: [{ x: .91, y: .11, to: 'sara' }] },
  'jan': { img: 'assets/jan.jpg', date: '30 Sep 2026', mix: { Retiree: 100 }, reason: '<b>Large, calm, high contrast</b>, chosen for him. First card: €1.250 to a payee he never paid before.',
    hots: [{ x: .5, y: .8, to: 'jan-kate2' }] },
  'jan-kate2': { img: 'assets/jan-kate2.jpg', date: '30 Sep 2026', mix: { Retiree: 100 }, reason: '<b>"That wasn\'t me"</b>: Kate gives the Card Stop number straight away.',
    hots: [{ x: .91, y: .1, to: 'jan' }] },
};
const TIMELINE = ['lotte-2018', 'lotte-2021', 'lotte-2022', 'lotte-2024', 'lotte-2026-02', 'lotte-2026'];
const TICKS = ['2018', '2021', '2022', '2024', 'Feb 26', 'Sep 26'];
const HOME = { lotte: null, sara: 'sara', jan: 'jan' };

const Demo = (() => {
  const root = document.getElementById('app');
  if (!root) return null;
  const $ = sel => root.querySelector(sel);
  const cursor = root.querySelector('.fake-cursor'), tt = $('[data-tt]'), hots = $('[data-hots]');
  let imgA = $('[data-a]'), imgB = $('[data-b]');
  const S = () => window.__deckScale || 1;
  let cust = 'lotte', ti = 0, frame = null, run = 0, touring = false, pos = { x: 700, y: 760 };

  tt.insertAdjacentHTML('beforeend', TICKS.map((y, i) => `<button class="yr" data-yr="${i}" style="left:${i / (TICKS.length - 1) * 100}%">${y}</button>`).join(''));
  $('[data-mix]').innerHTML = PERSONAS.map(p => `<div class="mixrow" data-p="${p}"><span>${p}</span><div class="bar"><i></i></div><b>0%</b></div>`).join('');
  Object.values(FRAMES).forEach(f => { const im = new Image(); im.src = f.img; });   // preload

  function show(name) {
    const F = FRAMES[name]; if (!F || name === frame) return;
    frame = name;
    if (!imgA.getAttribute('src') || STATIC) imgA.src = F.img;
    else { imgB.src = F.img; imgB.classList.remove('out'); imgA.classList.add('out'); [imgA, imgB] = [imgB, imgA]; }
    $('[data-badge]').textContent = F.date;
    root.querySelectorAll('[data-cust]').forEach(b => b.classList.toggle('on', b.dataset.cust === cust));
    tt.classList.toggle('off', cust !== 'lotte');
    const x = cust === 'lotte' ? ti / (TICKS.length - 1) * 100 : 100;
    tt.style.setProperty('--x', x + '%');
    root.querySelectorAll('.yr').forEach((b, i) => b.classList.toggle('on', cust === 'lotte' && i === ti));
    root.querySelectorAll('.mixrow').forEach(r => {
      const w = F.mix[r.dataset.p] || 0;
      r.querySelector('i').style.width = w + '%'; r.querySelector('b').textContent = w + '%'; r.classList.toggle('zero', !w);
    });
    $('[data-main]').innerHTML = F.reason;
    // hotspots positioned over the screen image (inside the device frame)
    const dev = root.querySelector('.screenbox .dev'), w = dev.offsetWidth, pad = w * .032, iw = w - 2 * pad, ih = dev.offsetHeight - 2 * pad;
    hots.innerHTML = (F.hots || []).map((h, i) => `<button class="hot on" data-hot="${h.to}" data-i="${i}" aria-label="Open" style="left:${pad + h.x * iw}px;top:${pad + h.y * ih}px"></button>`).join('');
  }
  const setYear = i => { cust = 'lotte'; ti = i; show(TIMELINE[i]); };
  const setCust = c => { cust = c; show(c === 'lotte' ? TIMELINE[ti] : HOME[c]); };

  root.addEventListener('click', e => {
    const t = e.target.closest('[data-cust],[data-yr],[data-hot]');
    if (!t) return;
    t.blur();
    if (t.dataset.cust) setCust(t.dataset.cust);
    else if (t.dataset.yr) setYear(+t.dataset.yr);
    else if (t.dataset.hot) show(t.dataset.hot);
  });

  // ---- Autopilot: a fake cursor performs the happy path ----
  const wait = ms => { const id = run; return new Promise((res, rej) => setTimeout(() => id === run ? res() : rej('abort'), ms)); };
  async function moveTo(sel, dur = 700, dy = 0) {
    const el = typeof sel === 'string' ? $(sel) : sel;
    const f = root.getBoundingClientRect(), r = el.getBoundingClientRect(), s = S();
    const to = { x: (r.left - f.left + r.width / 2) / s - 6, y: (r.top - f.top + r.height / 2) / s - 4 + dy };
    await cursor.animate([{ transform: `translate(${pos.x}px,${pos.y}px)` }, { transform: `translate(${to.x}px,${to.y}px)` }],
      { duration: dur, easing: 'cubic-bezier(.65,0,.35,1)', fill: 'forwards' }).finished;
    pos = to; await wait(0); return el;
  }
  function ripple() {
    const rp = document.createElement('div'); rp.className = 'ripple';
    Object.assign(rp.style, { left: pos.x + 6 + 'px', top: pos.y + 4 + 'px' }); root.appendChild(rp); setTimeout(() => rp.remove(), 700);
  }
  async function click(sel) {
    const el = await moveTo(sel);
    cursor.classList.add('press'); ripple();
    await wait(140); cursor.classList.remove('press'); el.click(); await wait(200);
  }
  const caps = [...document.querySelectorAll('#demoSteps li')];
  const setCap = i => caps.forEach((li, j) => { li.classList.toggle('on', j === i); li.classList.toggle('done', j < i); });
  const yr = i => root.querySelector(`[data-yr="${i}"]`);

  async function tour() {                  // ← the happy path, ≈ 20 s
    setCap(0); await wait(400);
    await moveTo(yr(0), 700, -24); cursor.classList.add('press');         // grab the time-travel thumb
    for (const i of [1, 2, 3]) { await moveTo(yr(i), 550, -24); setYear(i); await wait(850); }
    setCap(1);
    for (const i of [4, 5]) { await moveTo(yr(i), 550, -24); setYear(i); await wait(1050); }
    cursor.classList.remove('press');
    setCap(2); await click('[data-cust="sara"]'); await wait(1000);
    await click('[data-hot="sara-why"]'); await wait(1500);
    setCap(3); await click('[data-hot="sara-kate"]'); await wait(1500);
    setCap(4); await click('[data-cust="jan"]'); await wait(1100);
    await click('[data-hot="jan-kate2"]'); await wait(1500);
    caps[4].classList.add('done');
  }
  async function autopilot() {
    if (touring) return reset();
    reset(); touring = true; root.classList.add('touring'); cursor.classList.add('show');
    try { await tour(); await wait(1200); } catch (e) { if (e !== 'abort') console.error(e); }
    touring = false; root.classList.remove('touring'); cursor.classList.remove('show', 'press');
  }
  function reset() { run++; touring = false; root.classList.remove('touring'); cursor.classList.remove('show', 'press'); setCap(-1); cust = 'lotte'; ti = 0; frame = null; show(TIMELINE[0]); }

  document.querySelector('[data-autopilot]')?.addEventListener('click', e => { e.currentTarget.blur(); autopilot(); });
  document.querySelector('[data-reset]')?.addEventListener('click', e => { e.currentTarget.blur(); reset(); });
  document.addEventListener('deckkey', e => {
    if (!slides[cur].hasAttribute('data-demo')) return;
    if (e.detail === 'a' || e.detail === 'A') autopilot();
    if (e.detail === 'r' || e.detail === 'R') reset();
  });
  document.addEventListener('slidechange', e => {
    if (!e.detail.slide.hasAttribute('data-demo') && touring) reset();
    if (e.detail.slide.hasAttribute('data-demo')) { const F = FRAMES[frame]; frame = null; show(Object.keys(FRAMES).find(k => FRAMES[k] === F)); }   // re-place hotspots once visible
  });
  show(TIMELINE[0]);
  // ?tour auto-starts the autopilot when the demo slide is opened (kiosk loops, headless tests)
  if (new URLSearchParams(location.search).has('tour'))
    document.addEventListener('slidechange', e => { if (e.detail.slide.hasAttribute('data-demo')) setTimeout(autopilot, 1200); });
  return { reset, autopilot };
})();

// Boot: honour #N in the URL (1-based)
go.ran = false;
go(Math.max(0, (parseInt(location.hash.slice(1)) || 1) - 1));
