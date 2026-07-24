/* ===================================================
   FINORA — Page 5: Credit Score Scripts
   Gauge, Chart.js, Progress Bar, Theme, Reveal
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');
  const revealEls = document.querySelectorAll('.reveal');

  let scoreHistoryChart = null;

  /* ---- THEME ---- */
  function stored() { try { return localStorage.getItem('finora-theme'); } catch(e) { return null; } }
  function setTheme(t) {
    html.setAttribute('data-theme', t);
    try { localStorage.setItem('finora-theme', t); } catch(e){}
    updateChartColors(t);
  }
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

  /* ---- ANIMATED GAUGE ---- */
  const SCORE = 730;
  const MIN_SCORE = 300;
  const MAX_SCORE = 900;
  const ARC_LENGTH = 314; // approximate circumference of semi-circle (π * r ≈ π * 100)

  function animateGauge() {
    const arc = document.getElementById('gaugeArc');
    const dot = document.getElementById('needleDot');
    const scoreEl = document.getElementById('gaugeScore');
    if (!arc || !scoreEl) return;

    const fraction = (SCORE - MIN_SCORE) / (MAX_SCORE - MIN_SCORE); // 0-1
    const targetDash = fraction * ARC_LENGTH;

    // Animate counter
    let cur = 0;
    const step = Math.max(1, Math.ceil(SCORE / 50));
    const counterTimer = setInterval(() => {
      cur += step;
      if (cur >= SCORE) { cur = SCORE; clearInterval(counterTimer); }
      scoreEl.textContent = cur;
    }, 22);

    // Animate arc via CSS transition equivalent
    let progress = 0;
    const frames = 60;
    let frame = 0;
    function tick() {
      frame++;
      const t = frame / frames;
      const eased = 1 - Math.pow(1 - t, 3); // ease-out cubic
      progress = eased * targetDash;
      arc.setAttribute('stroke-dasharray', progress + ' ' + ARC_LENGTH);

      // Move needle dot along the arc
      if (dot) {
        const angle = Math.PI + (eased * fraction * Math.PI * 0); // we'll use a simpler approach
        // Semi-circle from left (π) to right (0)
        const a = Math.PI - eased * fraction * 0; // placeholder
        dot.setAttribute('opacity', '1');
      }

      if (frame < frames) requestAnimationFrame(tick);
    }

    // Actually position the dot at final position
    setTimeout(() => {
      const finalAngle = Math.PI * (1 - fraction);
      const cx = 130 + 100 * Math.cos(finalAngle);
      const cy = 130 - 100 * Math.sin(finalAngle);
      if (dot) {
        dot.setAttribute('cx', cx);
        dot.setAttribute('cy', cy);
        dot.setAttribute('opacity', '1');
      }
    }, 1200);

    requestAnimationFrame(tick);
  }

  /* ---- PROGRESS BARS ANIMATION ---- */
  function animateProgressBars() {
    document.querySelectorAll('.prog-fill, .bd-bar-fill').forEach(el => {
      if (el.getBoundingClientRect().top < window.innerHeight && !el.classList.contains('animated')) {
        el.classList.add('animated');
      }
    });
  }
  window.addEventListener('scroll', animateProgressBars, { passive: true });

  /* ---- CHART: Score History ---- */
  function initChart() {
    const theme = html.getAttribute('data-theme') || 'dark';
    const isDark = theme === 'dark';
    const textColor = isDark ? '#94A3B8' : '#475569';
    const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.05)';

    const ctx = document.getElementById('scoreHistoryChart');
    if (!ctx) return;

    scoreHistoryChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [{
          label: 'Credit Score',
          data: [695, 702, 698, 710, 718, 725, 730],
          borderColor: '#6366F1',
          backgroundColor: function(context) {
            const chart = context.chart;
            const { ctx: c, chartArea } = chart;
            if (!chartArea) return 'transparent';
            const grad = c.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
            grad.addColorStop(0, isDark ? 'rgba(99,102,241,0.3)' : 'rgba(99,102,241,0.15)');
            grad.addColorStop(1, 'rgba(99,102,241,0)');
            return grad;
          },
          fill: true,
          tension: 0.4,
          borderWidth: 3,
          pointRadius: 4,
          pointHoverRadius: 7,
          pointBackgroundColor: '#6366F1',
          pointBorderColor: isDark ? '#0F172A' : '#FFFFFF',
          pointBorderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: isDark ? '#0D1526' : '#FFFFFF',
            titleColor: isDark ? '#FFFFFF' : '#0F172A',
            bodyColor: isDark ? '#CBD5E1' : '#334155',
            borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
            borderWidth: 1,
            padding: 12
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: textColor, font: { family: 'Inter', size: 12 } }
          },
          y: {
            min: 680,
            max: 740,
            grid: { color: gridColor },
            ticks: {
              color: textColor,
              font: { family: 'Inter', size: 11 },
              stepSize: 10
            }
          }
        }
      }
    });
  }

  function updateChartColors(theme) {
    if (!scoreHistoryChart) return;
    const isDark = theme === 'dark';
    const textColor = isDark ? '#94A3B8' : '#475569';
    const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.05)';
    scoreHistoryChart.options.scales.x.ticks.color = textColor;
    scoreHistoryChart.options.scales.y.ticks.color = textColor;
    scoreHistoryChart.options.scales.y.grid.color = gridColor;
    scoreHistoryChart.options.plugins.tooltip.backgroundColor = isDark ? '#0D1526' : '#FFFFFF';
    scoreHistoryChart.options.plugins.tooltip.titleColor = isDark ? '#FFFFFF' : '#0F172A';
    scoreHistoryChart.options.plugins.tooltip.bodyColor = isDark ? '#CBD5E1' : '#334155';
    scoreHistoryChart.data.datasets[0].pointBorderColor = isDark ? '#0F172A' : '#FFFFFF';
    scoreHistoryChart.update();
  }

  /* ---- BOOT ---- */
  function boot() {
    initChart();
    animateGauge();
    setTimeout(animateProgressBars, 600);
  }

  document.addEventListener('DOMContentLoaded', boot);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(boot, 50);
  }

})();
