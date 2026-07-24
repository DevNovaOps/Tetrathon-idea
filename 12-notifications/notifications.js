/* ===================================================
   FINORA — Page 12: Notifications Scripts
   Filter Chips, Unread Toggle, Quick Actions, Reveal
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');
  const revealEls = document.querySelectorAll('.reveal');

  const chips = document.querySelectorAll('.chip');
  const notifCards = document.querySelectorAll('.notif-card');
  const markReadBtn = document.querySelector('.qa-btn');

  /* ---- THEME PERSISTENCE ---- */
  function stored() { try { return localStorage.getItem('finora-theme'); } catch(e) { return null; } }
  function setTheme(t) {
    html.setAttribute('data-theme', t);
    try { localStorage.setItem('finora-theme', t); } catch(e){}
  }
  setTheme(stored() || 'dark');
  if (themeToggle) themeToggle.addEventListener('click', () => { setTheme(html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'); });

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

  /* ---- FILTER CHIPS INTERACTIVITY ---- */
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');

      const filterText = chip.textContent.trim().toLowerCase();

      notifCards.forEach(card => {
        if (filterText.includes('all')) {
          card.style.display = 'flex';
        } else if (filterText.includes('unread')) {
          if (card.classList.contains('unread')) {
            card.style.display = 'flex';
          } else {
            card.style.display = 'none';
          }
        } else {
          // General category filter simulation
          card.style.display = 'flex';
        }
      });
    });
  });

  /* ---- CLICK NOTIFICATION TO MARK AS READ ---- */
  notifCards.forEach(card => {
    card.addEventListener('click', () => {
      card.classList.remove('unread');
      const dotWrap = card.querySelector('.notif-dot-wrap');
      if (dotWrap) dotWrap.style.display = 'none';
      updateUnreadCount();
    });
  });

  /* ---- MARK ALL AS READ QUICK ACTION ---- */
  if (markReadBtn) {
    markReadBtn.addEventListener('click', () => {
      notifCards.forEach(card => {
        card.classList.remove('unread');
        const dotWrap = card.querySelector('.notif-dot-wrap');
        if (dotWrap) dotWrap.style.display = 'none';
      });
      updateUnreadCount();
    });
  }

  function updateUnreadCount() {
    const unreadCount = document.querySelectorAll('.notif-card.unread').length;
    const unreadStat = document.querySelector('.stat-row .stat-val[style*="EF4444"]');
    if (unreadStat) unreadStat.textContent = unreadCount;

    const chipCount = document.querySelector('.chip-count');
    if (chipCount) chipCount.textContent = unreadCount;

    const bellBadge = document.querySelector('.bell-badge');
    if (bellBadge) bellBadge.style.display = unreadCount > 0 ? 'block' : 'none';
  }

  /* ---- BOOT ---- */
  function boot() {
    checkReveals();
  }

  document.addEventListener('DOMContentLoaded', boot);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(boot, 50);
  }

})();
