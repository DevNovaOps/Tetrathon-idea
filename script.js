/* ===================================================
   FINORA — Landing Page Scripts
   Theme Toggle, Active ScrollSpy Navigation, Smooth Scroll
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
  const sections = document.querySelectorAll('section[id]');
  const navItems = document.querySelectorAll('.nav-links a[href^="#"]');

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

  /* ---------- STICKY NAVBAR ---------- */
  function handleNavbarScroll() {
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;
    if (scrollY > 20) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }

  /* ---------- ACTIVE SCROLLSPY NAVIGATION ---------- */
  function handleScrollSpy() {
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;
    var navHeight = navbar ? navbar.offsetHeight : 70;

    sections.forEach(function (current) {
      var sectionHeight = current.offsetHeight;
      var sectionTop = current.offsetTop - navHeight - 60;
      var sectionId = current.getAttribute('id');

      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        navItems.forEach(function (item) {
          item.classList.remove('active');
          if (item.getAttribute('href') === '#' + sectionId) {
            item.classList.add('active');
          }
        });
      }
    });
  }

  /* Combined scroll handler */
  function onScroll() {
    handleNavbarScroll();
    handleScrollSpy();
    revealOnScroll();
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- SMOOTH SCROLLING FOR ALL NAV LINKS ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var href = this.getAttribute('href');
      if (!href || href === '#') return;

      var target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        var navHeight = navbar ? navbar.offsetHeight : 70;
        var targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight + 5;

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });

        // Close mobile nav if open
        if (hamburger && navLinks) {
          hamburger.classList.remove('active');
          navLinks.classList.remove('open');
        }
      }
    });
  });

  /* ---------- HAMBURGER MENU ---------- */
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', function () {
      hamburger.classList.toggle('active');
      navLinks.classList.toggle('open');
    });
  }

  /* ---------- SCROLL REVEAL ANIMATIONS ---------- */
  function revealOnScroll() {
    var windowHeight = window.innerHeight;
    reveals.forEach(function (el) {
      var top = el.getBoundingClientRect().top;
      if (top < windowHeight - 60) {
        el.classList.add('visible');
      }
    });
  }

  setTimeout(revealOnScroll, 100);

  /* ---------- CREDIT SCORE COUNTER ANIMATION ---------- */
  var animatedCounter = false;
  function checkGaugeCounter() {
    if (animatedCounter) return;
    var gaugeScore = document.querySelector('.gauge-score');
    if (!gaugeScore) return;

    var rect = gaugeScore.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      animatedCounter = true;
      var start = 0;
      var target = 730;
      var duration = 1400;
      var startTime = null;

      function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        gaugeScore.textContent = Math.floor(eased * target);
        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          gaugeScore.textContent = target;
        }
      }

      requestAnimationFrame(step);
    }
  }

  window.addEventListener('scroll', checkGaugeCounter, { passive: true });
  setTimeout(checkGaugeCounter, 300);

})();
