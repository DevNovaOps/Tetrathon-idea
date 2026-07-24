/* ===================================================
   FINORA — Page 3: User Onboarding Script
   Theme Toggle, Form UI Animations, Interactive Feedback
   =================================================== */

(function () {
  'use strict';

  /* ---------- DOM REFERENCES ---------- */
  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const btnNext = document.getElementById('btnNext');
  const btnSkip = document.getElementById('btnSkip');
  const formInputs = document.querySelectorAll('.form-input');

  /* ---------- THEME TOGGLE ---------- */
  function getStoredTheme() {
    try {
      return localStorage.getItem('finora-theme');
    } catch (e) {
      return null;
    }
  }

  function setTheme(theme) {
    html.setAttribute('data-theme', theme);
    try {
      localStorage.setItem('finora-theme', theme);
    } catch (e) {
      // silently fail
    }
  }

  // Initialise theme from storage or default to dark
  (function initTheme() {
    var stored = getStoredTheme();
    if (stored) {
      setTheme(stored);
    } else {
      setTheme('dark');
    }
  })();

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      var current = html.getAttribute('data-theme');
      setTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  /* ---------- BUTTON CLICK FEEDBACK ---------- */
  if (btnNext) {
    btnNext.addEventListener('click', function (e) {
      e.preventDefault();
      // Subtle pulse feedback
      btnNext.style.transform = 'scale(0.97)';
      setTimeout(function () {
        btnNext.style.transform = '';
      }, 150);
    });
  }

  if (btnSkip) {
    btnSkip.addEventListener('click', function (e) {
      e.preventDefault();
      btnSkip.style.transform = 'scale(0.97)';
      setTimeout(function () {
        btnSkip.style.transform = '';
      }, 150);
    });
  }

  /* ---------- INPUT HIGHLIGHT ON FOCUS ---------- */
  formInputs.forEach(function (input) {
    input.addEventListener('focus', function () {
      var group = input.closest('.form-group');
      if (group) {
        group.classList.add('focused');
      }
    });

    input.addEventListener('blur', function () {
      var group = input.closest('.form-group');
      if (group) {
        group.classList.remove('focused');
      }
    });
  });

})();
