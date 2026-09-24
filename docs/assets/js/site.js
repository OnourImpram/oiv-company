/* OIV. Progressive enhancements for navigation, search, filters and local briefs. */
(() => {
  'use strict';
  const lang = document.body.dataset.language === 'tr' ? 'tr' : 'en';
  const root = document.body.dataset.root || '';
  const tr = lang === 'tr';
  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  document.documentElement.classList.add('js');

  const header = $('.site-header'), menu = $('.menu-toggle'), nav = $('#main-nav');
  if (header && menu && nav) {
    menu.hidden = false;
    const closeMenu = () => {
      header.classList.remove('menu-open');
      menu.setAttribute('aria-expanded', 'false');
    };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      header.classList.toggle('menu-open', open);
      menu.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && header.classList.contains('menu-open')) { closeMenu(); menu.focus(); }
    });
    document.addEventListener('click', e => { if (!header.contains(e.target)) closeMenu(); });
    matchMedia('(min-width:1001px)').addEventListener('change', closeMenu);
  }

  const dialog = $('#site-search'), searchToggle = $('.search-toggle'), searchInput = $('#search-input'), searchResults = $('#search-results');
  if (dialog && searchToggle && searchInput && searchResults && window.OIV && window.OIV_SEARCH) {
    const records = window.OIV_SEARCH[lang] || [];
    let previousFocus = null;
    const showResults = () => {
      const matches = window.OIV.search(records, searchInput.value);
      searchResults.replaceChildren();
      if (!matches.length) {
        const p = document.createElement('p'); p.textContent = searchResults.dataset.empty; searchResults.append(p); return;
      }
      for (const record of matches) {
        const a = document.createElement('a'); a.href = root + record.href;
        const title = document.createElement('strong'); title.textContent = record.title;
        const desc = document.createElement('span'); desc.textContent = record.text.split('. ').slice(0,1).join('. ') + '.';
        a.append(title, desc); searchResults.append(a);
      }
    };
    const openSearch = () => {
      if (dialog.open) return;
      previousFocus = document.activeElement;
      dialog.showModal(); showResults(); searchInput.focus();
    };
    if (typeof dialog.showModal === 'function') {
      searchToggle.hidden = false;
      searchToggle.addEventListener('click', openSearch);
      $('.close-search').addEventListener('click', () => dialog.close());
      // Search fields can consume Escape to clear their value. Close the dialog explicitly.
      dialog.addEventListener('keydown', e => { if (e.key === 'Escape') { e.preventDefault(); dialog.close(); } });
      dialog.addEventListener('click', e => {
        if (e.target === dialog) {
          const r=dialog.getBoundingClientRect();
          if (e.clientX<r.left || e.clientX>r.right || e.clientY<r.top || e.clientY>r.bottom) dialog.close();
        }
      });
      dialog.addEventListener('close', () => { if (previousFocus && previousFocus.isConnected) previousFocus.focus(); });
      document.addEventListener('keydown', e => { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase()==='k') { e.preventDefault(); openSearch(); } });
      searchInput.addEventListener('input', showResults);
    }
  }

  const filterBar = $('.filter-bar');
  if (filterBar) {
    const cards = $$('[data-category]'), buttons = $$('[data-filter]'), count = $('.filter-count');
    filterBar.hidden = false;
    const applyFilter = value => {
      const safe = ['source','product'].includes(value) ? value : 'all';
      let visible = 0;
      cards.forEach(card => { card.hidden = safe !== 'all' && card.dataset.category !== safe; if (!card.hidden) visible++; });
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter===safe)));
      if (count) count.textContent = tr ? `${visible} çalışma gösteriliyor.` : `${visible} projects shown.`;
    };
    buttons.forEach(button => button.addEventListener('click', () => applyFilter(button.dataset.filter)));
    applyFilter('all');
    // Deep links to a project remain useful after filtering.
    addEventListener('hashchange', () => { if (['#mergen','#mneme'].includes(location.hash)) applyFilter('all'); });
  }

  const form = $('#brief-form'), app = $('.brief-app');
  if (form && app && window.OIV) {
    const preview = $('#brief-preview'), text = $('#brief-text'), status = $('#copy-result');
    let prepared = null;
    app.hidden = false;
    const topic = $('#topic');
    const requested = new URLSearchParams(location.search).get('topic');
    if (requested && [...topic.options].some(o => o.value===requested)) topic.value = requested;
    const message = $('#message'), counter = $('.char-count');
    message.addEventListener('input', () => { counter.textContent = `${message.value.length} / 3000`; });
    const data = () => Object.fromEntries(new FormData(form));
    form.addEventListener('input', e => {
      const target=e.target;
      if (target.getAttribute('aria-invalid')==='true') {
        target.removeAttribute('aria-invalid');
        const error=document.getElementById(target.id+'-error');if(error) error.hidden=true;
      }
    });
    form.addEventListener('submit', e => {
      e.preventDefault();
      const input=data(),errors=window.OIV.validate(input,lang);
      $$('.field-error').forEach(p=>{p.hidden=true;p.textContent='';});
      form.querySelectorAll('[aria-invalid]').forEach(el=>el.removeAttribute('aria-invalid'));
      if (Object.keys(errors).length) {
        for (const [field,value] of Object.entries(errors)) {
          const control=document.getElementById(field),error=document.getElementById(field+'-error');
          if(control) control.setAttribute('aria-invalid','true');
          if(error){error.textContent=value;error.hidden=false;}
        }
        document.getElementById(Object.keys(errors)[0]).focus();return;
      }
      prepared=window.OIV.buildBrief(input,lang);text.value=prepared.body;
      $('#email-draft').href=prepared.url;
      $('.long-brief-note').hidden=!prepared.tooLong;
      form.hidden=true;preview.hidden=false;status.textContent='';$('#preview-title').focus();
    });
    $('.edit-brief').addEventListener('click',()=>{preview.hidden=true;form.hidden=false;message.focus();});
    $('#copy-brief').addEventListener('click',async()=>{
      if(!prepared)return;
      try {
        if (!navigator.clipboard || !window.isSecureContext) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(text.value);status.textContent=status.dataset.ok;
      } catch {
        text.focus();text.select();status.textContent=status.dataset.failed;
      }
    });
    $('#save-brief').addEventListener('click',()=>{
      if(!prepared)return;
      const blob=new Blob(['\ufeff'+text.value],{type:'text/plain;charset=utf-8'});
      const url=URL.createObjectURL(blob),a=document.createElement('a');
      a.href=url;a.download=`OIV-${tr?'Gorusme-Notu':'Enquiry-Brief'}.txt`;document.body.append(a);a.click();a.remove();
      setTimeout(()=>URL.revokeObjectURL(url),1500);
    });
    // Never submit via fetch, store form data or report that an email was sent.
  }
})();

