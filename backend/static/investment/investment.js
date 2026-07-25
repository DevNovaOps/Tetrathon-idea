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
  // Need dynamic query for reveals because elements will be injected
  function getRevealEls() { return document.querySelectorAll('.reveal'); }

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
    getRevealEls().forEach(el => { if (el.getBoundingClientRect().top < trigger) el.classList.add('visible'); });
  }
  window.addEventListener('scroll', checkReveals, { passive: true });
  window.addEventListener('load', checkReveals);
  setTimeout(checkReveals, 100);

  /* ---- CHART.JS DONUT CHART ---- */
  function initDonutChart(labels, dataPoints, colors) {
    const ctx = document.getElementById('portfolioDonutChart');
    if (!ctx) return;
    
    // Destroy previous instance if it exists
    if (portfolioDonutChart) portfolioDonutChart.destroy();

    const theme = html.getAttribute('data-theme') || 'dark';
    const isDark = theme === 'dark';

    portfolioDonutChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: dataPoints,
          backgroundColor: colors,
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

  /* ---- API INTEGRATION ---- */
  async function loadInvestmentData() {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/investment/', { credentials: 'include' });
      if (!res.ok) throw new Error("Failed to load investment profile");
      const data = await res.json();
      populateUI(data);
    } catch (err) {
      console.error(err);
      // Let it fall back or show error if needed
    }
  }

  function formatMoney(amount) {
    return '₹' + amount.toLocaleString('en-IN');
  }

  function populateUI(data) {
    // 1. Top Summary Cards
    const cards = document.querySelectorAll('.summary-cards-row .sum-card-value');
    if (cards.length >= 5) {
      cards[0].innerText = formatMoney(data.target_value);
      cards[1].innerText = data.risk_bucket;
      cards[2].innerText = data.expected_cagr;
      cards[3].innerText = data.horizon_years + ' Years';
      cards[4].innerText = data.confidence_score + '%';
    }

    // 2. Allocation Grid
    const allocGrid = document.querySelector('.allocation-grid');
    if (allocGrid && data.allocation) {
      allocGrid.innerHTML = '';
      const chartLabels = [];
      const chartData = [];
      const chartColors = [];
      
      const colorMap = {
        'Index Funds': { c: 'blue', hex: '#3B82F6', icon: '📊' },
        'Debt Funds': { c: 'green', hex: '#10B981', icon: '🏦' },
        'Gold ETFs': { c: 'orange', hex: '#F97316', icon: '🪙' },
        'Liquid Funds': { c: 'cyan', hex: '#06B6D4', icon: '💧' },
        'Blue Chip Stocks': { c: 'purple', hex: '#A855F7', icon: '💎' }
      };

      data.allocation.forEach((item, idx) => {
        const style = colorMap[item.name] || { c: 'blue', hex: '#3B82F6', icon: '📈' };
        chartLabels.push(`${item.name} (${item.allocation_pct}%)`);
        chartData.push(item.allocation_pct);
        chartColors.push(style.hex);

        let riskBadgeColor = 'green';
        if (item.risk_level === 'Moderate') riskBadgeColor = 'blue';
        if (item.risk_level === 'High') riskBadgeColor = 'orange';

        allocGrid.innerHTML += `
          <div class="alloc-card glass-card reveal reveal--delay-${idx}">
            <div class="alloc-card-header">
              <div>
                <h3 class="alloc-title">${item.name}</h3>
                <span class="alloc-pct ${style.c}-text">${item.allocation_pct}%</span>
              </div>
              <div class="alloc-icon ${style.c}-bg">${style.icon}</div>
            </div>
            <div class="alloc-risk-badge"><span class="badge badge--${riskBadgeColor}">${item.risk_level} Risk</span></div>
            <div class="alloc-footer">
              <span class="alloc-lbl">Expected Return</span>
              <span class="alloc-val">${item.expected_cagr_range}</span>
            </div>
            ${item.is_highly_recommended ? '<div class="alloc-tag">⭐ Highly Recommended</div>' : ''}
          </div>
        `;
      });
      initDonutChart(chartLabels, chartData, chartColors);
    }

    // 3. AI Recommendations
    const recList = document.querySelector('.rec-list');
    if (recList && data.ai_recommendations) {
      recList.innerHTML = '';
      data.ai_recommendations.forEach(rec => {
        recList.innerHTML += `
          <div class="rec-item">
            <div class="rec-icon-circle ${rec.color_theme}-bg">✓</div>
            <div class="rec-text-wrap">
              <h4>${rec.action}</h4>
              <p>${rec.reason}</p>
            </div>
          </div>
        `;
      });
    }

    // 4. Key Benefits
    const benGrid = document.querySelector('.benefits-grid');
    if (benGrid && data.portfolio_benefits) {
      benGrid.innerHTML = '';
      data.portfolio_benefits.forEach((ben, idx) => {
        benGrid.innerHTML += `
          <div class="benefit-card glass-card reveal reveal--delay-${idx}">
            <div class="benefit-emoji ${ben.color_theme}-bg">${ben.emoji}</div>
            <h4 class="benefit-title">${ben.title}</h4>
            <p class="benefit-desc">${ben.description}</p>
          </div>
        `;
      });
    }

    // 5. Timeline Journey
    const timeline = document.querySelector('.journey-timeline-row');
    if (timeline) {
      timeline.innerHTML = `
        <div class="j-step"><span class="j-icon">📍</span><span class="j-name">Today</span><span class="j-sub">Profile Verified</span></div>
        <div class="j-arrow">➔</div>
        <div class="j-step"><span class="j-icon">💳</span><span class="j-name">Monthly SIP</span><span class="j-sub">${formatMoney(data.monthly_sip)} / month</span></div>
        <div class="j-arrow">➔</div>
        <div class="j-step"><span class="j-icon">📈</span><span class="j-name">Compound Growth</span><span class="j-sub">${data.expected_cagr} CAGR</span></div>
        <div class="j-arrow">➔</div>
        <div class="j-step"><span class="j-icon">🏆</span><span class="j-name">Goal Achievement</span><span class="j-sub">${formatMoney(data.target_value)} Target</span></div>
      `;
    }

    // Educational Disclaimer
    if (data.educational_disclaimer) {
      const footer = document.querySelector('.timeline-cta-section');
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

  /* ---- BOOT ---- */
  function boot() {
    loadInvestmentData();
  }

  document.addEventListener('DOMContentLoaded', boot);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(boot, 50);
  }

})();
