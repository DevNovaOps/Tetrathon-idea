/* ===================================================
   FINORA — Page 16: Settings Scripts
   Theme Toggle, Interactive Toggles, Mobile Sidebar, Reveal
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const appearanceRow = document.getElementById('appearanceRow');
  const themeLabel = document.getElementById('themeLabel');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');
  const revealEls = document.querySelectorAll('.reveal');

  /* ---- THEME PERSISTENCE & TOGGLE ---- */
  function stored() { try { return localStorage.getItem('finora-theme'); } catch(e) { return null; } }
  
  function setTheme(t) {
    html.setAttribute('data-theme', t);
    try { localStorage.setItem('finora-theme', t); } catch(e){}
    if (themeLabel) {
      themeLabel.textContent = t === 'dark' ? 'Dark Mode' : 'Light Mode';
    }
  }

  setTheme(stored() || 'dark');

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      setTheme(next);
    });
  }

  if (appearanceRow) {
    appearanceRow.addEventListener('click', () => {
      const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      setTheme(next);
    });
  }

  /* ---- MOBILE SIDEBAR ---- */
  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', e => { e.stopPropagation(); sidebar.classList.toggle('open'); });
    document.addEventListener('click', e => { if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== mobileToggle) sidebar.classList.remove('open'); });
  }

  /* ---- REVEAL ON SCROLL ---- */
  function checkReveals() {
    const trigger = window.innerHeight * 0.92;
    revealEls.forEach(el => { if (el.getBoundingClientRect().top < trigger) el.classList.add('visible'); });
  }
  window.addEventListener('scroll', checkReveals, { passive: true });
  window.addEventListener('load', checkReveals);
  setTimeout(checkReveals, 100);

  /* ---- BOOT ---- */
  function boot() {
    checkReveals();
  }

  document.addEventListener('DOMContentLoaded', boot);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(boot, 50);
  }

})();
