/* ===================================================
   FINORA — Authentication Module Scripts (Login)
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const togglePasswordBtn = document.getElementById('togglePassword');
  const passwordInput = document.getElementById('loginPassword');

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

  /* ---- PASSWORD VISIBILITY TOGGLE ---- */
  if (togglePasswordBtn && passwordInput) {
    togglePasswordBtn.addEventListener('click', () => {
      const eyeOpen = togglePasswordBtn.querySelector('.eye-open');
      const eyeClosed = togglePasswordBtn.querySelector('.eye-closed');
      if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        if (eyeOpen) eyeOpen.classList.add('hidden');
        if (eyeClosed) eyeClosed.classList.remove('hidden');
      } else {
        passwordInput.type = 'password';
        if (eyeOpen) eyeOpen.classList.remove('hidden');
        if (eyeClosed) eyeClosed.classList.add('hidden');
      }
    });
  }

})();
