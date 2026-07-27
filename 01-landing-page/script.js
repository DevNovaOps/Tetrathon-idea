/* ===================================================
   FINORA — Landing Page Scripts
   Theme Toggle, ScrollSpy, Smooth Scroll, Animations
   =================================================== */

(function () {
  'use strict';

  /* ---------- DOM REFERENCES ---------- */
  var html = document.documentElement;
  var themeToggle = document.getElementById('themeToggle');
  var navbar = document.getElementById('navbar');
  var navLinks = document.querySelectorAll('.nav-links a[href^="#"]');
  var allSections = document.querySelectorAll('section[id]');
  var hamburger = document.getElementById('hamburger');
  var navLinksContainer = document.getElementById('navLinks');

  /* ---------- THEME TOGGLE ---------- */
  function getStoredTheme() {
    try { return localStorage.getItem('finora-theme'); }
    catch (e) { return null; }
  }

  function updateVideoSource(theme) {
    var video = document.getElementById('hero-landing-video');
    var source = document.getElementById('hero-landing-video-src');
    if (video && source) {
      var isDjango = source.getAttribute('data-django') === 'true';
      var basePath = isDjango ? '/static/video/' : './video/';
      var newSrc = basePath + (theme === 'light' ? 'landing_white.mp4' : 'landing_black.mp4');
      if (source.getAttribute('src') !== newSrc) {
        source.setAttribute('src', newSrc);
        video.load();
        video.play().then(function() {
          video.playbackRate = 0.9;
        }).catch(function() {});
      } else {
        video.playbackRate = 0.9;
      }
    }
  }

  // Set video playback rate to 0.90x
  var heroVideo = document.getElementById('hero-landing-video');
  if (heroVideo) {
    heroVideo.playbackRate = 0.9;
    heroVideo.addEventListener('play', function() {
      heroVideo.playbackRate = 0.9;
    });
    heroVideo.addEventListener('loadedmetadata', function() {
      heroVideo.playbackRate = 0.9;
    });
  }


  function setTheme(theme) {
    html.setAttribute('data-theme', theme);
    try { localStorage.setItem('finora-theme', theme); }
    catch (e) { /* silently fail */ }
    updateVideoSource(theme);
  }

  // Initialise theme
  (function initTheme() {
    var stored = getStoredTheme();
    setTheme(stored || 'dark');
  })();

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      var current = html.getAttribute('data-theme');
      setTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  /* ---------- STICKY NAVBAR ---------- */
  function handleScroll() {
    if (!navbar) return;
    if (window.scrollY > 40) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  /* ---------- SMOOTH SCROLL NAVIGATION ---------- */
  navLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      var targetId = this.getAttribute('href');
      var target = document.querySelector(targetId);
      if (target) {
        var offset = navbar ? navbar.offsetHeight + 10 : 80;
        var top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }

      // Close mobile menu if open
      if (navLinksContainer) {
        navLinksContainer.classList.remove('open');
      }
    });
  });

  /* ---------- SCROLLSPY: ACTIVE NAV HIGHLIGHTING ---------- */
  function updateActiveNav() {
    var scrollPos = window.scrollY + 120;

    allSections.forEach(function (section) {
      var top = section.offsetTop;
      var height = section.offsetHeight;
      var id = section.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach(function (link) {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + id) {
            link.classList.add('active');
          }
        });
      }
    });
  }

  window.addEventListener('scroll', updateActiveNav, { passive: true });
  updateActiveNav();

  /* ---------- HAMBURGER MENU ---------- */
  if (hamburger && navLinksContainer) {
    hamburger.addEventListener('click', function () {
      navLinksContainer.classList.toggle('open');
    });
  }

  /* ---------- REVEAL ON SCROLL ANIMATION ---------- */
  var reveals = document.querySelectorAll('.reveal');

  function checkReveals() {
    var windowHeight = window.innerHeight;
    reveals.forEach(function (el) {
      var top = el.getBoundingClientRect().top;
      if (top < windowHeight - 80) {
        el.classList.add('visible');
      }
    });
  }

  window.addEventListener('scroll', checkReveals, { passive: true });
  window.addEventListener('load', checkReveals);
  checkReveals();

})();