/* motion-2026-09-24: orchestrated hero, paused offscreen and in hidden tabs; static under reduced motion. */
(() => {
  'use strict';
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.documentElement.classList.add('motion');
  const compass = document.querySelector('.compass');
  let visible = true;
  const sync = () => compass && compass.classList.toggle('is-paused', !visible || document.hidden);
  if (compass) {
    new IntersectionObserver(entries => { visible = entries[0].isIntersecting; sync(); }).observe(compass);
    document.addEventListener('visibilitychange', sync);
  }
  const rules = [...document.querySelectorAll('main h1, main h2')].filter(h => getComputedStyle(h, '::before').content !== 'none');
  const seen = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in-view'); seen.unobserve(e.target); }
  }), {rootMargin: '0px 0px -10% 0px'});
  rules.forEach(h => { h.classList.add('rule'); seen.observe(h); });
  const land = document.querySelector('.hero-landscape'), hero = document.querySelector('.hero');
  if (land && hero) {
    let inView = true, queued = false;
    new IntersectionObserver(entries => { inView = entries[0].isIntersecting; }).observe(hero);
    const paint = () => { queued = false; const y = Math.min(scrollY, hero.offsetHeight); land.style.transform = `translate3d(0, ${(y * 0.14).toFixed(1)}px, 0) scale(1.06)`; };
    addEventListener('scroll', () => { if (inView && !queued) { queued = true; requestAnimationFrame(paint); } }, {passive: true});
    paint();
  }
})();

/* orbit-nodes-2026-09-24: nodes travel the orbit and take turns transferring to the middle ring.
   One rAF loop, transform/opacity only. Held on hover/focus so a node can be clicked; paused
   offscreen and in hidden tabs; off at 1000px and below where the orbit gets crowded (rings still turn); static under reduced motion. */
