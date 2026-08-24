#!/usr/bin/env node
/*
 * KingKira demo — page smoke test.
 *
 *   node tools/smoke_test_page.js docs/fleet/index.html [docs/sales/index.html ...]
 *
 * For each page it:
 *   1. Extracts the inline <script> block(s) (ignores <script src=...>).
 *   2. Runs a PARSE check (new vm.Script) — catches syntax errors like a duplicate
 *      `const`, which silently blank a JS-rendered page and are invisible to the
 *      data-model validator (that checks data, not rendered pages).
 *   3. Headless-renders the script against a minimal DOM + a fetch() stub that
 *      reads the repo's local JSON (../data/... -> docs/data/...), and asserts the
 *      render produced DOM content (appendChild calls) with no thrown error.
 *
 * Exit 0 = all pages parse and render non-empty. Exit 1 = a failure (CI-friendly).
 * Pure Node stdlib. Written for the userspace Node install; no npm deps.
 */
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const REPO = path.resolve(__dirname, '..');
const pages = process.argv.slice(2);
if (!pages.length) { console.error('usage: node tools/smoke_test_page.js <page.html> [more.html ...]'); process.exit(2); }

function inlineScripts(html) {
  // grab <script> ... </script> blocks that have NO src attribute
  const out = [];
  const re = /<script(\b[^>]*)>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (!/\bsrc\s*=/i.test(m[1])) out.push(m[2]);
  }
  return out;
}

function makeEl() {
  let mutations = { n: 0 };
  const el = {
    _mut: mutations, _html: '', children: [], style: {}, className: '', onclick: null,
    set innerHTML(v) { this._html = v; if (v) mutations.n++; },
    get innerHTML() { return this._html; },
    appendChild(c) { this.children.push(c); mutations.n++; return c; },
    setAttribute() {}, getAttribute() { return null; },
  };
  return el;
}

function runPage(file) {
  const abs = path.resolve(REPO, file);
  const html = fs.readFileSync(abs, 'utf8');
  const dir = path.dirname(abs);
  const scripts = inlineScripts(html);
  if (!scripts.length) return { file, ok: true, note: 'no inline script (static page)' };

  let totalMut = 0, err = null;

  // shared DOM registry — getElementById returns a stable stub per id
  const registry = {};
  const globalMut = { n: 0 };
  const mkTracked = () => { const e = makeEl(); e._mut = globalMut;
    e.appendChild = function (c) { this.children.push(c); globalMut.n++; return c; };
    Object.defineProperty(e, 'innerHTML', { set(v){ this.__h = v; if (v) globalMut.n++; }, get(){ return this.__h || ''; } });
    return e; };
  const document = {
    getElementById: id => (registry[id] || (registry[id] = mkTracked())),
    createElement: () => mkTracked(),
    querySelector: () => null, querySelectorAll: () => [],
    head: mkTracked(), body: mkTracked(), currentScript: { getAttribute: () => null },
  };
  const fetchStub = url => {
    const rel = String(url).replace(/^\.\.\//, 'docs/').replace(/^\//, '');
    const p = path.resolve(dir, url.startsWith('/') ? path.join(REPO, 'docs', url) : url);
    const candidate = fs.existsSync(p) ? p : path.resolve(REPO, rel);
    const ok = fs.existsSync(candidate);
    return Promise.resolve({ ok, status: ok ? 200 : 404,
      json: () => ok ? Promise.resolve(JSON.parse(fs.readFileSync(candidate, 'utf8'))) : Promise.reject(new Error('404')) });
  };

  const sandbox = { fetch: fetchStub, document, window: {}, Promise, console,
    setTimeout, clearTimeout, Date, Math, Object, Array, JSON, Number, String, Set, Map, parseInt, parseFloat };

  for (const code of scripts) {
    // 1) parse check
    try { new vm.Script(code, { filename: file }); }
    catch (e) { return { file, ok: false, note: 'PARSE ERROR: ' + e.message }; }
    // 2) run
    try { vm.runInNewContext(code, sandbox, { timeout: 5000 }); }
    catch (e) { err = e; }
  }
  return new Promise(res => setTimeout(() => {
    totalMut = globalMut.n;
    if (err) return res({ file, ok: false, note: 'RUNTIME ERROR: ' + err.message });
    if (totalMut === 0) return res({ file, ok: false, note: 'rendered NOTHING (0 DOM mutations) — likely a silent failure' });
    res({ file, ok: true, note: totalMut + ' DOM mutations (render produced content)' });
  }, 400));
}

(async () => {
  let fail = 0;
  for (const f of pages) {
    let r;
    try { r = await runPage(f); } catch (e) { r = { file: f, ok: false, note: 'harness error: ' + e.message }; }
    console.log((r.ok ? 'PASS ' : 'FAIL ') + r.file + ' — ' + r.note);
    if (!r.ok) fail++;
  }
  console.log(`\n${pages.length - fail}/${pages.length} pages passed.`);
  process.exit(fail ? 1 : 0);
})();
