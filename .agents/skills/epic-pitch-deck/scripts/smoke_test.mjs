// Smoke-test a deck in real (headless) Chrome via the DevTools protocol. Node 22+, no npm deps.
//
//   node smoke_test.mjs path/to/index.html [--tour-seconds=20]
//
// 1. Visits every slide (?static#N) and reports elements that overflow the 1920×1080 stage
//    or overlap the slide's padding edge, plus any JS errors.
// 2. Opens the demo slide with ?tour and logs demo state once per second so you can confirm
//    the autopilot reaches its final step. Edit PROBE below if your demo markup differs.
import { spawn } from 'node:child_process';
import { existsSync, readFileSync, mkdtempSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { tmpdir } from 'node:os';

const file = process.argv[2];
if (!file) { console.log('usage: node smoke_test.mjs deck.html [--tour-seconds=20]'); process.exit(1); }
const tourSeconds = +(process.argv.find(a => a.startsWith('--tour-seconds='))?.split('=')[1] || 20);
const base = pathToFileURL(resolve(file)).href;
const html = readFileSync(file, 'utf8');
const slideTags = [...html.matchAll(/<section[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>/g)].map(m => m[0]);
const demoIndex = slideTags.findIndex(t => t.includes('data-demo')) + 1;

const browser = [process.env.CHROME_PATH,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome', '/usr/bin/chromium'].find(p => p && existsSync(p));
if (!browser) { console.log('No Chrome/Edge found; set CHROME_PATH'); process.exit(1); }

const port = 9300 + Math.floor(Math.random() * 500);
const proc = spawn(browser, ['--headless=new', `--remote-debugging-port=${port}`, '--window-size=1920,1080',
  `--user-data-dir=${mkdtempSync(tmpdir() + '/deck-smoke-')}`, 'about:blank']);
const sleep = ms => new Promise(r => setTimeout(r, ms));
let targets;
for (let i = 0; i < 60 && !targets; i++) { try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); } catch { await sleep(250); } }
const ws = new WebSocket(targets.find(t => t.type === 'page').webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);
let id = 0; const pending = {}; let errors = [];
ws.onmessage = m => {
  const d = JSON.parse(m.data);
  if (d.id && pending[d.id]) { pending[d.id](d.result); delete pending[d.id]; }
  if (d.method === 'Runtime.exceptionThrown') errors.push(d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text);
  if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') errors.push(d.params.args.map(a => a.value ?? a.description).join(' '));
};
const send = (method, params = {}) => new Promise(r => { pending[++id] = r; ws.send(JSON.stringify({ id, method, params })); });
const evaluate = async expr => (await send('Runtime.evaluate', { expression: expr, returnByValue: true })).result?.value;
await send('Runtime.enable'); await send('Page.enable');
// hash-only changes don't reload a page, so hop through about:blank between slides
const open = async url => { await send('Page.navigate', { url: 'about:blank' }); await sleep(100); await send('Page.navigate', { url }); await sleep(900); };

// ---- 1. layout check per slide ----
const LAYOUT = `(() => {
  const slide = document.querySelector('.slide.active'), s = window.__deckScale || 1;
  const st = document.getElementById('stage').getBoundingClientRect(), out = [];
  slide.querySelectorAll('h1,h2,h3,p,.card,.stat,.chip,.browser,img,svg,li,.btn').forEach(el => {
    if (el.closest('.notes, .browser .shop-vp')) return;
    // union of the box and its actual content (text can spill past a block's box)
    const box = el.getBoundingClientRect(); if (!box.width) return;
    const isText = /^(H1|H2|H3|P|LI)$/.test(el.tagName) || el.classList.contains('chip');
    const rg = document.createRange(); rg.selectNodeContents(el); const c = isText ? rg.getBoundingClientRect() : { width: 0 };
    const r = c.width ? { left: Math.min(box.left, c.left), top: Math.min(box.top, c.top), right: Math.max(box.right, c.right), bottom: Math.max(box.bottom, c.bottom) } : box;
    const L = (r.left - st.left) / s, T = (r.top - st.top) / s, R = (r.right - st.left) / s, B = (r.bottom - st.top) / s;
    const tag = el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : '');
    const txt = (el.textContent || '').trim().slice(0, 30);
    if (L < -1 || T < -1 || R > 1921 || B > 1081) out.push('OFF-STAGE ' + tag + ' "' + txt + '" [' + [L, T, R, B].map(Math.round) + ']');
    else if (L < 40 || T < 30 || R > 1880 || B > 1050) out.push('near edge ' + tag + ' "' + txt + '" [' + [L, T, R, B].map(Math.round) + ']');
    if (el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflow !== 'visible') out.push('clipped ' + tag + ' "' + txt + '"');
  });
  return out;
})()`;
let problems = 0;
for (let i = 1; i <= slideTags.length; i++) {
  errors = [];
  await open(`${base}?static#${i}`);
  const issues = await evaluate(LAYOUT) || [];
  const title = (slideTags[i - 1].match(/data-title="([^"]*)"/) || [])[1] || '';
  const bad = issues.length + errors.length;
  problems += bad;
  console.log(`${bad ? '✗' : '✓'} slide ${i} ${title}`);
  issues.forEach(x => console.log('    ' + x));
  errors.forEach(x => console.log('    JS ERROR ' + x));
}

// ---- 2. demo autopilot run ----
if (demoIndex > 0) {
  const PROBE = `JSON.stringify({
    step: [...document.querySelectorAll('#demoSteps li')].map(l => l.classList.contains('on') ? '●' : l.classList.contains('done') ? '✓' : '·').join(''),
    badge: document.querySelector('[data-badge]')?.textContent,
    view: (document.querySelector('[data-main]')?.innerText || '').split(String.fromCharCode(10))[0].slice(0, 40) })`;
  errors = [];
  console.log(`\nDemo (slide ${demoIndex}) autopilot, ${tourSeconds}s:`);
  await open(`${base}?tour#${demoIndex}`);
  let last = '';
  for (let t = 1; t <= tourSeconds; t++) {
    const v = await evaluate(PROBE);
    if (v !== last) console.log(`  ${String(t).padStart(2)}s ${v}`);
    last = v; await sleep(1000);
  }
  errors.forEach(x => console.log('  JS ERROR ' + x));
  problems += errors.length;
}
console.log(problems ? `\n${problems} issue(s) found.` : '\nAll clear.');
ws.close(); proc.kill();
process.exit(problems ? 1 : 0);
