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
