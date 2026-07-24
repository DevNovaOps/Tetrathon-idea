/* ===================================================
   FINORA — Page 4: AI Financial Dashboard Scripts
   Theme Persistence, Chart.js Initialization, Counter & Reveal
   =================================================== */

(function () {
  'use strict';

  /* ---------- DOM REFERENCES ---------- */
  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');
  const navLinks = document.querySelectorAll('.nav-link');
  const countUpElements = document.querySelectorAll('.count-up');
  const revealElements = document.querySelectorAll('.reveal');

  /* ---------- CHART INSTANCE REFERENCES ---------- */
  let incomeExpenseChartInstance = null;
  let spendingDonutChartInstance = null;

  /* ---------- THEME PERSISTENCE ---------- */
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
      // ignore
    }
    // Re-render chart colors if charts exist
    if (typeof updateChartThemeColors === 'function') {
      updateChartThemeColors(theme);
    }
  }

  (function initTheme() {
    const stored = getStoredTheme();
    setTheme(stored || 'dark');
  })();

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      setTheme(next);
    });
  }

  /* ---------- MOBILE SIDEBAR TOGGLE ---------- */
  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', function (e) {
      e.stopPropagation();
      sidebar.classList.toggle('open');
    });

    document.addEventListener('click', function (e) {
      if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== mobileToggle) {
        sidebar.classList.remove('open');
      }
    });
  }

  /* ---------- SIDEBAR NAVIGATION ACTIVE STATE ---------- */
  navLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      navLinks.forEach(l => l.classList.remove('active'));
      this.classList.add('active');
      if (window.innerWidth <= 900 && sidebar) {
        sidebar.classList.remove('open');
      }
    });
  });

  /* ---------- COUNTER ANIMATION ---------- */
  function animateCounters() {
    countUpElements.forEach(function (el) {
      const target = parseInt(el.getAttribute('data-target'), 10);
      if (isNaN(target) || el.classList.contains('animated')) return;

      el.classList.add('animated');
      let current = 0;
      const step = Math.max(1, Math.ceil(target / 45));
      const timer = setInterval(function () {
        current += step;
        if (current >= target) {
          current = target;
          clearInterval(timer);
        }
        el.textContent = current.toLocaleString();
      }, 25);
    });
  }

  /* ---------- REVEAL ANIMATION ---------- */
  function checkReveals() {
    const triggerBottom = window.innerHeight * 0.9;
    revealElements.forEach(function (el) {
      const top = el.getBoundingClientRect().top;
      if (top < triggerBottom) {
        el.classList.add('visible');
      }
    });
    animateCounters();
  }

  window.addEventListener('scroll', checkReveals, { passive: true });
  window.addEventListener('load', checkReveals);
  setTimeout(checkReveals, 100);

  /* ---------- CHART.JS INITIALIZATION ---------- */

  function initCharts() {
    const theme = html.getAttribute('data-theme') || 'dark';
    const isDark = theme === 'dark';
    const textColor = isDark ? '#94A3B8' : '#475569';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.05)';

    // 1. Income vs Expense Dual Bar Chart
    const ctxBar = document.getElementById('incomeExpenseChart');
    if (ctxBar) {
      incomeExpenseChartInstance = new Chart(ctxBar, {
        type: 'bar',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
          datasets: [
            {
              label: 'Income',
              data: [65000, 72000, 68000, 80000, 85000, 82000, 88000],
              backgroundColor: '#3B82F6',
              borderRadius: 6,
              barPercentage: 0.6,
              categoryPercentage: 0.6
            },
            {
              label: 'Expense',
              data: [28000, 31000, 29000, 34000, 32400, 35000, 33000],
              backgroundColor: '#A855F7',
              borderRadius: 6,
              barPercentage: 0.6,
              categoryPercentage: 0.6
            }
          ]
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
              padding: 12,
              displayColors: true,
              callbacks: {
                label: function (context) {
                  return context.dataset.label + ': ₹' + context.raw.toLocaleString();
                }
              }
            }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: { color: textColor, font: { family: 'Inter', size: 12 } }
            },
            y: {
              grid: { color: gridColor },
              ticks: {
                color: textColor,
                font: { family: 'Inter', size: 11 },
                callback: function (val) {
                  return '₹' + (val / 1000) + 'k';
                }
              }
            }
          }
        }
      });
    }

    // 2. Spending Categories Donut Chart
    const ctxDonut = document.getElementById('spendingDonutChart');
    if (ctxDonut) {
      spendingDonutChartInstance = new Chart(ctxDonut, {
        type: 'doughnut',
        data: {
          labels: ['Housing', 'Food', 'Transport', 'Entertainment', 'Others'],
          datasets: [{
            data: [40, 20, 15, 15, 10],
            backgroundColor: [
              '#3B82F6', // Housing - Blue
              '#F97316', // Food - Orange
              '#10B981', // Transport - Green
              '#A855F7', // Entertainment - Purple
              '#06B6D4'  // Others - Cyan
            ],
            borderWidth: 3,
            borderColor: isDark ? '#0F172A' : '#FFFFFF',
            hoverOffset: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '76%',
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: isDark ? '#0D1526' : '#FFFFFF',
              titleColor: isDark ? '#FFFFFF' : '#0F172A',
              bodyColor: isDark ? '#CBD5E1' : '#334155',
              borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
              borderWidth: 1,
              padding: 10,
              callbacks: {
                label: function (context) {
                  return context.label + ': ' + context.raw + '%';
                }
              }
            }
          }
        }
      });
    }
  }

  function updateChartThemeColors(theme) {
    const isDark = theme === 'dark';
    const textColor = isDark ? '#94A3B8' : '#475569';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.05)';

    if (incomeExpenseChartInstance) {
      incomeExpenseChartInstance.options.scales.x.ticks.color = textColor;
      incomeExpenseChartInstance.options.scales.y.ticks.color = textColor;
      incomeExpenseChartInstance.options.scales.y.grid.color = gridColor;
      incomeExpenseChartInstance.options.plugins.tooltip.backgroundColor = isDark ? '#0D1526' : '#FFFFFF';
      incomeExpenseChartInstance.options.plugins.tooltip.titleColor = isDark ? '#FFFFFF' : '#0F172A';
      incomeExpenseChartInstance.options.plugins.tooltip.bodyColor = isDark ? '#CBD5E1' : '#334155';
      incomeExpenseChartInstance.update();
    }

    if (spendingDonutChartInstance) {
      spendingDonutChartInstance.data.datasets[0].borderColor = isDark ? '#0F172A' : '#FFFFFF';
      spendingDonutChartInstance.options.plugins.tooltip.backgroundColor = isDark ? '#0D1526' : '#FFFFFF';
      spendingDonutChartInstance.options.plugins.tooltip.titleColor = isDark ? '#FFFFFF' : '#0F172A';
      spendingDonutChartInstance.options.plugins.tooltip.bodyColor = isDark ? '#CBD5E1' : '#334155';
      spendingDonutChartInstance.update();
    }
  }

  // Initialize charts after DOM ready
  document.addEventListener('DOMContentLoaded', initCharts);

  // If DOM is already loaded
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(initCharts, 50);
  }

})();
