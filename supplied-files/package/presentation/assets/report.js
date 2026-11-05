/* Progressive enhancement only: no fetches, storage or data mutations. */
(() => {
  'use strict';
  document.documentElement.classList.add('js-ready');
  document.querySelector('.print-button')?.addEventListener('click', () => window.print());
  function tableAccess() {
    document.querySelectorAll('.table-scroll').forEach(table => {
      table.dataset.label ||= table.getAttribute('aria-label') || 'Source table';
      const overflowing = table.scrollWidth > table.clientWidth + 1 && table.clientWidth > 0;
      if (overflowing) {table.tabIndex = 0; table.setAttribute('role', 'region'); table.setAttribute('aria-label', table.dataset.label);}
      else {table.removeAttribute('tabindex'); table.removeAttribute('role'); table.removeAttribute('aria-label');}
    });
  }
  window.addEventListener('resize', tableAccess);
  tableAccess();
  const records = [...document.querySelectorAll('.record')];
  const search = document.querySelector('#search');
  const selects = [...document.querySelectorAll('[data-filter]')];
  const count = document.querySelector('#result-count');
  const empty = document.querySelector('#empty-state');
  const normalize = text => text.normalize('NFKC').toLocaleLowerCase().replace(/\s+/g, ' ').trim();
  const texts = records.map(record => normalize(record.textContent));
  function filter() {
    const terms = normalize(search?.value || '').split(' ').filter(Boolean);
    let shown = 0;
    records.forEach((record, i) => {
      const match = terms.every(term => texts[i].includes(term)) && selects.every(select => {
        const values = JSON.parse(record.getAttribute(`data-${select.dataset.filter}`) || '[]');
        return !select.value || values.includes(select.value);
      });
      record.hidden = !match;
      if (match) shown++;
    });
    if (count) count.textContent = `${shown} of ${records.length} records shown`;
    if (empty) empty.hidden = shown !== 0;
    tableAccess();
  }
  function reset() {
    if (search) search.value = '';
    selects.forEach(select => { select.value = ''; });
    filter();
  }
  let timer;
  search?.addEventListener('input', () => {
    clearTimeout(timer);
    timer = setTimeout(filter, 100);
  });
  selects.forEach(select => select.addEventListener('change', filter));
  document.querySelector('#reset')?.addEventListener('click', () => {
    clearTimeout(timer);
    reset();
    search?.focus();
  });
  function revealHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = id && document.getElementById(id);
    if (!target) return;
    const record = target.closest('.record');
    if (record) {
      if (record.hidden) reset();
      record.querySelectorAll('details').forEach(detail => { detail.open = true; });
    }
    requestAnimationFrame(() => target.scrollIntoView({block: 'start'}));
  }
  window.addEventListener('hashchange', revealHash);
  revealHash();
  let printState = [];
  window.addEventListener('beforeprint', () => {
    printState = [...document.querySelectorAll('details')].map(detail => [detail, detail.open]);
    printState.forEach(([detail]) => { detail.open = true; });
  });
  window.addEventListener('afterprint', () => {
    printState.forEach(([detail, open]) => { detail.open = open; });
    printState = [];
  });
})();
