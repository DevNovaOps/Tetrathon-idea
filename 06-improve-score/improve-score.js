/* ===================================================
   FINORA — Page 6: Improve My Score Scripts
   Progress Bar Animation, Theme Toggle, Reveal
   =================================================== */

(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');
  const revealEls = document.querySelectorAll('.reveal');

  /* ---- THEME PERSISTENCE ---- */
  function stored() {
    try { return localStorage.getItem('finora-theme'); }
    catch (e) { return null; }
  }

  function setTheme(t) {
    html.setAttribute('data-theme', t);
    try { localStorage.setItem('finora-theme', t); }
    catch (e) {}
  }

  setTheme(stored() || 'dark');

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      setTheme(html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
  }

  /* ---- MOBILE SIDEBAR TOGGLE ---- */
  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', e => {
      e.stopPropagation();
      sidebar.classList.toggle('open');
    });

    document.addEventListener('click', e => {
      if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== mobileToggle) {
        sidebar.classList.remove('open');
      }
    });
  }

  /* ---- REVEAL ON SCROLL ---- */
  function checkReveals() {
    const trigger = window.innerHeight * 0.92;
    document.querySelectorAll('.reveal').forEach(el => {
      if (el.getBoundingClientRect().top < trigger) {
        el.classList.add('visible');
      }
    });
  }

  window.addEventListener('scroll', checkReveals, { passive: true });
  window.addEventListener('load', checkReveals);
  setTimeout(checkReveals, 100);

  /* ---- API INTEGRATION ---- */
  async function fetchImproveScoreData() {
    try {
      const response = await fetch('/api/improve-score/', {
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
      
      const resData = await response.json();
      if (resData.success && resData.data) {
        populateData(resData.data);
        setTimeout(animateProgress, 300);
        setTimeout(checkReveals, 100);
      }
    } catch (error) {
      console.error('API Error:', error);
    }
  }

  function populateData(data) {
      // 1. Scores (Hero)
      document.querySelector('.current-score-card .score-number-big').textContent = data.current_score;
      document.querySelector('.target-score-card .score-number-big').textContent = data.target_score;
      
      // Progress Bar
      document.querySelector('.progress-pct-badge').textContent = `${data.completed_tasks} / ${data.total_tasks} Completed`;
      const fill = document.getElementById('roadmapProgressFill');
      if (fill) fill.dataset.width = `${data.completion_percentage}%`;
      
      // Trajectory Row
      const trajScores = document.querySelectorAll('.traj-score');
      if (trajScores.length >= 3) {
          trajScores[0].textContent = data.current_score;
          trajScores[1].textContent = data.estimated_score;
          trajScores[2].textContent = data.target_score;
      }
      
      // 2. Roadmap Journey (Tasks displayed as journey steps)
      const journeyContainer = document.querySelector('.roadmap-journey');
      if (journeyContainer && data.tasks) {
          journeyContainer.innerHTML = '';
          data.tasks.forEach((task, index) => {
              let stepClass = '';
              let numClass = '';
              let statusHtml = '';
              
              if (task.status === 'Completed') {
                  stepClass = 'done-step';
                  statusHtml = '<span class="status-check">✓ Done</span>';
              } else if (task.status === 'In Progress' || index === data.completed_tasks) {
                  stepClass = 'active-step';
                  numClass = 'active-num';
                  statusHtml = '<span class="status-pending">In Progress</span>';
              } else {
                  statusHtml = '<span class="status-pending">Upcoming</span>';
              }
              
              journeyContainer.innerHTML += `
              <div class="journey-step ${stepClass}">
                <div class="step-num-badge ${numClass}">${index + 1}</div>
                <div class="step-content">
                  <span class="step-title">${task.title}</span>
                  <span class="step-desc">${task.description}</span>
                </div>
                ${statusHtml}
                <span class="arrow-indicator">→</span>
              </div>`;
              
              if (index < data.tasks.length - 1) {
                  journeyContainer.innerHTML += `<div class="journey-connector"></div>`;
              }
          });
      }
      
      // 3. AI Recommendations
      const recGrid = document.querySelector('.recommendations-grid');
      if (recGrid && data.tasks) {
          recGrid.innerHTML = '';
          data.tasks.forEach((task, idx) => {
              let badgeColor = 'blue';
              if (task.priority === 'Critical') badgeColor = 'purple';
              else if (task.priority === 'High') badgeColor = 'green';
              else if (task.priority === 'Medium') badgeColor = 'blue';
              else badgeColor = 'cyan';
              
              const delayClass = idx > 0 ? `reveal--delay-${Math.min(idx, 2)}` : '';
              
              recGrid.innerHTML += `
              <div class="rec-card glass-card reveal ${delayClass}">
                <div class="rec-header">
                  <span class="badge badge--${badgeColor}">${task.priority} Priority</span>
                  <span class="score-boost-badge">+${task.expected_points} Points</span>
                </div>
                <h3 class="rec-title">${task.title}</h3>
                <p class="rec-desc">${task.description}</p>
                <div class="rec-meta">
                  <span class="meta-tag">⚡ Difficulty: <strong>${task.difficulty}</strong></span>
                  <span class="meta-tag">⏱️ Time: <strong>${task.duration}</strong></span>
                </div>
              </div>`;
          });
      }
      
      // 4. Weekly Roadmap List
      const weeklyList = document.querySelector('.weekly-plan-list');
      if (weeklyList && data.roadmap_weeks) {
          weeklyList.innerHTML = '';
          data.roadmap_weeks.forEach(week => {
              let badgeClass = 'blue';
              let statusText = week.status;
              let activeClass = '';
              
              if (statusText === 'Complete') badgeClass = 'green';
              else if (statusText === 'In Progress') { badgeClass = 'blue'; activeClass = 'week-badge--active'; }
              else { badgeClass = 'purple'; }
              
              weeklyList.innerHTML += `
              <div class="week-item">
                <div class="week-badge ${activeClass}">Week ${week.week_number}</div>
                <div class="week-info">
                  <span class="week-title">${week.title}</span>
                  <span class="week-desc">${week.description}</span>
                </div>
                <span class="badge badge--${badgeClass}">${statusText}</span>
              </div>`;
          });
      }
      
      // 5. Success Metrics
      const metricsList = document.querySelector('.metrics-list');
      if (metricsList && data.metrics) {
          metricsList.innerHTML = '';
          data.metrics.forEach(m => {
              metricsList.innerHTML += `
              <div class="metric-item">
                <div class="metric-icon-box ${m.bg_class}">${m.icon}</div>
                <div class="metric-content">
                  <span class="metric-name">${m.name}</span>
                  <div class="metric-bar-track"><div class="metric-bar-fill" data-width="${m.percentage}%" style="--c:${m.hex_color};"></div></div>
                </div>
                <span class="metric-value ${m.text_class}">${m.value_text}</span>
              </div>`;
          });
      }
      
      // Optional: Fetch User Name for Header
      fetch('/api/dashboard/')
          .then(res => res.json())
          .then(dashData => {
              if (dashData.success) {
                  document.querySelector('.profile-username').textContent = dashData.data.user.full_name;
                  document.querySelector('.user-name-small').textContent = dashData.data.user.full_name;
                  const initials = dashData.data.user.full_name.substring(0,1).toUpperCase();
                  document.querySelector('.profile-avatar-circle span').textContent = initials;
                  document.querySelector('.user-avatar-small span').textContent = initials;
              }
          })
          .catch(err => console.log('Silently failed to fetch user for header'));
  }

  /* ---- ANIMATE PROGRESS BARS ---- */
  function animateProgress() {
    const fill = document.getElementById('roadmapProgressFill');
    if (fill && fill.dataset.width && fill.getBoundingClientRect().top < window.innerHeight) {
      fill.style.width = fill.dataset.width;
    }

    document.querySelectorAll('.metric-bar-fill').forEach(el => {
      if (el.getBoundingClientRect().top < window.innerHeight && !el.classList.contains('animated')) {
        el.style.setProperty('--w', el.dataset.width);
        el.classList.add('animated');
      }
    });
  }

  window.addEventListener('scroll', animateProgress, { passive: true });
  
  // Initialize
  document.addEventListener('DOMContentLoaded', fetchImproveScoreData);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    fetchImproveScoreData();
  }

})();
