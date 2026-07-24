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
  const MIN_SCORE = 300;
  const MAX_SCORE = 900;
  const ARC_LENGTH = 314; // approximate circumference of semi-circle (π * r ≈ π * 100)

  function animateGauge(score, rating) {
    const arc = document.getElementById('gaugeArc');
    const dot = document.getElementById('needleDot');
    const scoreEl = document.getElementById('gaugeScore');
    const ratingEl = document.querySelector('.gauge-rating');
    const dateEl = document.querySelector('.gauge-updated');
    
    if (!arc || !scoreEl) return;
    
    if (ratingEl && rating) ratingEl.textContent = rating;

    const fraction = (score - MIN_SCORE) / (MAX_SCORE - MIN_SCORE); // 0-1
    const targetDash = fraction * ARC_LENGTH;

    // Animate counter
    let cur = 0;
    const step = Math.max(1, Math.ceil(score / 50));
    const counterTimer = setInterval(() => {
      cur += step;
      if (cur >= score) { cur = score; clearInterval(counterTimer); }
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
  function initChart(historyData) {
    const theme = html.getAttribute('data-theme') || 'dark';
    const isDark = theme === 'dark';
    const textColor = isDark ? '#94A3B8' : '#475569';
    const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.05)';

    const ctx = document.getElementById('scoreHistoryChart');
    if (!ctx) return;
    
    // Get last 7 months
    const months = [];
    const now = new Date();
    for (let i = 6; i >= 0; i--) {
        const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
        months.push(d.toLocaleString('default', { month: 'short' }));
    }

    scoreHistoryChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: months,
        datasets: [{
          label: 'Credit Score',
          data: historyData,
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
            min: Math.min(...historyData) - 20,
            max: Math.max(...historyData) + 20,
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

  /* ---- API INTEGRATION ---- */
  async function fetchCreditScoreData() {
    try {
      const response = await fetch('/api/credit-score/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      
      if (response.status === 403 || response.status === 401) {
        window.location.href = '../01-landing-page/index.html';
        return;
      }
      if (response.status === 404) {
        window.location.href = '../03-onboarding/index.html';
        return;
      }
      
      const resData = await response.json();
      if (resData.success && resData.data) {
        populateData(resData.data);
        initChart(resData.data.history);
        animateGauge(resData.data.score, resData.data.category);
        setTimeout(animateProgressBars, 600);
        setTimeout(checkReveals, 100);
      } else {
        console.error('Failed to load credit score:', resData.message);
      }
    } catch (error) {
      console.error('API Error:', error);
    }
  }

  function populateData(data) {
      // 1. Date Updated
      const dateEl = document.querySelector('.gauge-updated');
      if (dateEl) dateEl.textContent = `Updated ${data.updated_at}`;
      
      // 2. Score Factors
      const posContainer = document.querySelector('.factors-group:nth-child(2)');
      const negContainer = document.querySelector('.factors-group:nth-child(3)');
      
      if (posContainer && data.positive_factors) {
          posContainer.innerHTML = '<h4 class="factors-label positive-label">Positive Factors</h4>';
          data.positive_factors.forEach(f => {
              posContainer.innerHTML += `
              <div class="factor-item positive">
                <span class="factor-icon">✓</span>
                <div class="factor-body">
                  <span class="factor-name">${f.name}</span>
                  <span class="factor-impact badge badge--${f.badge_color}">${f.impact_text}</span>
                </div>
              </div>`;
          });
      }
      
      if (negContainer && data.negative_factors) {
          negContainer.innerHTML = '<h4 class="factors-label negative-label">Negative Factors</h4>';
          data.negative_factors.forEach(f => {
              negContainer.innerHTML += `
              <div class="factor-item negative">
                <span class="factor-icon">✗</span>
                <div class="factor-body">
                  <span class="factor-name">${f.name}</span>
                  <span class="factor-impact badge badge--${f.badge_color}">${f.impact_text}</span>
                </div>
              </div>`;
          });
      }

      // 3. Quick Insights
      const miniCards = document.querySelectorAll('.insight-mini-card .mini-val');
      if (miniCards.length >= 4) {
          miniCards[0].textContent = data.risk_level;
          miniCards[1].textContent = data.category;
          miniCards[2].textContent = data.recommendations.top_strength;
          miniCards[3].textContent = data.recommendations.improvement_opportunity;
      }
      
      // 4. Feature Importance
      const featureList = document.querySelector('.progress-list');
      if (featureList && data.feature_importance) {
          featureList.innerHTML = '';
          data.feature_importance.forEach(f => {
              featureList.innerHTML += `
              <div class="progress-item">
                <span class="prog-label">${f.label}</span>
                <div class="prog-track">
                  <div class="prog-fill prog-fill--${f.color_class}" style="--w:${f.percentage}%"></div>
                </div>
                <span class="prog-pct">${f.percentage}%</span>
              </div>`;
          });
      }

      // 5. AI Explanations
      const aiGrid = document.querySelector('.ai-grid');
      if (aiGrid && data.ai_explanations) {
          aiGrid.innerHTML = '';
          data.ai_explanations.forEach((exp, idx) => {
              let svgIcon = '';
              if (exp.icon_type === 'check') svgIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>`;
              else if (exp.icon_type === 'alert') svgIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`;
              else if (exp.icon_type === 'sparkle') svgIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 6l-9.5 9.5-5-5L1 18"/><path d="M17 6h6v6"/></svg>`;
              else if (exp.icon_type === 'shield') svgIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`;
              else if (exp.icon_type === 'trend') svgIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>`;
              else svgIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>`;
              
              const delayClass = idx > 0 ? `reveal--delay-${Math.min(idx, 3)}` : '';
              
              aiGrid.innerHTML += `
              <div class="ai-card glass-card reveal ${delayClass}">
                <div class="ai-card-icon ${exp.icon_color}-bg">${svgIcon}</div>
                <div class="ai-card-body">
                  <h4>${exp.title}</h4>
                  <p>${exp.desc}</p>
                </div>
              </div>`;
          });
      }

      // 6. Breakdown Cards
      const bdGrid = document.querySelector('.breakdown-grid');
      if (bdGrid && data.breakdown) {
          bdGrid.innerHTML = '';
          data.breakdown.forEach((bd, idx) => {
              const delayClass = idx > 0 ? `reveal--delay-${Math.min(idx, 5)}` : '';
              bdGrid.innerHTML += `
              <div class="breakdown-card glass-card reveal ${delayClass}">
                <div class="bd-icon ${bd.bg_class}">${bd.icon}</div>
                <h4 class="bd-title">${bd.title}</h4>
                <div class="bd-bar-track">
                  <div class="bd-bar-fill" style="--w:${bd.percentage}%; --c:${bd.hex_color};"></div>
                </div>
                <span class="bd-pct ${bd.text_class}">${bd.percentage}%</span>
              </div>`;
          });
      }
  }

  // Initialize
  document.addEventListener('DOMContentLoaded', fetchCreditScoreData);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(fetchCreditScoreData, 50);
  }

})();
