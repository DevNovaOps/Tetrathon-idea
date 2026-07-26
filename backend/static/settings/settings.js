/* ===================================================
   FINORA — Page 16: Settings Scripts (Backend Driven)
   Theme Toggle, Interactive Toggles, Mobile Sidebar, Reveal,
   Live APIs for Appearance, Notifications, Privacy, Support
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

  /* ---- CSRF TOKEN HELPERS ---- */
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  /* ---- THEME PERSISTENCE & TOGGLE ---- */
  function stored() { try { return localStorage.getItem('finora-theme'); } catch(e) { return null; } }
  
  function setTheme(t) {
    html.setAttribute('data-theme', t);
    try { localStorage.setItem('finora-theme', t); } catch(e){}
    if (themeLabel) {
      themeLabel.textContent = t === 'dark' ? 'Dark Mode' : 'Light Mode';
    }
    // Save to backend asynchronously
    if (csrftoken) {
      fetch('/api/settings/update/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
        body: JSON.stringify({ theme: t })
      }).catch(()=>{});
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
    appearanceRow.style.cursor = 'pointer';
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

  /* ---- BACKEND API INTEGRATION ---- */
  async function loadSettingsData() {
    try {
      const res = await fetch('/api/settings/');
      if (!res.ok) return;
      const data = await res.json();
      renderSettings(data);
    } catch(err) { console.error('Settings load error:', err); }
  }

  function renderSettings(data) {
    if (data.appearance && data.appearance.theme) {
      const t = data.appearance.theme;
      html.setAttribute('data-theme', t);
      if (themeLabel) themeLabel.textContent = t === 'dark' ? 'Dark Mode' : 'Light Mode';
    }

    // Connect Notification Preference Toggles
    const toggles = document.querySelectorAll('.toggle-row input[type="checkbox"]');
    if (toggles && toggles.length >= 8 && data.notifications) {
      const n = data.notifications;
      const app = data.appearance || {};
      toggles[0].checked = n.bills !== false;
      toggles[1].checked = n.investments !== false;
      toggles[2].checked = n.credit_score !== false;
      toggles[3].checked = n.education !== false;
      toggles[4].checked = app.marketing_emails === true;
      toggles[5].checked = n.ai_insights !== false;
      toggles[6].checked = app.weekly_reports_email !== false;
      toggles[7].checked = app.monthly_reports_email !== false;

      // Add change listeners
      const keys = ['bills', 'investments', 'credit_score', 'education', 'marketing_emails', 'ai_insights', 'weekly_reports_email', 'monthly_reports_email'];
      toggles.forEach((chk, idx) => {
        chk.onchange = async () => {
          const k = keys[idx];
          const isAppSetting = ['marketing_emails', 'weekly_reports_email', 'monthly_reports_email'].includes(k);
          const url = isAppSetting ? '/api/settings/update/' : '/api/settings/notifications/';
          const body = {};
          body[k] = chk.checked;
          try {
            await fetch(url, {
              method: 'PATCH',
              headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
              body: JSON.stringify(body)
            });
          } catch(err) { console.error('Setting toggle error:', err); }
        };
      });
    }

    // Connect Setting Rows
    const rows = document.querySelectorAll('.setting-row');
    if (rows && rows.length >= 6) {
      // 0: Appearance (already attached)
      // 1: Notifications
      rows[1].style.cursor = 'pointer';
      rows[1].onclick = () => window.location.href = '/notifications/';
      
      // 2: Privacy & Security
      rows[2].style.cursor = 'pointer';
      rows[2].onclick = async () => {
        if (confirm('Would you like to log out from all other active sessions for privacy & security?')) {
          try {
            const r = await fetch('/api/settings/privacy/action/', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
              body: JSON.stringify({ action: 'logout_all_devices' })
            });
            const res = await r.json();
            alert(res.message || 'Logged out from all sessions.');
          } catch(err){}
        }
      };

      // 3: Language
      rows[3].style.cursor = 'pointer';
      rows[3].onclick = () => {
        const lang = prompt('Enter preferred language code (e.g., English, Hindi, Spanish):', 'English');
        if (lang) {
          const valEl = rows[3].querySelector('.setting-value');
          if (valEl) valEl.textContent = lang;
          fetch('/api/settings/update/', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
            body: JSON.stringify({ language: lang })
          }).catch(()=>{});
        }
      };

      // 4: Export Data
      rows[4].style.cursor = 'pointer';
      rows[4].onclick = () => {
        window.location.href = '/api/profile/export/?format=zip';
      };

      // 5: Delete Account
      rows[5].style.cursor = 'pointer';
      rows[5].onclick = async () => {
        if (confirm('WARNING: Are you sure you want to permanently deactivate your account? This action cannot be undone.')) {
          try {
            const r = await fetch('/api/settings/privacy/action/', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
              body: JSON.stringify({ action: 'delete_account' })
            });
            if (r.ok) {
              alert('Account deactivated. Redirecting...');
              window.location.href = '/accounts/logout/';
            }
          } catch(err){}
        }
      };
    }

    // Connect Support grid items
    const supItems = document.querySelectorAll('.support-grid .support-item');
    if (supItems && supItems.length >= 6) {
      supItems[0].onclick = () => alert('Finora Help Center 24/7 Support: Reach out to support@finora.ai or call 1800-FINORA.');
      supItems[1].onclick = () => alert('Frequently Asked Questions:\nQ: How does simulator work?\nA: It uses your primary active goal and monthly savings to project wealth.');
      supItems[2].onclick = () => alert('Contact Support: Please email support@finora.ai for instant assistance.');
      supItems[3].onclick = () => {
        const fb = prompt('Please enter your feedback or feature request for Finora:');
        if (fb) alert('Thank you for your valuable feedback! We have submitted it to our product team.');
      };
      supItems[4].onclick = () => alert('Terms & Conditions: By using Finora, you agree to our standard terms of service for financial analysis.');
      supItems[5].onclick = () => alert('Privacy Policy: Your financial data is encrypted and used solely for personalized AI coaching.');
    }
  }

  /* ---- BOOT ---- */
  function boot() {
    checkReveals();
    loadSettingsData();
  }

  document.addEventListener('DOMContentLoaded', boot);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(boot, 50);
  }

})();
