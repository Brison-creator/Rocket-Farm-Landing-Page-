/* ------------------------------------------------------------------
   1. Site map — generated from the lot table so the two can't drift.
      The table is the single source of truth for every rate.
------------------------------------------------------------------ */
(function () {
  var layer = document.getElementById('lot-layer');
  var rows  = [].slice.call(document.querySelectorAll('#lot-rows tr'));
  var svg   = document.getElementById('sitemap');
  var tip   = document.getElementById('tip');
  if (!layer || !svg || !rows.length) return;

  var NS = 'http://www.w3.org/2000/svg';
  /* Two bands of pads, between the three interior roads. */
  var BANDS = { A: { y0: 148, y1: 272 }, B: { y0: 330, y1: 452 } };
  var X0 = 152, X1 = 872, SKEW = 26;

  var byRow = {};
  rows.forEach(function (tr) {
    var r = tr.getAttribute('data-row');
    (byRow[r] = byRow[r] || []).push(tr);
  });

  var shapes = {};

  Object.keys(byRow).forEach(function (rowKey) {
    var band = BANDS[rowKey];
    if (!band) return;
    var list = byRow[rowKey];
    var step = (X1 - X0) / list.length;
    var padW = step * 0.6;

    list.forEach(function (tr, i) {
      var x    = X0 + i * step;
      var lot  = tr.getAttribute('data-lot');
      var g    = document.createElementNS(NS, 'g');
      g.setAttribute('class', 'lot');
      g.setAttribute('data-lot', lot);
      g.setAttribute('data-amps', tr.getAttribute('data-amps'));
      g.setAttribute('data-term', tr.getAttribute('data-term'));
      g.setAttribute('tabindex', '0');
      g.setAttribute('role', 'button');

      var svc = tr.getAttribute('data-amps') === '50' ? '50/30/20 amp' : '30/20 amp';
      var per = tr.getAttribute('data-term') === 'nightly' ? 'per night' : 'per month';
      g.setAttribute('aria-label',
        'Space ' + lot + ', ' + svc + ', $' + tr.getAttribute('data-price') + ' ' + per);

      var pad = document.createElementNS(NS, 'path');
      pad.setAttribute('class', 'pad');
      pad.setAttribute('d',
        'M' + x + ' ' + band.y1 +
        'L' + (x + SKEW) + ' ' + band.y0 +
        'L' + (x + SKEW + padW) + ' ' + band.y0 +
        'L' + (x + padW) + ' ' + band.y1 + 'Z');
      g.appendChild(pad);

      var num = document.createElementNS(NS, 'text');
      num.setAttribute('class', 'num');
      num.setAttribute('x', String(x + SKEW / 2 + padW / 2));
      num.setAttribute('y', String((band.y0 + band.y1) / 2 + 5));
      num.textContent = lot;
      g.appendChild(num);

      layer.appendChild(g);
      shapes[lot] = g;
    });
  });

  /* --- hover / focus: tooltip + paired table row highlight --- */
  function lotData(lot) {
    var tr = document.querySelector('#lot-rows tr[data-lot="' + lot + '"]');
    if (!tr) return null;
    var nightly = tr.getAttribute('data-term') === 'nightly';
    return {
      tr: tr,
      lot: lot,
      svc: tr.getAttribute('data-amps') === '50' ? '50 / 30 / 20 amp' : '30 / 20 amp',
      price: '$' + tr.getAttribute('data-price') + (nightly ? ' / night' : ' / month')
    };
  }

  var current = null;

  function show(lot) {
    var d = lotData(lot);
    if (!d) return;
    var g = shapes[lot];
    if (current && current !== lot) hide(current);
    current = lot;
    d.tr.classList.add('active');
    g.classList.add('active');

    tip.querySelector('.tip-lot').textContent = 'Space ' + d.lot;
    tip.querySelector('.tip-svc').textContent = d.svc;
    tip.querySelector('.tip-price').textContent = d.price;

    /* Position the tip over the pad, in the frame's coordinates. Flip it below
       the pad when there is no room above, and keep it inside the frame, which
       clips its overflow. */
    var frame = tip.parentElement.getBoundingClientRect();
    var box   = g.getBoundingClientRect();
    tip.classList.add('show');

    var tipW = tip.offsetWidth, tipH = tip.offsetHeight;
    var padTop = box.top - frame.top, padBottom = box.bottom - frame.top;

    /* Prefer above the pad; drop below when it would not fit, then clamp so the
       frame (which hides overflow) never crops it. */
    var top = padTop - tipH - 10;
    if (top < 8) top = padBottom + 10;
    top = Math.min(top, frame.height - tipH - 8);
    tip.style.top = Math.max(8, top) + 'px';

    var cx  = box.left - frame.left + box.width / 2;
    var min = tipW / 2 + 8, max = frame.width - tipW / 2 - 8;
    tip.style.left = (max < min ? frame.width / 2 : Math.max(min, Math.min(max, cx))) + 'px';
  }

  /* Only the lot that is currently showing may close the tooltip — otherwise a
     late mouseleave from the pad we just left closes the one we just opened. */
  function hide(lot) {
    if (shapes[lot]) shapes[lot].classList.remove('active');
    var d = lotData(lot);
    if (d) d.tr.classList.remove('active');
    if (current === lot) {
      tip.classList.remove('show');
      current = null;
    }
  }

  Object.keys(shapes).forEach(function (lot) {
    var g = shapes[lot];
    g.addEventListener('mouseenter', function () { show(lot); });
    g.addEventListener('mouseleave', function () { hide(lot); });
    g.addEventListener('focus', function () { show(lot); });
    g.addEventListener('blur', function () { hide(lot); });
    g.addEventListener('click', function () { show(lot); });
    g.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(lot); }
    });
  });

  /* Hovering a table row lights up its pad on the map. */
  rows.forEach(function (tr) {
    var lot = tr.getAttribute('data-lot');
    tr.addEventListener('mouseenter', function () {
      if (shapes[lot]) shapes[lot].classList.add('active');
    });
    tr.addEventListener('mouseleave', function () {
      if (shapes[lot]) shapes[lot].classList.remove('active');
    });
  });

  /* --- filter chips --- */
  var chips = [].slice.call(document.querySelectorAll('.chip[data-filter]'));
  function matches(tr, f) {
    if (f === 'all') return true;
    if (f === 'nightly') return tr.getAttribute('data-term') === 'nightly';
    return tr.getAttribute('data-amps') === f && tr.getAttribute('data-term') === 'monthly';
  }
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.getAttribute('data-filter');
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
      if (current) hide(current);
      rows.forEach(function (tr) {
        var ok = matches(tr, f);
        tr.style.display = ok ? '' : 'none';
        var g = shapes[tr.getAttribute('data-lot')];
        if (g) g.classList.toggle('dim', !ok);
      });
    });
  });
})();

