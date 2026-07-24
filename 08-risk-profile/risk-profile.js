/* ===================================================
   FINORA — Page 8: Risk Assessment Result Scripts
   Gauge Animation, Theme Toggle, Reveal
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');
  const revealEls = document.querySelectorAll('.reveal');

  /* ---- THEME ---- */
  function stored() { try { return localStorage.getItem('finora-theme'); } catch(e) { return null; } }
  function setTheme(t) { html.setAttribute('data-theme', t); try { localStorage.setItem('finora-theme', t); } catch(e){} }
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

  /* ---- ANIMATED RISK GAUGE ---- */
  function animateRiskGauge() {
    const arc = document.getElementById('riskGaugeArc');
    const needle = document.getElementById('riskNeedle');
    if (!arc) return;

    const ARC_LENGTH = 314;
    // Moderate = ~50% of the arc (middle of the gauge)
    const fraction = 0.5;
    const targetDash = fraction * ARC_LENGTH;

    let frame = 0;
    const totalFrames = 70;

    function tick() {
      frame++;
      const t = frame / totalFrames;
      const eased = 1 - Math.pow(1 - t, 3);
      const progress = eased * targetDash;
      arc.setAttribute('stroke-dasharray', progress + ' ' + ARC_LENGTH);

      if (frame < totalFrames) {
        requestAnimationFrame(tick);
      } else {
        // Position needle at Moderate (~50%)
        if (needle) {
          const angle = Math.PI * (1 - fraction); // from left (π) to right (0)
          const needleLength = 80;
          const cx = 130;
          const cy = 135;
          const x2 = cx + needleLength * Math.cos(angle);
          const y2 = cy - needleLength * Math.sin(angle);
          needle.setAttribute('x2', x2);
          needle.setAttribute('y2', y2);
          needle.setAttribute('opacity', '1');
          needle.style.transition = 'all 0.5s ease';
        }
      }
    }

    requestAnimationFrame(tick);
  }

  /* ---- BOOT ---- */
  function boot() {
    animateRiskGauge();
  }

  document.addEventListener('DOMContentLoaded', boot);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(boot, 50);
  }

})();
