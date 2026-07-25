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
  function getRevealEls() { return document.querySelectorAll('.reveal'); }

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
    getRevealEls().forEach(el => { if (el.getBoundingClientRect().top < trigger) el.classList.add('visible'); });
  }
  window.addEventListener('scroll', checkReveals, { passive: true });
  window.addEventListener('load', checkReveals);
  setTimeout(checkReveals, 100);

  /* ---- INTERACTIVE CONTROLS & API ---- */
  let monthlyInvestment = null;
  let years = null;
  let scenario = null; // conservative, moderate, aggressive

  let debounceTimer = null;
  let currentAbortController = null;

  function formatRupees(num) {
    return '₹' + num.toLocaleString('en-IN');
  }

  async function fetchSimulationData() {
    // Abort previous request to prevent race conditions
    if (currentAbortController) {
      currentAbortController.abort();
    }
    currentAbortController = new AbortController();

    try {
      // Build query string based on current user selections
      const params = new URLSearchParams();
      if (monthlyInvestment) params.append('sip', monthlyInvestment);
      if (years) params.append('years', years);
      if (scenario) params.append('scenario', scenario);

      const url = `http://127.0.0.1:8000/api/simulator/project/?${params.toString()}`;
      
      const res = await fetch(url, {
        credentials: 'include',
        signal: currentAbortController.signal
      });

      if (!res.ok) throw new Error("Failed to fetch simulator data");
      const data = await res.json();
      populateUI(data);

    } catch (err) {
      if (err.name === 'AbortError') {
        console.log("Fetch aborted due to newer request");
      } else {
        console.error(err);
      }
    }
  }

  function triggerUpdate() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      fetchSimulationData();
    }, 300); // 300ms debounce
  }

  if (monthlySlider) {
    monthlySlider.addEventListener('input', e => {
      monthlyInvestment = parseInt(e.target.value, 10);
      if (monthlyValText) monthlyValText.textContent = formatRupees(monthlyInvestment);
      triggerUpdate();
    });
  }

  periodPills.forEach(pill => {
    pill.addEventListener('click', () => {
      periodPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      years = parseInt(pill.getAttribute('data-years'), 10);
      triggerUpdate();
    });
  });

  scenarioTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      scenarioTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      scenario = tab.getAttribute('data-scenario');
      triggerUpdate();
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

  function populateUI(data) {
    // Initialize component state variables to backend defaults if null
    monthlyInvestment = data.summary_metrics.monthly_sip;
    years = data.summary_metrics.horizon_years;
    scenario = data.active_scenario;

    // 1. Controls
    if (monthlySlider) monthlySlider.value = monthlyInvestment;
    if (monthlyValText) monthlyValText.textContent = formatRupees(monthlyInvestment);
    if (periodValText) periodValText.textContent = years + (years === 1 ? ' Year' : ' Years');

    // Expected Return Display
    const exReturn = document.querySelector('.strategy-info-row .ctrl-val-med.green-text');
    if (exReturn) exReturn.textContent = data.summary_metrics.expected_cagr + " p.a.";
    
    // Sync Scenario Tabs
    scenarioTabs.forEach(t => {
      if(t.getAttribute('data-scenario') === scenario) t.classList.add('active');
      else t.classList.remove('active');
    });

    // Sync Pills
    periodPills.forEach(p => {
      if(parseInt(p.getAttribute('data-years'), 10) === years) p.classList.add('active');
      else p.classList.remove('active');
    });

    // 2. Summary Metrics
    if (totalInvestedText) totalInvestedText.textContent = formatRupees(data.summary_metrics.total_invested);
    if (estReturnsText) estReturnsText.textContent = formatRupees(data.summary_metrics.estimated_returns);
    if (futureValueText) futureValueText.textContent = formatRupees(data.summary_metrics.future_value);

    // 3. Scenario Cards
    const scenGrid = document.querySelector('.scenario-grid');
    if (scenGrid && data.scenarios) {
      scenGrid.innerHTML = '';
      data.scenarios.forEach((scen, idx) => {
        const isActive = scen.id === scenario ? 'active-scen-card' : '';
        scenGrid.innerHTML += `
          <div class="scen-card glass-card ${isActive} reveal reveal--delay-${idx}">
            <div class="scen-header">
              <span class="scen-icon ${scen.color}-bg">${scen.icon}</span>
              <span class="badge badge--${scen.color}">${scen.cagr}% Returns</span>
            </div>
            <h3 class="scen-title">${scen.name}</h3>
            <p class="scen-desc">${scen.desc}</p>
            <div class="scen-value-wrap">
              <span class="scen-lbl">${years}-Year Portfolio</span>
              <span class="scen-val ${scen.color}-text">${formatRupees(scen.future_value)}</span>
            </div>
          </div>
        `;
      });
    }

    // 4. Update Chart.js Data
    if (growthChart && data.chart_data) {
      growthChart.data.labels = data.chart_data.labels;
      
      const theme = html.getAttribute('data-theme') || 'dark';
      const isDark = theme === 'dark';

      // Rebuild datasets
      const colors = {
        'aggressive': { border: '#A855F7', bg: 'rgba(168,85,247,0.08)' },
        'moderate': { border: '#6366F1', bg: 'rgba(99,102,241,0.12)' },
        'conservative': { border: '#F97316', bg: 'rgba(249,115,22,0.05)' }
      };

      growthChart.data.datasets = data.chart_data.datasets.map(ds => {
        const c = colors[ds.id] || colors['moderate'];
        return {
          label: ds.label,
          data: ds.data,
          borderColor: c.border,
          backgroundColor: c.bg,
          fill: true,
          tension: 0.4,
          borderWidth: 3,
          pointRadius: 4,
          pointBackgroundColor: c.border
        };
      });
      growthChart.update();
    }

    // 5. Goal Tracker
    const goalBox = document.querySelector('.goal-box');
    if (goalBox && data.goal_tracker) {
      const g = data.goal_tracker;
      const statusBadge = document.querySelector('.insights-goal-grid .badge');
      if (statusBadge) {
        statusBadge.textContent = g.status;
        statusBadge.className = 'badge ' + (g.progress_pct >= 100 ? 'badge--green' : (g.progress_pct >= 80 ? 'badge--blue' : 'badge--orange'));
      }

      goalBox.innerHTML = `
        <div class="goal-header">
          <span class="goal-emoji">🏠</span>
          <div>
            <h4 class="goal-name">${g.name}</h4>
            <span class="goal-target">Target: ${formatRupees(g.target)}</span>
          </div>
        </div>
        <div class="goal-progress-wrap">
          <div class="goal-progress-labels">
            <span>Current: ${formatRupees(g.current)}</span>
            <span class="green-text">${g.progress_pct}% Progress</span>
          </div>
          <div class="goal-track">
            <div class="goal-fill" style="width: ${Math.min(100, g.progress_pct)}%;"></div>
          </div>
        </div>
        <div class="goal-footer">
          <span class="goal-time-tag">⏱️ Estimated Completion: <strong>${g.estimated_completion}</strong></span>
          <span class="goal-status-tag">Status: <strong>${g.status}</strong></span>
        </div>
      `;
    }

    // 6. AI Insights
    const insList = document.querySelector('.sim-insights-list');
    if (insList && data.ai_insights) {
      insList.innerHTML = '';
      data.ai_insights.forEach(ins => {
        insList.innerHTML += `
          <div class="sim-ins-item">
            <span class="sim-ins-icon ${ins.color}-bg">${ins.icon}</span>
            <div class="sim-ins-text">
              <h4>${ins.title}</h4>
              <p>${ins.desc}</p>
            </div>
          </div>
        `;
      });
    }

    // 7. Timeline Journey
    const timeline = document.querySelector('.journey-timeline-row');
    if (timeline && data.timeline) {
      let timelineHTML = '';
      data.timeline.forEach((step, idx) => {
        timelineHTML += `
          <div class="j-step">
            <span class="j-icon">${step.icon}</span>
            <span class="j-name">${step.name}</span>
            <span class="j-sub">${step.sub}</span>
          </div>
        `;
        if (idx < data.timeline.length - 1) {
          timelineHTML += `<div class="j-arrow">➔</div>`;
        }
      });
      timeline.innerHTML = timelineHTML;
    }

    // Educational Disclaimer
    if (data.educational_disclaimer) {
      const footer = document.querySelector('.compound-timeline-section');
      if (footer) {
        let disc = document.getElementById('apiDisclaimer');
        if (!disc) {
          disc = document.createElement('p');
          disc.id = 'apiDisclaimer';
          disc.style = 'text-align: center; font-size: 0.8rem; opacity: 0.6; margin-top: 2rem; width: 100%;';
          footer.parentElement.appendChild(disc);
        }
        disc.innerText = data.educational_disclaimer;
      }
    }

    checkReveals();
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
    fetchSimulationData(); // Replaces updateCalculations
  }

  document.addEventListener('DOMContentLoaded', boot);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(boot, 50);
  }

})();