/* ------------------------------------------------------------------
   2. Scroll reveal
------------------------------------------------------------------ */
(function () {
  var items = [].slice.call(document.querySelectorAll('.reveal'));
  if (!items.length) return;
  if (!('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
  items.forEach(function (el) { io.observe(el); });
})();

/* ------------------------------------------------------------------
   3. Footer year
------------------------------------------------------------------ */
var yr = document.getElementById('year'); if (yr) yr.textContent = new Date().getFullYear();

/* ------------------------------------------------------------------
   4. Waitlist form — no-backend fallback.
      If you set a real `action` on the form, DELETE this block.
------------------------------------------------------------------ */
(function () {
  var form = document.getElementById('waitlist-form');
  var msg  = document.getElementById('form-msg');
  if (!form || !msg) return;

  /* Look fields up by id: form.name would return the form's own name
     attribute, not the "name" input. */
  var $ = function (id) { return document.getElementById(id); };

  /* Where reservations land. Assembled at runtime so scrapers reading the
     raw HTML don't harvest it. Swap back to 'stay@therocketfarm.com' once
     that forwarder exists at Namecheap. */
  var TO = ['admin', 'nohm.app'].join('@');
  var PAY_LINK = '';                     // e.g. 'https://buy.stripe.com/xxxx' — leave empty until it exists
  if (PAY_LINK) {
    var pr = document.getElementById('pay-row'), pl = document.getElementById('pay-link');
    if (pr && pl) { pl.href = PAY_LINK; pr.hidden = false; }
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var name  = $('name').value.trim();
    var phone = $('phone').value.trim();
    var email = $('email').value.trim();
    var validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
    var validPhone = phone.replace(/\D/g, '').length >= 10;

    var bad = !name ? $('name') : !validPhone ? $('phone') : !validEmail ? $('email') : null;
    if (bad) {
      msg.className = 'form-msg show';
      msg.style.borderColor = 'rgba(232,98,60,.5)';
      msg.style.background  = 'rgba(232,98,60,.12)';
      msg.textContent = 'Please add your name, a phone number and a valid email address.';
      bad.focus();
      return;
    }

    var body =
      'Name: '    + name + '\n' +
      'Company: ' + ($('company').value.trim() || '(not given)') + '\n' +
      'Reason: '  + $('reason').value + '\n' +
      'Phone: '   + phone + '\n' +
      'Email: '   + email + '\n';

    var href = 'mailto:' + TO +
      '?subject=' + encodeURIComponent('Rocket Farm reservation — ' + name) +
      '&body='    + encodeURIComponent(body);

    msg.className = 'form-msg show';
    msg.style.borderColor = '';
    msg.style.background  = '';
    msg.innerHTML = 'Thanks, ' + name.replace(/[<>&]/g, '') +
      ' — your email app should be opening with the details filled in. We reply with deposit instructions to hold your space. ' +
      'If it didn\'t, send them to <a href="mailto:' + TO + '">' + TO + '</a>.';

    window.location.href = href;
  });
})();

/* ------------------------------------------------------------------
   5. Mobile menu
------------------------------------------------------------------ */
(function () {
  var hdr = document.getElementById('site-header');
  var btn = hdr && hdr.querySelector('.nav-toggle');
  if (!hdr || !btn) return;
  function set(open) {
    hdr.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  btn.addEventListener('click', function () { set(!hdr.classList.contains('open')); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
  document.addEventListener('click', function (e) { if (hdr.classList.contains('open') && !hdr.contains(e.target)) set(false); });
})();

/* ------------------------------------------------------------------
   6. Section index on the rules page
------------------------------------------------------------------ */
(function () {
  var links = [].slice.call(document.querySelectorAll('.toc ol a'));
  if (!links.length || !('IntersectionObserver' in window)) return;
  var secs = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  var cur = -1;
  function set(i) {
    if (i === cur) return; cur = i;
    links.forEach(function (a, k) { a.classList.toggle('cur', k === i); });
    var a = links[i]; if (a && a.scrollIntoView && window.innerWidth < 980) {
      a.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
    }
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) set(secs.indexOf(e.target)); });
  }, { rootMargin: '-40% 0px -55% 0px' });
  secs.forEach(function (s) { if (s) io.observe(s); });
})();