(() => {
  'use strict';
  const compass = document.querySelector('.compass');
  if (!compass || !document.documentElement.classList.contains('motion')) return;
  const nodes = [...compass.querySelectorAll('.compass-node')];
  const pulse = () => compass.querySelector('.ring-pulse')?.getAnimations().find(a => a.animationName === 'orbit-cw');
  const small = matchMedia('(max-width: 1000px)');
  const OUTER = 160, INNER = 116, TURN = 90000, SLOT = 6000, CYCLE = SLOT * nodes.length, MOVE = 2000, HOLD = 1500;
  const ease = x => x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x);
  let t = 0, last = 0, raf = 0, held = false, geo = null;
  const measure = () => {
    const w = compass.clientWidth, h = compass.clientHeight, s = Math.min(w / 500, h / 440);
    geo = {cx: w / 2, cy: h / 2, s, home: nodes.map(n => {
      const cs = getComputedStyle(n), x = parseFloat(cs.left), y = parseFloat(cs.top);
      return {x, y, a: Math.atan2(y - h / 2, x - w / 2), hw: n.offsetWidth / 2 + 4, hh: n.offsetHeight / 2 + 4};
    }), keep: [...compass.querySelectorAll('.compass-aside, .compass-quote, .compass-center')].filter(e => e.offsetParent).map(e => {
      const c = compass.getBoundingClientRect(), r = e.getBoundingClientRect();
      return {l: r.left - c.left, t: r.top - c.top, r: r.right - c.left, b: r.bottom - c.top};
    })};
  };
  const place = () => {
    const {cx, cy, s, home} = geo, spin = (t / TURN) * Math.PI * 2;
    const p = pulse(), T = 24000;
    const pa = p ? (8 + 360 * ((p.currentTime || 0) % T) / T) * Math.PI / 180 : null;
    nodes.forEach((n, i) => {
      const k = (t - i * SLOT) % CYCLE, u = k < 0 ? 0 : k;
      const inward = ease(u / MOVE) - ease((u - MOVE - HOLD) / MOVE);
      const r = (OUTER - (OUTER - INNER) * inward) * s * Math.min(1, 0.4 + t / 2500) + Math.hypot(home[i].x - cx, home[i].y - cy) * Math.max(0, 0.6 - t / 2500);
      const a = home[i].a + spin, {hw, hh} = home[i];
      const clear = rr => { const px = cx + rr * Math.cos(a), py = cy + rr * Math.sin(a);
        return !geo.keep.some(k => px - hw < k.r && k.l < px + hw && py - hh < k.b && k.t < py + hh); };
      let rr = r;
      if (!clear(rr)) { let lo = rr; for (let d = 4; d < rr; d += 4) { if (clear(rr - d)) { lo = rr - d; break; } } rr = lo; }
      const x = cx + rr * Math.cos(a) - home[i].x, y = cy + rr * Math.sin(a) - home[i].y;
      n.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) translate(-50%, -50%)`;
      const icon = n.querySelector('.icon');
      if (icon && pa !== null) {
        let d = Math.abs(((a - pa) % (Math.PI * 2) + Math.PI * 3) % (Math.PI * 2) - Math.PI);
        icon.style.opacity = (0.72 + 0.28 * Math.max(0, 1 - d / 0.35)).toFixed(2);
      }
    });
  };
  const frame = now => {
    raf = 0;
    if (last) t += Math.min(now - last, 100);
    last = now;
    place();
    run();
  };
  let visible = true;
  const run = () => {
    const go = visible && !document.hidden && !held && !small.matches;
    if (go && !raf) raf = requestAnimationFrame(frame);
    if (!go) { if (raf) cancelAnimationFrame(raf); raf = 0; last = 0; }
  };
  const reset = () => { if (small.matches) nodes.forEach(n => { n.style.transform = ''; const i = n.querySelector('.icon'); if (i) i.style.opacity = ''; }); };
  const hold = on => { held = on; compass.classList.toggle('is-held', on); run(); };
  nodes.forEach(n => {
    n.addEventListener('pointerenter', () => hold(true));
    n.addEventListener('pointerleave', () => hold(compass.contains(document.activeElement) && document.activeElement.matches('.compass-node')));
    n.addEventListener('focus', () => hold(true));
    n.addEventListener('blur', () => hold(false));
  });
  new IntersectionObserver(e => { visible = e[0].isIntersecting; run(); }).observe(compass);
  document.addEventListener('visibilitychange', run);
  addEventListener('resize', () => { measure(); reset(); run(); }, {passive: true});
  small.addEventListener?.('change', () => { reset(); run(); });
  measure(); reset(); run();
})();

/* motion-cycle-2026-09-24: the process flow and the values cycle run only while at least a
   third of them is on screen and the tab is visible. Reduced motion never adds .motion. */
(() => {
  'use strict';
  if (!document.documentElement.classList.contains('motion')) return;
  const loops = [...document.querySelectorAll('[data-loop]')], shown = new Set();
  const sync = () => loops.forEach(el => el.classList.toggle('is-paused', document.hidden || !shown.has(el)));
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => e.intersectionRatio >= 0.33 ? shown.add(e.target) : shown.delete(e.target)); sync();
  }, {threshold: [0, 0.33]});
  loops.forEach(el => io.observe(el));
  document.addEventListener('visibilitychange', sync);
  sync();
})();
/* motion-a11y-2026-09-24: WCAG 2.2.2. A loop counts laps of its reference animation (paused
   time does not count) and after three it settles into its static end state via .is-done. */
(() => {
  'use strict';
  if (!document.documentElement.classList.contains('motion')) return;
  const LAPS = 3;
  document.querySelectorAll('[data-loop]').forEach(el => {
    const ref = el.classList.contains('cycle') ? 'cycle-light' : 'step-ring';
    const first = el.querySelector('.cycle-light, .step-line span');
    let laps = 0;
    el.addEventListener('animationiteration', e => {
      if (e.animationName !== ref || e.target !== first) return;
      if (++laps >= LAPS) el.classList.add('is-done');
    });
  });
})();