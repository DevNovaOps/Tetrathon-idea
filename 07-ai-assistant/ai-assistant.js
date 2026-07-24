/* ===================================================
   FINORA — Page 7: AI Financial Assistant Scripts
   Theme Toggle, Sidebar, Reveal, Chat Scroll
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');
  const revealEls = document.querySelectorAll('.reveal');
  const chatMessages = document.getElementById('chatMessages');

  /* ---- THEME ---- */
  function stored() { try { return localStorage.getItem('finora-theme'); } catch(e) { return null; } }
  function setTheme(t) { html.setAttribute('data-theme', t); try { localStorage.setItem('finora-theme', t); } catch(e){} }
  setTheme(stored() || 'dark');
  if (themeToggle) themeToggle.addEventListener('click', () => { setTheme(html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'); });

  /* ---- MOBILE SIDEBAR ---- */
  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', e => { e.stopPropagation(); sidebar.classList.toggle('open'); });
    document.addEventListener('click', e => { if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== mobileToggle) sidebar.classList.remove('open'); });
  }

  /* ---- REVEAL ON SCROLL ---- */
  function checkReveals() {
    const trigger = window.innerHeight * 0.95;
    revealEls.forEach(el => { if (el.getBoundingClientRect().top < trigger) el.classList.add('visible'); });
  }
  window.addEventListener('scroll', checkReveals, { passive: true });
  window.addEventListener('load', checkReveals);
  setTimeout(checkReveals, 100);

  /* ---- SCROLL CHAT TO BOTTOM ---- */
  if (chatMessages) {
    setTimeout(() => { chatMessages.scrollTop = chatMessages.scrollHeight; }, 300);
  }

  /* ---- STAGGERED MESSAGE FADE-IN ---- */
  const messages = document.querySelectorAll('.message');
  messages.forEach((msg, i) => {
    msg.style.animationDelay = (i * 0.12) + 's';
  });

})();