/* ------------------------------------------------------------------
   7. Day / night sky: re-check the Central-time clock each minute unless
      the visitor has chosen one with the header toggle.
------------------------------------------------------------------ */
(function () {
  var root = document.documentElement;
  function hourCT() {
    return parseInt(new Intl.DateTimeFormat('en-US', { timeZone: 'America/Chicago', hour: 'numeric', hourCycle: 'h23' }).format(new Date()), 10) % 24;
  }
  function stored() { try { return localStorage.getItem('rf-theme'); } catch (e) { return null; } }
  function apply() {
    var pref = stored();
    var day = (pref === 'day' || pref === 'night') ? pref === 'day' : (function () { var h = hourCT(); return h >= 6 && h < 17; })();
    root.setAttribute('data-theme', day ? 'day' : 'night');
    var reset = document.querySelector('.sky-reset'); if (reset) reset.hidden = !pref;
    var sw = document.querySelector('.sky-switch'); if (sw) sw.textContent = day ? 'Switch to night sky' : 'Switch to day sky';
  }
  function flip(e) {
    if (e) e.preventDefault();
    var next = root.getAttribute('data-theme') === 'day' ? 'night' : 'day';
    try { localStorage.setItem('rf-theme', next); } catch (x) {}
    apply();
  }
  [].forEach.call(document.querySelectorAll('.theme-toggle,.sky-switch'), function (el) { el.addEventListener('click', flip); });
  var reset = document.querySelector('.sky-reset');
  if (reset) reset.addEventListener('click', function (e) { e.preventDefault(); try { localStorage.removeItem('rf-theme'); } catch (x) {} apply(); });
  if (!new URLSearchParams(location.search).get('sky')) { apply(); setInterval(apply, 60000); }
  else {
    var r = document.querySelector('.sky-reset'); if (r) r.hidden = true;
    var sw2 = document.querySelector('.sky-switch'); if (sw2) sw2.textContent = root.getAttribute('data-theme') === 'day' ? 'Switch to night sky' : 'Switch to day sky';
  }
})();

/* ------------------------------------------------------------------
   8. Crew booking button pre-selects the reason on the form
------------------------------------------------------------------ */
(function () {
  var a = document.querySelector('[data-reason]'), sel = document.getElementById('reason');
  if (!a || !sel) return;
  a.addEventListener('click', function () {
    var want = a.getAttribute('data-reason');
    [].forEach.call(sel.options, function (o) { if (o.text === want) sel.value = o.value; });
  });
})();
