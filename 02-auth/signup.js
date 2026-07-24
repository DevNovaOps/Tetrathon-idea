/* ===================================================
   FINORA — Sign Up Scripts
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');

  /* ---- THEME PERSISTENCE ---- */
  function stored() { try { return localStorage.getItem('finora-theme'); } catch(e) { return null; } }
  function setTheme(t) {
    html.setAttribute('data-theme', t);
    try { localStorage.setItem('finora-theme', t); } catch(e){}
  }
  setTheme(stored() || 'dark');

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = html.getAttribute('data-theme') || 'dark';
      setTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

})();
