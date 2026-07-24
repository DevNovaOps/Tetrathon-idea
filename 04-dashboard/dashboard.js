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

  function initCharts(chartData) {
    const theme = html.getAttribute('data-theme') || 'dark';
    const isDark = theme === 'dark';
    const textColor = isDark ? '#94A3B8' : '#475569';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.05)';

    const ctxBar = document.getElementById('incomeExpenseChart');
    if (ctxBar && chartData?.income_vs_expense) {
      const data = chartData.income_vs_expense;
      incomeExpenseChartInstance = new Chart(ctxBar, {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: [
            {
              label: 'Income',
              data: data.datasets[0].data,
              backgroundColor: data.datasets[0].backgroundColor,
              borderRadius: 6,
              barPercentage: 0.6,
              categoryPercentage: 0.6
            },
            {
              label: 'Expense',
              data: data.datasets[1].data,
              backgroundColor: data.datasets[1].backgroundColor,
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
    if (ctxDonut && chartData?.spending_categories) {
      const dData = chartData.spending_categories;
      
      // Update the center label text in HTML if it exists
      const centerVal = document.querySelector('.donut-center-val');
      if (centerVal) centerVal.textContent = dData.total_spent;

      spendingDonutChartInstance = new Chart(ctxDonut, {
        type: 'doughnut',
        data: {
          labels: dData.labels,
          datasets: [{
            data: dData.datasets[0].data,
            backgroundColor: dData.datasets[0].backgroundColor,
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

  /* ---------- DATA FETCHING & BINDING ---------- */
  async function fetchDashboardData() {
    try {
      const response = await fetch('/api/dashboard/', {
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
        populateDashboard(resData.data);
        initCharts(resData.data.charts);
        // Delay reveals slightly to allow DOM to update
        setTimeout(checkReveals, 100);
      } else {
        console.error('Failed to load dashboard data:', resData.message);
      }
    } catch (error) {
      console.error('API Error:', error);
    }
  }

  function populateDashboard(data) {
    // Top Nav / Sidebar
    const elSidebarAvatar = document.getElementById('sidebar-user-avatar');
    const elSidebarName = document.getElementById('sidebar-user-name');
    const elSidebarTier = document.getElementById('sidebar-user-tier');
    const elWelcomeTitle = document.getElementById('welcome-title');
    const elTopAvatar = document.getElementById('top-nav-avatar');
    const elTopUsername = document.getElementById('top-nav-username');

    if (elSidebarAvatar) elSidebarAvatar.innerHTML = `<span>${data.user.initials}</span>`;
    if (elSidebarName) elSidebarName.textContent = data.user.full_name;
    if (elSidebarTier) elSidebarTier.textContent = `Member since ${data.user.member_since}`;
    const welcome = document.querySelector('.welcome-title');
    if (welcome) welcome.textContent = `Welcome back, ${data.user.full_name} 👋`;
    if (elTopAvatar) elTopAvatar.innerHTML = `<span>${data.user.initials}</span>`;
    if (elTopUsername) elTopUsername.textContent = data.user.full_name;

    // Stat Cards
    const safeSetText = (id, text) => {
      const el = document.getElementById(id);
      if (el) el.textContent = text;
    };
    
    // Set counter targets instead of text content so the animation runs
    const safeSetTarget = (id, target) => {
      const el = document.getElementById(id);
      if (el) {
        el.setAttribute('data-target', target);
        el.textContent = '0'; // reset for animation
        el.classList.remove('animated'); // reset animation flag
      }
    };

    safeSetTarget('val-health-score', data.analytics.financial_health_score);
    safeSetText('val-risk-profile', data.financial_summary.risk_preference);
    safeSetText('val-monthly-investment', data.financial_summary.investment_budget);
    safeSetText('val-cash-flow', data.analytics.monthly_cash_flow);
    safeSetTarget('val-savings-rate', data.analytics.savings_rate);

    // Summary Widgets
    safeSetText('val-total-savings', data.financial_summary.savings);
    safeSetText('val-monthly-income', data.financial_summary.monthly_income);
    safeSetText('val-monthly-expenses', data.financial_summary.monthly_expenses);
    safeSetText('val-expense-ratio', `${data.analytics.expense_ratio}%`);
    safeSetText('val-profile-completion', `${data.profile.completion}%`);
    safeSetText('val-emergency-fund', data.financial_summary.emergency_fund);

    // Insights
    const insightsContainer = document.getElementById('insights-container');
    if (insightsContainer && data.insights) {
      insightsContainer.innerHTML = '';
      data.insights.forEach((insight, index) => {
        let svgIcon = '';
        if (insight.icon === 'sparkle') {
          svgIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 6l-9.5 9.5-5-5L1 18"/><path d="M17 6h6v6"/></svg>`;
        } else if (insight.icon === 'alert') {
          svgIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`;
        } else if (insight.icon === 'shield') {
          svgIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`;
        } else if (insight.icon === 'check') {
          svgIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>`;
        } else {
          svgIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>`;
        }
        
        let colorClass = insight.badge_color === 'green' ? 'emerald-bg' : insight.badge_color === 'orange' ? 'orange-bg' : insight.badge_color === 'purple' ? 'purple-bg' : insight.badge_color === 'cyan' ? 'cyan-bg' : 'blue-bg';

        insightsContainer.innerHTML += `
          <div class="insight-card reveal ${index > 0 ? 'reveal--delay-' + Math.min(index, 3) : ''}">
            <div class="insight-icon-box ${colorClass}">
              ${svgIcon}
            </div>
            <div class="insight-body">
              <div class="insight-header">
                <h4 class="insight-title">${insight.title}</h4>
                <span class="badge badge--${insight.badge_color}">${insight.badge_text}</span>
              </div>
              <p class="insight-desc">${insight.desc}</p>
            </div>
          </div>
        `;
      });
    }

    // Quick Actions
    const actionsContainer = document.getElementById('quick-actions-container');
    if (actionsContainer && data.quick_actions) {
      actionsContainer.innerHTML = '';
      data.quick_actions.forEach(action => {
        actionsContainer.innerHTML += `
          <div class="action-btn-card" onclick="window.location.href='${action.link}'" style="cursor: pointer;">
            <div class="action-icon-box ${action.icon_bg}">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            </div>
            <div class="action-text">
              <span class="action-name">${action.name}</span>
              <span class="action-sub">${action.sub}</span>
            </div>
            <span class="action-arrow">→</span>
          </div>
        `;
      });
    }

    // Activity Timeline
    const activityContainer = document.getElementById('activity-container');
    if (activityContainer && data.activities) {
      activityContainer.innerHTML = '';
      data.activities.forEach(act => {
        activityContainer.innerHTML += `
          <div class="activity-item">
            <div class="activity-icon-col">
              <div class="act-icon">${act.icon}</div>
              <div class="act-line"></div>
            </div>
            <div class="activity-details">
              <div class="act-main-row">
                <span class="act-name">${act.name}</span>
                <span class="act-amt ${act.amount_class}">${act.amount}</span>
              </div>
              <span class="act-time">${act.time}</span>
            </div>
          </div>
        `;
      });
    }
  }

  // Initialize
  document.addEventListener('DOMContentLoaded', fetchDashboardData);

})();
