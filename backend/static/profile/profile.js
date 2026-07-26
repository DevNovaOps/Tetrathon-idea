/* ===================================================
   FINORA — Page 15: Profile Scripts (Backend Driven)
   Theme Persistence, Mobile Sidebar, Reveal Animations,
   Live APIs for Identity, Goals, Services, AI Memory
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');
  const revealEls = document.querySelectorAll('.reveal');

  let currentProfileData = null;

  /* ---- THEME PERSISTENCE & TOGGLE ---- */
  function stored() { try { return localStorage.getItem('finora-theme'); } catch(e) { return null; } }
  function setTheme(t) {
    html.setAttribute('data-theme', t);
    try { localStorage.setItem('finora-theme', t); } catch(e){}
  }
  setTheme(stored() || 'dark');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      setTheme(html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
  }

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

  /* ---- CSRF TOKEN HELPERS ---- */
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  /* ---- BACKEND API INTEGRATION ---- */
  async function loadProfileData() {
    try {
      const res = await fetch('/api/profile/');
      if (!res.ok) return;
      const data = await res.json();
      currentProfileData = data;
      renderAll(data);
    } catch (err) {
      console.error('Error fetching profile data:', err);
    }
  }

  function renderAll(data) {
    renderHeader(data.profile);
    renderPersonalInfo(data.profile);
    renderSnapshot(data.financial_snapshot);
    renderGoals(data.goals, data.account_statistics);
    renderServices(data.connected_services);
    renderTimeline(data.timeline_events);
    renderStats(data.account_statistics);
    renderAboutMe(data.about_me, data.explainable_ai);
    setupQuickActions();
    checkReveals();
  }

  function renderHeader(p) {
    if (!p) return;
    const nameEl = document.querySelector('.ph-user-name');
    const avatarEl = document.querySelector('.ph-avatar-circle span');
    const pills = document.querySelectorAll('.ph-meta-pills span');
    
    if (nameEl) nameEl.textContent = p.display_name || 'Dev Sharma';
    if (avatarEl) avatarEl.textContent = (p.display_name || 'D')[0].toUpperCase();
    if (pills && pills.length >= 3) {
      pills[0].textContent = `📧 ${p.email || 'devsharma@gmail.com'}`;
      pills[1].textContent = `📱 ${p.phone || '+91 Not Provided'}`;
      const dt = p.created_at ? new Date(p.created_at).toLocaleDateString('en-US', {month: 'short', year: 'numeric'}) : 'May 2024';
      pills[2].textContent = `🗓 Member Since ${dt}`;
    }

    const editBtn = document.querySelector('.ph-edit-btn');
    if (editBtn) {
      editBtn.onclick = () => window.openProfileModal();
    }
  }

  function renderPersonalInfo(p) {
    if (!p) return;
    const cells = document.querySelectorAll('.info-cell .info-value');
    if (!cells || cells.length < 8) return;
    cells[0].textContent = p.full_name || p.display_name || 'Not provided';
    cells[1].textContent = p.email || 'Not provided';
    cells[2].textContent = p.phone || '+91 Not provided';
    cells[3].textContent = `${p.city || 'Vadodara'}, ${p.state || 'Gujarat'}, ${p.country || 'India'}`;
    cells[4].textContent = p.occupation || 'Student / Investor';
    const dt = p.created_at ? new Date(p.created_at).toLocaleDateString('en-US', {month: 'short', year: 'numeric'}) : 'May 2024';
    cells[5].textContent = dt;
    cells[6].textContent = p.gender ? `${p.gender}` : 'Male, 22 Years';
    cells[7].textContent = `${p.preferred_language || 'English (US)'} (${p.completion_percentage}% Completed)`;
  }

  function renderSnapshot(s) {
    if (!s) return;
    const vals = document.querySelectorAll('.snapshot-grid .snap-val');
    if (!vals || vals.length < 7) return;
    
    // Credit Score
    const cs = s.credit_score || 730;
    const csTag = cs >= 750 ? 'Excellent' : cs >= 700 ? 'Good' : 'Fair';
    vals[0].innerHTML = `${cs} <span class="snap-sub">${csTag}</span>`;
    
    // Risk Profile
    vals[1].textContent = s.risk_profile || 'Moderate';
    
    // Monthly Income
    vals[2].textContent = `₹${Number(s.monthly_income || 50000).toLocaleString('en-IN')}`;
    
    // Monthly Savings
    vals[3].textContent = `₹${Number(s.monthly_savings || 18000).toLocaleString('en-IN')}`;
    
    // Investment Portfolio
    vals[4].textContent = `₹${Number(s.investment_portfolio || 200000).toLocaleString('en-IN')}`;
    
    // Net Worth
    vals[5].textContent = `₹${Number(s.net_worth || 485000).toLocaleString('en-IN')}`;
    
    // Financial Health
    vals[6].textContent = `${s.financial_health_score || 91} / 100`;
  }

  function renderGoals(goals, stats) {
    const listEl = document.querySelector('.goal-list');
    if (!listEl) return;
    
    let htmlStr = '';
    if (goals && goals.length > 0) {
      goals.forEach(g => {
        const isComp = g.status === 'Completed' || Number(g.completion_percentage) >= 100;
        const colorClass = isComp ? 'green-text' : g.is_primary ? 'purple-text' : 'blue-text';
        const icon = isComp ? '🏆 ' : g.is_primary ? '⭐ ' : '🎯 ';
        const primaryTag = g.is_primary ? ' <span style="font-size:10px;background:rgba(168,85,247,0.2);color:#c084fc;padding:2px 6px;border-radius:10px;">Simulator Goal</span>' : '';
        
        htmlStr += `
          <div class="goal-item" style="cursor:pointer;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05);" onclick="window.openGoalModal('${g.id}')" title="Click to deposit or manage this goal">
            <div class="goal-labels">
              <span>${icon}<strong>${g.goal_name}</strong> (${g.status})${primaryTag} — ₹${Number(g.current_progress).toLocaleString('en-IN')} / ₹${Number(g.target_amount).toLocaleString('en-IN')}</span>
              <span class="${colorClass}">${g.completion_percentage}%</span>
            </div>
            <div class="progress-track"><div class="progress-fill" style="width:${Math.min(g.completion_percentage, 100)}%;background:${isComp ? '#22c55e' : g.is_primary ? '#a855f7' : '#3b82f6'}"></div></div>
          </div>
        `;
      });
    } else {
      htmlStr = `<div style="padding:12px;color:var(--text-muted);text-align:center;">No active goals found. Click '+ Add Goal' below!</div>`;
    }

    htmlStr += `
      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:12px;padding-top:10px;border-top:1px solid var(--border-light);">
        <button class="btn btn-outline" style="padding:6px 14px;font-size:12px;" onclick="window.openGoalModal()">+ Add New Goal</button>
        <div class="goal-badge-row" style="margin:0;">
          <span style="font-size:12px;color:var(--text-secondary);">Achievements Unlocked:</span>
          <span class="goal-badge-val" style="margin-left:8px;">${stats ? stats.achievements : 18} Badges</span>
        </div>
      </div>
    `;

    listEl.innerHTML = htmlStr;
  }

  function renderServices(svc) {
    const listEl = document.querySelector('.services-list');
    if (!listEl || !svc) return;

    let htmlStr = '';
    if (svc.banks) {
      svc.banks.forEach(b => {
        htmlStr += `
          <div class="service-row">
            <div class="svc-left"><span class="svc-icon blue-bg">🏦</span><div><h4>${b.bank_name}</h4><p>${b.masked_account} (${b.account_type})</p></div></div>
            <div style="display:flex;align-items:center;gap:8px;">
              <span class="svc-badge green-badge">${b.connection_status}</span>
              <button onclick="window.removeService('bank', '${b.id}')" style="background:none;border:none;color:var(--text-muted);cursor:pointer;font-size:16px;" title="Disconnect">&times;</button>
            </div>
          </div>
        `;
      });
    }
    if (svc.upis) {
      svc.upis.forEach(u => {
        htmlStr += `
          <div class="service-row">
            <div class="svc-left"><span class="svc-icon purple-bg">⚡</span><div><h4>UPI ID (${u.upi_app})</h4><p>${u.upi_id}</p></div></div>
            <div style="display:flex;align-items:center;gap:8px;">
              <span class="svc-badge green-badge">${u.verification_status}</span>
              <button onclick="window.removeService('upi', '${u.id}')" style="background:none;border:none;color:var(--text-muted);cursor:pointer;font-size:16px;" title="Disconnect">&times;</button>
            </div>
          </div>
        `;
      });
    }
    if (svc.cards) {
      svc.cards.forEach(c => {
        htmlStr += `
          <div class="service-row">
            <div class="svc-left"><span class="svc-icon cyan-bg">💳</span><div><h4>${c.issuer} ${c.card_type}</h4><p>${c.masked_number}</p></div></div>
            <div style="display:flex;align-items:center;gap:8px;">
              <span class="svc-badge green-badge">${c.status}</span>
              <button onclick="window.removeService('card', '${c.id}')" style="background:none;border:none;color:var(--text-muted);cursor:pointer;font-size:16px;" title="Disconnect">&times;</button>
            </div>
          </div>
        `;
      });
    }

    htmlStr += `
      <div style="margin-top:14px;text-align:right;">
        <button class="btn btn-outline" style="padding:6px 14px;font-size:12px;" onclick="window.openServiceModal()">+ Connect Bank / UPI / Card</button>
      </div>
    `;

    listEl.innerHTML = htmlStr;
  }

  function renderTimeline(events) {
    const tlEl = document.querySelector('.timeline');
    if (!tlEl || !events) return;

    let htmlStr = '';
    events.forEach(e => {
      const color = getEventColor(e.category);
      const icon = getEventIcon(e.category);
      htmlStr += `
        <div class="timeline-item">
          <div class="tl-dot ${color}">${icon}</div>
          <div class="tl-content"><h4>${e.title}</h4><p>${e.description || ''}</p></div>
          <span class="tl-time">${e.time_ago || e.date_formatted}</span>
        </div>
      `;
    });

    tlEl.innerHTML = htmlStr;
  }

  function getEventColor(cat) {
    switch ((cat || '').toLowerCase()) {
      case 'learning': return 'green-bg';
      case 'reports': return 'blue-bg';
      case 'investments': return 'purple-bg';
      case 'credit score': return 'orange-bg';
      case 'ai insights': return 'cyan-bg';
      case 'goals': return 'emerald-bg';
      default: return 'purple-bg';
    }
  }

  function getEventIcon(cat) {
    switch ((cat || '').toLowerCase()) {
      case 'learning': return '✓';
      case 'reports': return '📄';
      case 'investments': return '📈';
      case 'credit score': return '🛡️';
      case 'ai insights': return '🤖';
      case 'goals': return '🏆';
      default: return '👤';
    }
  }

  function renderStats(stats) {
    if (!stats) return;
    const vals = document.querySelectorAll('.astats-grid .astat-val');
    if (!vals || vals.length < 6) return;
    vals[0].textContent = stats.reports_generated || 12;
    vals[1].textContent = stats.ai_assessments || 8;
    vals[2].textContent = stats.investments || 5;
    vals[3].textContent = stats.lessons_completed || 18;
    vals[4].textContent = stats.notifications || 42;
    vals[5].innerHTML = `<span class="green-text">${stats.days_active || 30} Days</span>`;
  }

  function renderAboutMe(aboutText, aiObj) {
    const aboutEl = document.getElementById('aboutMeText');
    if (aboutEl && aboutText) {
      aboutEl.textContent = `"${aboutText}"`;
    }

    const aiBox = document.getElementById('explainableAiBox');
    const aiTextEl = document.getElementById('explainableAiText');
    if (aiBox && aiTextEl && aiObj && aiObj.summary_text) {
      aiTextEl.textContent = aiObj.summary_text;
      aiBox.style.display = 'block';
    }
  }

  function setupQuickActions() {
    const cards = document.querySelectorAll('.qa-grid .qa-card');
    if (!cards || cards.length < 6) return;
    
    // 0: Edit Profile
    cards[0].onclick = () => window.openProfileModal();
    // 1: Download My Data
    cards[1].onclick = () => {
      window.location.href = '/api/profile/export/?format=zip';
    };
    // 2: View Reports
    cards[2].onclick = () => window.location.href = '/reports/';
    // 3: Manage Settings
    cards[3].onclick = () => window.location.href = '/settings/';
    // 4: Contact Support
    cards[4].onclick = () => window.location.href = '/settings/#support';
    // 5: View Achievements
    cards[5].onclick = () => window.location.href = '/achievements/';
  }

  /* ---- MODAL HANDLERS ---- */
  window.openProfileModal = function() {
    const m = document.getElementById('profileEditModal');
    if (!m) return;
    if (currentProfileData && currentProfileData.profile) {
      const p = currentProfileData.profile;
      document.getElementById('editFullName').value = p.full_name || p.display_name || '';
      document.getElementById('editPhone').value = p.phone || '';
      document.getElementById('editOccupation').value = p.occupation || '';
      document.getElementById('editCity').value = p.city || '';
      document.getElementById('editCurrency').value = p.preferred_currency || 'INR';
    }
    m.classList.add('open');
  };

  window.closeProfileModal = function() {
    const m = document.getElementById('profileEditModal');
    if (m) m.classList.remove('open');
  };

  window.submitProfileEdit = async function(e) {
    e.preventDefault();
    const body = {
      full_name: document.getElementById('editFullName').value,
      phone: document.getElementById('editPhone').value,
      occupation: document.getElementById('editOccupation').value,
      city: document.getElementById('editCity').value,
      preferred_currency: document.getElementById('editCurrency').value
    };
    try {
      const res = await fetch('/api/profile/update/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
        body: JSON.stringify(body)
      });
      if (res.ok) {
        window.closeProfileModal();
        loadProfileData();
      }
    } catch(err) { console.error('Profile edit error:', err); }
  };

  window.openGoalModal = function(goalId = null) {
    const m = document.getElementById('goalManageModal');
    if (!m) return;
    const titleEl = document.getElementById('goalModalTitle');
    const submitBtn = document.getElementById('goalSubmitBtn');
    const contribGroup = document.getElementById('goalContributeGroup');
    const idInput = document.getElementById('editGoalId');
    
    if (goalId && currentProfileData && currentProfileData.goals) {
      const g = currentProfileData.goals.find(x => strEq(x.id, goalId));
      if (g) {
        idInput.value = g.id;
        titleEl.textContent = `Manage Goal: ${g.goal_name}`;
        submitBtn.textContent = 'Save & Contribute';
        document.getElementById('goalNameInput').value = g.goal_name;
        document.getElementById('goalTargetInput').value = g.target_amount;
        document.getElementById('goalMonthlyInput').value = g.monthly_contribution;
        document.getElementById('goalIsPrimaryInput').checked = g.is_primary;
        contribGroup.style.display = 'flex';
        document.getElementById('goalAddAmt').value = '';
      }
    } else {
      idInput.value = '';
      titleEl.textContent = 'Add New Financial Goal';
      submitBtn.textContent = 'Create Goal';
      document.getElementById('goalNameInput').value = '';
      document.getElementById('goalTargetInput').value = '';
      document.getElementById('goalMonthlyInput').value = '10000';
      document.getElementById('goalIsPrimaryInput').checked = false;
      contribGroup.style.display = 'none';
    }
    m.classList.add('open');
  };

  function strEq(a, b) { return String(a) === String(b); }

  window.closeGoalModal = function() {
    const m = document.getElementById('goalManageModal');
    if (m) m.classList.remove('open');
  };

  window.submitGoalForm = async function(e) {
    e.preventDefault();
    const id = document.getElementById('editGoalId').value;
    const name = document.getElementById('goalNameInput').value;
    const target = document.getElementById('goalTargetInput').value;
    const monthly = document.getElementById('goalMonthlyInput').value;
    const isPrimary = document.getElementById('goalIsPrimaryInput').checked;
    const addAmt = document.getElementById('goalAddAmt').value;

    try {
      if (id) {
        // Update goal
        await fetch(`/api/profile/goals/${id}/`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
          body: JSON.stringify({ goal_name: name, target_amount: target, monthly_contribution: monthly, is_primary: isPrimary })
        });
        if (addAmt && Number(addAmt) > 0) {
          await fetch(`/api/profile/goals/${id}/contribute/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
            body: JSON.stringify({ amount: addAmt, notes: 'Direct deposit from Profile' })
          });
        }
      } else {
        // Create new goal
        await fetch(`/api/profile/goals/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
          body: JSON.stringify({ goal_name: name, target_amount: target, monthly_contribution: monthly, is_primary: isPrimary })
        });
      }
      window.closeGoalModal();
      loadProfileData();
    } catch(err) { console.error('Goal save error:', err); }
  };

  window.openServiceModal = function() {
    const m = document.getElementById('serviceAddModal');
    if (m) {
      window.toggleServiceFields();
      m.classList.add('open');
    }
  };

  window.closeServiceModal = function() {
    const m = document.getElementById('serviceAddModal');
    if (m) m.classList.remove('open');
  };

  window.toggleServiceFields = function() {
    const type = document.getElementById('serviceTypeSelect').value;
    document.getElementById('bankFields').style.display = type === 'bank' ? 'block' : 'none';
    document.getElementById('upiFields').style.display = type === 'upi' ? 'block' : 'none';
    document.getElementById('cardFields').style.display = type === 'card' ? 'block' : 'none';
  };

  window.submitServiceForm = async function(e) {
    e.preventDefault();
    const type = document.getElementById('serviceTypeSelect').value;
    let body = {};
    if (type === 'bank') {
      body = { bank_name: document.getElementById('svcBankName').value || 'HDFC Bank', account_number: document.getElementById('svcAccNum').value || '8839' };
    } else if (type === 'upi') {
      body = { upi_id: document.getElementById('svcUpiId').value || 'user@okaxis', upi_app: document.getElementById('svcUpiApp').value || 'Google Pay' };
    } else if (type === 'card') {
      body = { card_type: document.getElementById('svcCardType').value, issuer: document.getElementById('svcCardIssuer').value || 'HDFC Bank', card_number: document.getElementById('svcCardDigits').value || '4589' };
    }
    try {
      const res = await fetch(`/api/profile/services/${type}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
        body: JSON.stringify(body)
      });
      if (res.ok) {
        window.closeServiceModal();
        loadProfileData();
      }
    } catch(err) { console.error('Service connect error:', err); }
  };

  window.removeService = async function(type, id) {
    if (!confirm('Are you sure you want to disconnect this service?')) return;
    try {
      await fetch(`/api/profile/services/${type}/${id}/`, {
        method: 'DELETE',
        headers: { 'X-CSRFToken': csrftoken }
      });
      loadProfileData();
    } catch(err) { console.error('Remove service error:', err); }
  };

  /* ---- BOOT ---- */
  function boot() {
    checkReveals();
    loadProfileData();
  }

  document.addEventListener('DOMContentLoaded', boot);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(boot, 50);
  }

})();
