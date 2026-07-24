/* ===================================================
   FINORA — Page 10: Growth Simulator Scripts
   Chart.js Area Line Chart, Interactive Controls, Reveal
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');
  const revealEls = document.querySelectorAll('.reveal');

  const monthlySlider = document.getElementById('monthlySlider');
  const monthlyValText = document.getElementById('monthlyValText');
  const periodValText = document.getElementById('periodValText');
  const periodPills = document.querySelectorAll('.pill-btn');
  const scenarioTabs = document.querySelectorAll('.scenario-tab');

  const totalInvestedText = document.getElementById('totalInvestedText');
  const estReturnsText = document.getElementById('estReturnsText');
  const futureValueText = document.getElementById('futureValueText');

  let growthChart = null;

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

  /* ---- INTERACTIVE CONTROLS ---- */
  let monthlyInvestment = 2000;
  let years = 5;
  let scenario = 'moderate'; // conservative, moderate, aggressive

  function formatRupees(num) {
    return '₹' + num.toLocaleString('en-IN');
  }

  function updateCalculations() {
    const totalMonths = years * 12;
    const totalInvested = monthlyInvestment * totalMonths;

    let rate = 0.12;
    if (scenario === 'conservative') rate = 0.08;
    if (scenario === 'aggressive') rate = 0.16;

    // Monthly compounding SIP formula: FV = P * [((1 + i)^n - 1) / i] * (1 + i)
    const i = rate / 12;
    const fv = monthlyInvestment * (((Math.pow(1 + i, totalMonths) - 1) / i) * (1 + i));
    const returns = Math.max(0, fv - totalInvested);

    if (monthlyValText) monthlyValText.textContent = formatRupees(monthlyInvestment);
    if (periodValText) periodValText.textContent = years + (years === 1 ? ' Year' : ' Years');

    if (totalInvestedText) totalInvestedText.textContent = formatRupees(Math.round(totalInvested));
    if (estReturnsText) estReturnsText.textContent = formatRupees(Math.round(returns));
    if (futureValueText) futureValueText.textContent = formatRupees(Math.round(fv));

    updateChartData();
  }

  if (monthlySlider) {
    monthlySlider.addEventListener('input', e => {
      monthlyInvestment = parseInt(e.target.value, 10);
      updateCalculations();
    });
  }

  periodPills.forEach(pill => {
    pill.addEventListener('click', () => {
      periodPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      years = parseInt(pill.getAttribute('data-years'), 10);
      updateCalculations();
    });
  });

  scenarioTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      scenarioTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      scenario = tab.getAttribute('data-scenario');
      updateCalculations();
    });
  });

  /* ---- CHART.JS MULTI-LINE AREA CHART ---- */
  function initChart() {
    const ctx = document.getElementById('growthChart');
    if (!ctx) return;

    const theme = html.getAttribute('data-theme') || 'dark';
    const isDark = theme === 'dark';
    const textColor = isDark ? '#94A3B8' : '#475569';
    const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.05)';

    growthChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'],
        datasets: [
          {
            label: 'Aggressive (16%)',
            data: [26000, 56000, 92000, 136000, 188000],
            borderColor: '#A855F7',
            backgroundColor: 'rgba(168,85,247,0.08)',
            fill: true,
            tension: 0.4,
            borderWidth: 3,
            pointRadius: 4,
            pointBackgroundColor: '#A855F7'
          },
          {
            label: 'Moderate (12%)',
            data: [25500, 53000, 84000, 122000, 168000],
            borderColor: '#6366F1',
            backgroundColor: 'rgba(99,102,241,0.12)',
            fill: true,
            tension: 0.4,
            borderWidth: 3,
            pointRadius: 4,
            pointBackgroundColor: '#6366F1'
          },
          {
            label: 'Conservative (8%)',
            data: [25000, 51000, 78000, 108000, 142000],
            borderColor: '#F97316',
            backgroundColor: 'rgba(249,115,22,0.05)',
            fill: true,
            tension: 0.4,
            borderWidth: 3,
            pointRadius: 4,
            pointBackgroundColor: '#F97316'
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
            callbacks: {
              label: function (ctx) {
                return ctx.dataset.label + ': ₹' + ctx.raw.toLocaleString('en-IN');
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

  function updateChartData() {
    if (!growthChart) return;

    // Dynamically compute 5-year data points for all 3 scenarios
    const yearsArr = [1, 2, 3, 4, 5];
    const labels = yearsArr.map(y => 'Year ' + y);

    const calcDataset = (rate) => {
      const i = rate / 12;
      return yearsArr.map(yr => {
        const n = yr * 12;
        const fv = monthlyInvestment * (((Math.pow(1 + i, n) - 1) / i) * (1 + i));
        return Math.round(fv);
      });
    };

    growthChart.data.labels = labels;
    growthChart.data.datasets[0].data = calcDataset(0.16); // Aggressive
    growthChart.data.datasets[1].data = calcDataset(0.12); // Moderate
    growthChart.data.datasets[2].data = calcDataset(0.08); // Conservative
    growthChart.update();
  }

  function updateChartTheme(theme) {
    if (!growthChart) return;
    const isDark = theme === 'dark';
    const textColor = isDark ? '#94A3B8' : '#475569';
    const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.05)';

    growthChart.options.scales.x.ticks.color = textColor;
    growthChart.options.scales.y.ticks.color = textColor;
    growthChart.options.scales.y.grid.color = gridColor;
    growthChart.options.plugins.tooltip.backgroundColor = isDark ? '#0D1526' : '#FFFFFF';
    growthChart.options.plugins.tooltip.titleColor = isDark ? '#FFFFFF' : '#0F172A';
    growthChart.options.plugins.tooltip.bodyColor = isDark ? '#CBD5E1' : '#334155';
    growthChart.update();
  }

  /* ---- BOOT ---- */
  function boot() {
    initChart();
    updateCalculations();
  }

  document.addEventListener('DOMContentLoaded', boot);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(boot, 50);
  }

})();
