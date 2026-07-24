/* ===================================================
   FINORA — Landing Page Scripts
   Theme Toggle, Sticky Nav, Animations
   =================================================== */

(function () {
  'use strict';

  /* ---------- DOM REFERENCES ---------- */
  const html = document.documentElement;
  const navbar = document.getElementById('navbar');
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('navLinks');
  const themeToggle = document.getElementById('themeToggle');
  const reveals = document.querySelectorAll('.reveal');

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

  // Initialise theme from storage or system preference
  (function initTheme() {
    var stored = getStoredTheme();
    if (stored) {
      setTheme(stored);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setTheme('dark');
    } else {
      setTheme('light');
    }
  })();

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      var current = html.getAttribute('data-theme');
      setTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  /* ---------- STICKY NAVBAR ---------- */
  var lastScroll = 0;
  var ticking = false;

  function handleScroll() {
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollY > 20) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    lastScroll = scrollY;
    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) {
      window.requestAnimationFrame(handleScroll);
      ticking = true;
    }
  }, { passive: true });

  // Run once on load
  handleScroll();

  /* ---------- HAMBURGER MENU ---------- */
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', function () {
      hamburger.classList.toggle('active');
      navLinks.classList.toggle('open');
    });

    // Close menu on link click
    var links = navLinks.querySelectorAll('a');
    links.forEach(function (link) {
      link.addEventListener('click', function () {
        hamburger.classList.remove('active');
        navLinks.classList.remove('open');
      });
    });

    // Close menu on outside click
    document.addEventListener('click', function (e) {
      if (!navbar.contains(e.target)) {
        hamburger.classList.remove('active');
        navLinks.classList.remove('open');
      }
    });
  }

  /* ---------- SMOOTH SCROLL ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var href = this.getAttribute('href');
      if (href === '#') return;
      var target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        var offset = navbar.offsetHeight + 20;
        var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });

  /* ---------- SCROLL REVEAL ---------- */
  function revealOnScroll() {
    var windowHeight = window.innerHeight;
    reveals.forEach(function (el) {
      var top = el.getBoundingClientRect().top;
      var revealPoint = 100;
      if (top < windowHeight - revealPoint) {
        el.classList.add('visible');
      }
    });
  }

  window.addEventListener('scroll', function () {
    window.requestAnimationFrame(revealOnScroll);
  }, { passive: true });

  // Trigger on load
  window.addEventListener('DOMContentLoaded', function () {
    // Small delay for initial reveal so the CSS transition is visible
    setTimeout(revealOnScroll, 150);
  });

  // Also trigger immediately in case DOMContentLoaded already fired
  setTimeout(revealOnScroll, 300);

  /* ---------- BUTTON RIPPLE EFFECT ---------- */
  document.querySelectorAll('.btn').forEach(function (btn) {
    btn.addEventListener('mouseenter', function (e) {
      var rect = btn.getBoundingClientRect();
      var x = e.clientX - rect.left;
      var y = e.clientY - rect.top;
      btn.style.setProperty('--ripple-x', x + 'px');
      btn.style.setProperty('--ripple-y', y + 'px');
    });
  });

  /* ---------- COUNTER ANIMATION (Credit Score) ---------- */
  function animateCounter(element, target, duration) {
    if (!element) return;
    var start = 0;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      element.textContent = Math.floor(eased * target);
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        element.textContent = target;
      }
    }

    requestAnimationFrame(step);
  }

  // Animate scores when they become visible
  var scoreAnimated = false;
  function checkScoreAnimation() {
    if (scoreAnimated) return;
    var scoreSection = document.querySelector('.dash-score-section');
    if (!scoreSection) return;
    var rect = scoreSection.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      scoreAnimated = true;
      // Animate both score numbers
      var semiScore = document.querySelector('.gauge-semi-score .score-number');
      var circleScore = document.querySelector('.gauge-circle-score .score-number');
      animateCounter(semiScore, 742, 1800);
      animateCounter(circleScore, 730, 1800);
    }
  }

  window.addEventListener('scroll', checkScoreAnimation, { passive: true });
  setTimeout(checkScoreAnimation, 500);

  /* ---------- PARALLAX DASHBOARD ---------- */
  var dashboardWrapper = document.querySelector('.dashboard-wrapper');
  if (dashboardWrapper) {
    document.addEventListener('mousemove', function (e) {
      var rect = dashboardWrapper.getBoundingClientRect();
      // Only apply when dashboard is in viewport
      if (rect.top > window.innerHeight || rect.bottom < 0) return;

      var centerX = rect.left + rect.width / 2;
      var centerY = rect.top + rect.height / 2;
      var deltaX = (e.clientX - centerX) / rect.width;
      var deltaY = (e.clientY - centerY) / rect.height;

      // Subtle rotation based on mouse position
      var rotateY = deltaX * 4;
      var rotateX = -deltaY * 3;

      var frame = dashboardWrapper.querySelector('.dashboard-frame');
      if (frame) {
        frame.style.transform =
          'perspective(1400px) rotateY(' + rotateY + 'deg) rotateX(' + rotateX + 'deg)';
      }
    });

    // Reset on mouse leave
    document.addEventListener('mouseleave', function () {
      var frame = dashboardWrapper.querySelector('.dashboard-frame');
      if (frame) {
        frame.style.transform = '';
      }
    });
  }

})();
