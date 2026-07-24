/* ===================================================
   FINORA — Page 9: Investment Recommendation Scripts
   Chart.js Donut, Theme Persistence, Reveal
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');
  const revealEls = document.querySelectorAll('.reveal');

  let portfolioDonutChart = null;

  /* ---- THEME PERSISTENCE ---- */
  function stored() { try { return localStorage.getItem('finora-theme'); } catch(e) { return null; } }
  function setTheme(t) {
    html.setAttribute('data-theme', t);
    try { localStorage.setItem('finora-theme', t); } catch(e){}
    updateChartTheme(t);
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

  /* ---- CHART.JS DONUT CHART ---- */
  function initDonutChart() {
    const ctx = document.getElementById('portfolioDonutChart');
    if (!ctx) return;

    const theme = html.getAttribute('data-theme') || 'dark';
    const isDark = theme === 'dark';

    portfolioDonutChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Index Fund (40%)', 'Debt Fund (20%)', 'Gold ETF (20%)', 'Liquid Fund (10%)', 'Blue Chip Stocks (10%)'],
        datasets: [{
          data: [40, 20, 20, 10, 10],
          backgroundColor: [
            '#3B82F6', // Index Fund (Blue)
            '#10B981', // Debt Fund (Green)
            '#F97316', // Gold ETF (Orange)
            '#06B6D4', // Liquid Fund (Cyan)
            '#A855F7'  // Blue Chip (Purple)
          ],
          borderColor: isDark ? '#0D1526' : '#FFFFFF',
          borderWidth: 3,
          hoverOffset: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: isDark ? '#CBD5E1' : '#334155',
              font: { family: 'Inter', size: 11, weight: '600' },
              padding: 12,
              usePointStyle: true,
              pointStyle: 'circle'
            }
          },
          tooltip: {
            backgroundColor: isDark ? '#0D1526' : '#FFFFFF',
            titleColor: isDark ? '#FFFFFF' : '#0F172A',
            bodyColor: isDark ? '#CBD5E1' : '#334155',
            borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
            borderWidth: 1,
            padding: 12
          }
        }
      }
    });
  }

  function updateChartTheme(theme) {
    if (!portfolioDonutChart) return;
    const isDark = theme === 'dark';
    portfolioDonutChart.data.datasets[0].borderColor = isDark ? '#0D1526' : '#FFFFFF';
    portfolioDonutChart.options.plugins.legend.labels.color = isDark ? '#CBD5E1' : '#334155';
    portfolioDonutChart.options.plugins.tooltip.backgroundColor = isDark ? '#0D1526' : '#FFFFFF';
    portfolioDonutChart.options.plugins.tooltip.titleColor = isDark ? '#FFFFFF' : '#0F172A';
    portfolioDonutChart.options.plugins.tooltip.bodyColor = isDark ? '#CBD5E1' : '#334155';
    portfolioDonutChart.update();
  }

  /* ---- BOOT ---- */
  function boot() {
    initDonutChart();
  }

  document.addEventListener('DOMContentLoaded', boot);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(boot, 50);
  }

})();
