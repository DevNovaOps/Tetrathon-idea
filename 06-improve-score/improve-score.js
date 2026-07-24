/* ===================================================
   FINORA — Page 6: Improve My Score Scripts
   Progress Bar Animation, Theme Toggle, Reveal
   =================================================== */

(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');
  const revealEls = document.querySelectorAll('.reveal');

  /* ---- THEME PERSISTENCE ---- */
  function stored() {
    try { return localStorage.getItem('finora-theme'); }
    catch (e) { return null; }
  }

  function setTheme(t) {
    html.setAttribute('data-theme', t);
    try { localStorage.setItem('finora-theme', t); }
    catch (e) {}
  }

  setTheme(stored() || 'dark');

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      setTheme(html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
  }

  /* ---- MOBILE SIDEBAR TOGGLE ---- */
  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', e => {
      e.stopPropagation();
      sidebar.classList.toggle('open');
    });

    document.addEventListener('click', e => {
      if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== mobileToggle) {
        sidebar.classList.remove('open');
      }
    });
  }

  /* ---- REVEAL ON SCROLL ---- */
  function checkReveals() {
    const trigger = window.innerHeight * 0.92;
    revealEls.forEach(el => {
      if (el.getBoundingClientRect().top < trigger) {
        el.classList.add('visible');
      }
    });
  }

  window.addEventListener('scroll', checkReveals, { passive: true });
  window.addEventListener('load', checkReveals);
  setTimeout(checkReveals, 100);

  /* ---- ANIMATE PROGRESS BARS ---- */
  function animateProgress() {
    const fill = document.getElementById('roadmapProgressFill');
    if (fill && fill.getBoundingClientRect().top < window.innerHeight) {
      fill.style.width = '40%';
    }

    document.querySelectorAll('.metric-bar-fill').forEach(el => {
      if (el.getBoundingClientRect().top < window.innerHeight && !el.classList.contains('animated')) {
        el.classList.add('animated');
      }
    });
  }

  window.addEventListener('scroll', animateProgress, { passive: true });
  window.addEventListener('load', animateProgress);
  setTimeout(animateProgress, 300);

})();
