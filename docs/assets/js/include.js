/* ============================================================
   KingKira Group — shared header/footer injector
   Owner: alice (Sales). Used by every page so nav/footer stay in sync.

   HOW TO USE ON YOUR PAGE (Bob /fleet, Cindy /workforce):
   1. In <head>:   <link rel="stylesheet" href="../assets/css/brand.css">
                   (Yanone font link is auto-added by this script.)
   2. First element in <body>:  <div id="site-header"></div>
   3. Last element in <body>:   <div id="site-footer"></div>
   4. Before </body>:
        <script src="../assets/js/include.js" data-active="fleet"></script>
      - data-active = one of: home | sales | fleet | workforce  (highlights the nav tab)
      - The script finds its OWN src to compute the site root, so the SAME
        relative depth rule applies: pages in /docs/<section>/ use "../assets/..".
        The landing page /docs/index.html uses "assets/..".
   ============================================================ */
(function () {
  var script = document.currentScript;
  var src = script.getAttribute('src');            // e.g. "../assets/js/include.js"
  var base = src.replace(/assets\/js\/include\.js.*$/, ''); // -> "../"  or  ""
  var active = (script.getAttribute('data-active') || '').toLowerCase();

  // Ensure the display font is loaded (safe on GitHub Pages; no-op if offline)
  if (!document.querySelector('link[data-kk-font]')) {
    var f = document.createElement('link');
    f.rel = 'stylesheet';
    f.setAttribute('data-kk-font', '1');
    f.href = 'https://fonts.googleapis.com/css2?family=Yanone+Kaffeesatz:wght@400;600;700&family=Inter:wght@400;600;700&display=swap';
    document.head.appendChild(f);
  }

  var NAV = [
    { key: 'home',      label: 'Home',      href: base + 'index.html' },
    { key: 'sales',     label: 'Sales',     href: base + 'sales/' },
    { key: 'fleet',     label: 'Assets',    href: base + 'fleet/' },
    { key: 'workforce', label: 'Workforce', href: base + 'workforce/' }
  ];

  var navHtml = NAV.map(function (n) {
    var cls = (n.key === active) ? ' class="is-active"' : '';
    return '<a href="' + n.href + '"' + cls + '>' + n.label + '</a>';
  }).join('');

  var headerHtml =
    '<header class="kk-header"><div class="kk-header__inner">' +
      '<a class="kk-brand" href="' + base + 'index.html" style="text-decoration:none">' +
        '<span class="kk-brand__mark">K</span>' +
        '<span class="kk-brand__name">King<span>Kira</span></span>' +
      '</a>' +
      '<nav class="kk-nav">' + navHtml + '</nav>' +
    '</div></header>';

  var year = document.documentElement.getAttribute('data-year') || '2026';
  var footerHtml =
    '<footer class="kk-footer"><div class="kk-footer__inner">' +
      '<div class="kk-footer__tag">' +
        '<strong style="color:#fff;font-family:var(--kk-display);font-size:1.3rem">KingKira Group</strong><br>' +
        'Empowering People, Protecting Country, Creating Opportunity.' +
      '</div>' +
      '<div>' +
        '<strong style="color:#fff">Integrated Industrial &amp; Environmental Services</strong><br>' +
        'Level 2, 21 Kintail Rd, Applecross WA 6153 &middot; (08) 9364 0500' +
      '</div>' +
      '<div class="kk-footer__tag">' +
        'KingKira acknowledges the Traditional Custodians of the lands on which we work, ' +
        'and pays respect to Elders past and present.' +
      '</div>' +
    '</div>' +
    '<div class="kk-footer__inner" style="margin-top:18px">' +
      '<small>&copy; ' + year + ' KingKira Group (demo). Synthetic data — built for a ppz agent demo, not an official KingKira site.</small>' +
    '</div></footer>';

  var h = document.getElementById('site-header');
  if (h) h.outerHTML = headerHtml;
  var ft = document.getElementById('site-footer');
  if (ft) ft.outerHTML = footerHtml;
})();
