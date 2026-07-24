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

  /* ============================================================
     BACKEND INTEGRATION — Fetch API
     ============================================================ */

  const API_BASE = window.location.origin;

  /** Read Django CSRF token from the cookie. */
  function getCSRFToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
  }

  /** Ensure a CSRF cookie exists by hitting the user endpoint once. */
  async function ensureCSRF() {
    if (!getCSRFToken()) {
      try {
        await fetch(`${API_BASE}/api/auth/user/`, { credentials: 'same-origin' });
      } catch (_) { /* ignore — we just want the cookie set */ }
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
    // Avoid duplicates
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
    full_name: 'fullName',
    email: 'signupEmail',
    phone: 'signupPhone',
    country: 'countrySelect',
    password: 'signupPassword',
    confirm_password: 'confirmPassword',
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

  // ── Intercept "Create Account" click ────────────────────────────
  const signupBtn = document.querySelector('#signupForm .btn-primary');

  if (signupBtn) {
    signupBtn.addEventListener('click', async function (e) {
      e.preventDefault();
      clearErrors();

      // Client-side: terms checkbox
      const termsBox = document.getElementById('agreeTerms');
      if (termsBox && !termsBox.checked) {
        showFieldError('agreeTerms', 'You must agree to the Terms & Privacy Policy.');
        return;
      }

      const payload = {
        full_name: document.getElementById('fullName')?.value.trim() || '',
        email: document.getElementById('signupEmail')?.value.trim() || '',
        phone: document.getElementById('signupPhone')?.value.trim() || '',
        country: document.getElementById('countrySelect')?.value || '',
        password: document.getElementById('signupPassword')?.value || '',
        confirm_password: document.getElementById('confirmPassword')?.value || '',
      };

      // Disable button to prevent double-submit
      signupBtn.style.pointerEvents = 'none';
      signupBtn.style.opacity = '0.7';
      const originalText = signupBtn.querySelector('span');
      if (originalText) originalText.textContent = 'Creating Account…';

      try {
        await ensureCSRF();

        const res = await fetch(`${API_BASE}/api/auth/register/`, {
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
          // Redirect to onboarding
          window.location.href = data.data.redirect;
        } else if (data.errors) {
          renderErrors(data.errors);
        } else {
          showFieldError('signupEmail', data.message || 'Registration failed.');
        }
      } catch (err) {
        console.error('Signup error:', err);
        showFieldError('signupEmail', 'Network error. Please try again.');
      } finally {
        signupBtn.style.pointerEvents = '';
        signupBtn.style.opacity = '';
        if (originalText) originalText.textContent = 'Create Account';
      }
    });
  }

  // ── Google Login button ─────────────────────────────────────────
  const socialBtns = document.querySelectorAll('.btn-social');
  if (socialBtns.length > 0) {
    // First social button is Google
    socialBtns[0].addEventListener('click', () => {
      window.location.href = `${API_BASE}/accounts/google/login/`;
    });
  }

})();
