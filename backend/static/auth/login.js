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

  /* ============================================================
     BACKEND INTEGRATION — Fetch API
     ============================================================ */

  const API_BASE = window.location.origin;

  /** Read Django CSRF token from the cookie. */
  function getCSRFToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
  }

  /** Ensure a CSRF cookie exists. */
  async function ensureCSRF() {
    if (!getCSRFToken()) {
      try {
        await fetch(`${API_BASE}/api/auth/user/`, { credentials: 'same-origin' });
      } catch (_) { /* ignore */ }
    }
  }

  /** Remove existing error messages from the form. */
  function clearErrors() {
    document.querySelectorAll('.field-error').forEach(el => el.remove());
  }

  /** Display a validation error below a form field. */
  function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    const wrapper = field.closest('.form-group');
    if (!wrapper) return;
    const existing = wrapper.querySelector('.field-error');
    if (existing) existing.remove();
    const errorEl = document.createElement('span');
    errorEl.className = 'field-error';
    errorEl.style.cssText = 'color:#ef4444;font-size:12px;margin-top:4px;display:block;';
    errorEl.textContent = message;
    wrapper.appendChild(errorEl);
  }

  /** Map backend field names to frontend input IDs. */
  const FIELD_MAP = {
    email: 'loginEmail',
    password: 'loginPassword',
  };

  /** Display backend errors mapped to the correct fields. */
  function renderErrors(errors) {
    clearErrors();
    for (const [field, messages] of Object.entries(errors)) {
      const frontId = FIELD_MAP[field] || field;
      const msg = Array.isArray(messages) ? messages[0] : messages;
      showFieldError(frontId, msg);
    }
  }

  // ── Intercept "Sign In" click ───────────────────────────────────
  const loginBtn = document.querySelector('#loginForm .btn-primary');

  if (loginBtn) {
    loginBtn.addEventListener('click', async function (e) {
      e.preventDefault();
      clearErrors();

      const payload = {
        email: document.getElementById('loginEmail')?.value.trim() || '',
        password: document.getElementById('loginPassword')?.value || '',
        remember_me: document.getElementById('rememberMe')?.checked || false,
      };

      // Basic client-side check
      if (!payload.email) {
        showFieldError('loginEmail', 'Email is required.');
        return;
      }
      if (!payload.password) {
        showFieldError('loginPassword', 'Password is required.');
        return;
      }

      // Disable button
      loginBtn.style.pointerEvents = 'none';
      loginBtn.style.opacity = '0.7';
      const originalText = loginBtn.querySelector('span');
      if (originalText) originalText.textContent = 'Signing In…';

      try {
        await ensureCSRF();

        const res = await fetch(`${API_BASE}/api/auth/login/`, {
          method: 'POST',
          credentials: 'same-origin',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          body: JSON.stringify(payload),
        });

        const data = await res.json();

        if (data.success) {
          // Redirect based on onboarding status
          window.location.href = data.data.redirect;
        } else if (data.errors) {
          renderErrors(data.errors);
        } else {
          showFieldError('loginEmail', data.message || 'Login failed.');
        }
      } catch (err) {
        console.error('Login error:', err);
        showFieldError('loginEmail', 'Network error. Please try again.');
      } finally {
        loginBtn.style.pointerEvents = '';
        loginBtn.style.opacity = '';
        if (originalText) originalText.textContent = 'Sign In';
      }
    });
  }

  // ── Google Login button ─────────────────────────────────────────
  const socialBtns = document.querySelectorAll('.btn-social');
  if (socialBtns.length > 0) {
    socialBtns[0].addEventListener('click', () => {
      window.location.href = `${API_BASE}/accounts/google/login/`;
    });
  }

})();
