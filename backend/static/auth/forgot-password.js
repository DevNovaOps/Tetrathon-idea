/* ===================================================
   FINORA — Forgot Password Scripts
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const sendBtn = document.getElementById('sendBtn');
  const resetEmail = document.getElementById('resetEmail');
  const requestState = document.getElementById('requestState');
  const successState = document.getElementById('successState');
  const sentEmailDisplay = document.getElementById('sentEmailDisplay');
  const resendBtn = document.getElementById('resendBtn');

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

  /* ---- STATIC RESET LINK SUBMISSION ---- */
  if (sendBtn && requestState && successState) {
    sendBtn.addEventListener('click', () => {
      const emailVal = resetEmail ? resetEmail.value.trim() || 'devsharma@gmail.com' : 'devsharma@gmail.com';
      if (sentEmailDisplay) sentEmailDisplay.textContent = emailVal;
      requestState.style.display = 'none';
      successState.classList.remove('hidden-state');
    });
  }

  if (resendBtn) {
    resendBtn.addEventListener('click', () => {
      resendBtn.textContent = 'Reset Link Resent ✓';
      resendBtn.style.color = '#10B981';
      setTimeout(() => {
        resendBtn.textContent = 'Resend Email';
        resendBtn.style.color = '';
      }, 3000);
    });
  }

})();
