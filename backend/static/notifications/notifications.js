/* ===================================================
   FINORA — Page 12: Notifications Scripts
   Live Backend API Integration, Filters, Stats, Quick Actions
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');
  const revealEls = document.querySelectorAll('.reveal');

  /* ---- THEME PERSISTENCE ---- */
  function stored() { try { return localStorage.getItem('finora-theme'); } catch(e) { return null; } }
  function setTheme(t) {
    html.setAttribute('data-theme', t);
    try { localStorage.setItem('finora-theme', t); } catch(e){}
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

  /* ---- CSRF TOKEN HELPER ---- */
  function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, 10) === ('csrftoken=')) {
          cookieValue = decodeURIComponent(cookie.substring(10));
          break;
        }
      }
    }
    return cookieValue || '';
  }

  /* ---- HELPER: ICON & BADGE MAPPING ---- */
  function getIconAndBadge(notif) {
    const cat = (notif.category || '').toLowerCase();
    const type = (notif.type || '').toLowerCase();
    const title = (notif.title || '').toLowerCase();

    if (cat.includes('bill') || title.includes('bill') || title.includes('electricity')) {
      return { bg: 'green-bg', icon: '⚡', badgeClass: 'badge--green', badgeText: 'Bills' };
    }
    if (cat.includes('invest') || title.includes('sip') || title.includes('portfolio') || title.includes('fund')) {
      return { bg: 'blue-bg', icon: '📊', badgeClass: 'badge--blue', badgeText: 'Investment' };
    }
    if (cat.includes('credit') || title.includes('credit score') || title.includes('cibil')) {
      return { bg: 'purple-bg', icon: '🛡️', badgeClass: 'badge--purple', badgeText: 'Credit' };
    }
    if (cat.includes('ai') || type.includes('ai') || title.includes('ai ') || title.includes('recommendation')) {
      return { bg: 'orange-bg', icon: '🧠', badgeClass: 'badge--orange', badgeText: 'AI Insight' };
    }
    if (cat.includes('secur') || title.includes('emergency') || title.includes('password') || title.includes('login')) {
      return { bg: 'cyan-bg', icon: '🛟', badgeClass: 'badge--cyan', badgeText: 'Security' };
    }
    if (cat.includes('educat') || cat.includes('learn') || title.includes('lesson') || title.includes('course') || title.includes('article')) {
      return { bg: 'green-bg', icon: '📚', badgeClass: 'badge--green', badgeText: 'Learn' };
    }
    if (cat.includes('report') || title.includes('report') || title.includes('summary')) {
      return { bg: 'blue-bg', icon: '📄', badgeClass: 'badge--blue', badgeText: 'Report' };
    }
    if (cat.includes('achieve') || type.includes('achieve') || title.includes('milestone') || title.includes('badge') || title.includes('xp')) {
      return { bg: 'purple-bg', icon: '🏆', badgeClass: 'badge--purple', badgeText: 'Milestone' };
    }
    if (cat.includes('simulat') || title.includes('simulation') || title.includes('projection')) {
      return { bg: 'cyan-bg', icon: '📈', badgeClass: 'badge--cyan', badgeText: 'Simulator' };
    }
    if (cat.includes('risk') || title.includes('risk')) {
      return { bg: 'orange-bg', icon: '⚖️', badgeClass: 'badge--orange', badgeText: 'Risk Profile' };
    }
    if (cat.includes('dashboard') || title.includes('salary') || title.includes('income') || title.includes('expense')) {
      return { bg: 'blue-bg', icon: '💰', badgeClass: 'badge--blue', badgeText: 'Dashboard' };
    }
    return { bg: 'purple-bg', icon: '🔔', badgeClass: 'badge--purple', badgeText: notif.category || 'General' };
  }

  /* ---- FETCH & RENDER NOTIFICATIONS ---- */
  function loadNotifications(filterParam = 'all') {
    const listCol = document.querySelector('.notif-list-col');
    if (!listCol) return;

    let url = '/api/notifications/';
    if (filterParam && filterParam.toLowerCase() !== 'all') {
      url = `/api/notifications/filter/?filter=${encodeURIComponent(filterParam)}`;
    }

    fetch(url)
      .then(r => r.json())
      .then(data => {
        const notifs = data.notifications || [];
        renderNotificationGroups(listCol, notifs);
        updateStats();
      })
      .catch(err => {
        console.error('Error loading notifications:', err);
      });
  }

  function renderNotificationGroups(container, notifs) {
    container.innerHTML = '';

    if (notifs.length === 0) {
      container.innerHTML = `
        <div class="glass-card reveal visible" style="padding:48px 24px; text-align:center; border-radius:20px;">
          <div style="font-size:3.5rem; margin-bottom:12px; opacity:0.7;">📭</div>
          <h3 style="margin:0 0 8px; font-size:1.3rem;">No Notifications Found</h3>
          <p style="color:var(--text-muted); font-size:0.95rem; margin:0;">You're all caught up! When financial alerts occur, they will appear right here.</p>
        </div>
      `;
      return;
    }

    // Grouping: Today, This Week, Older
    const today = [];
    const thisWeek = [];
    const older = [];

    const now = new Date();
    const todayStr = now.toDateString();

    notifs.forEach(n => {
      const dt = new Date(n.created_at);
      const diffDays = (now - dt) / (1000 * 60 * 60 * 24);

      if (dt.toDateString() === todayStr || diffDays < 1) {
        today.push(n);
      } else if (diffDays < 7) {
        thisWeek.push(n);
      } else {
        older.push(n);
      }
    });

    if (today.length > 0) {
      container.appendChild(createGroupElement('Today', today, 0));
    }
    if (thisWeek.length > 0) {
      container.appendChild(createGroupElement('This Week', thisWeek, 1));
    }
    if (older.length > 0) {
      container.appendChild(createGroupElement('Older', older, 2));
    }

    // Append View All CTA
    const ctaDiv = document.createElement('div');
    ctaDiv.className = 'view-all-cta reveal visible';
    ctaDiv.style.marginTop = '24px';
    ctaDiv.innerHTML = `<button class="btn btn-outline btn-full" id="viewAllBtn">View All Notifications (${notifs.length})</button>`;
    ctaDiv.querySelector('#viewAllBtn').onclick = () => {
      document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      const firstChip = document.querySelector('.chip');
      if (firstChip) firstChip.classList.add('active');
      loadNotifications('all');
    };
    container.appendChild(ctaDiv);

    // Re-trigger reveal check
    setTimeout(checkReveals, 50);
  }

  function createGroupElement(label, items, delayIdx) {
    const groupDiv = document.createElement('div');
    groupDiv.className = `notif-group reveal visible ${delayIdx > 0 ? 'reveal--d' + delayIdx : ''}`;
    groupDiv.innerHTML = `<h3 class="group-label">${label}</h3>`;

    items.forEach(notif => {
      const { bg, icon, badgeClass, badgeText } = getIconAndBadge(notif);
      const card = document.createElement('div');
      card.className = `notif-card glass-card ${notif.is_read ? '' : 'unread'}`;
      card.style.cursor = 'pointer';

      let dotHtml = notif.is_read ? '' : `<div class="notif-dot-wrap"><span class="unread-dot"></span></div>`;
      let badgeHtml = badgeText ? `<span class="notif-badge ${badgeClass}">${badgeText}</span>` : '';

      card.innerHTML = `
        ${dotHtml}
        <div class="notif-icon ${bg}">${icon}</div>
        <div class="notif-body">
          <h4>${notif.title}</h4>
          <p>${notif.message}</p>
        </div>
        <div class="notif-meta">
          <span class="notif-time">${notif.time_ago || 'Recently'}</span>
          ${badgeHtml}
        </div>
      `;

      card.addEventListener('click', () => {
        if (!notif.is_read) {
          fetch(`/api/notifications/${notif.id}/read/`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCSRFToken() },
            body: JSON.stringify({})
          })
          .then(r => r.json())
          .then(() => {
            notif.is_read = true;
            card.classList.remove('unread');
            const dot = card.querySelector('.notif-dot-wrap');
            if (dot) dot.style.display = 'none';
            updateStats();
          });
        }
        if (notif.action_url && notif.action_url !== '#') {
          window.location.href = notif.action_url;
        }
      });

      groupDiv.appendChild(card);
    });

    return groupDiv;
  }

  /* ---- FETCH & UPDATE STATISTICS ---- */
  function updateStats() {
    fetch('/api/notifications/stats/')
      .then(r => r.json())
      .then(stats => {
        if (!stats) return;

        // Stat rows in panel
        const statRows = document.querySelectorAll('.stat-row');
        statRows.forEach(row => {
          const label = row.querySelector('.stat-label')?.textContent.trim().toLowerCase() || '';
          const valEl = row.querySelector('.stat-val');
          if (!valEl) return;

          if (label === 'unread') valEl.textContent = stats.unread || 0;
          else if (label.includes('today')) valEl.textContent = stats.today_alerts || 0;
          else if (label.includes('week')) valEl.textContent = stats.this_week || 0;
          else if (label.includes('ai')) valEl.textContent = stats.ai_recommendations || 0;
          else if (label.includes('security')) valEl.textContent = stats.security_alerts || 0;
        });

        // Unread chip counter
        const chipCount = document.querySelector('.chip-count');
        if (chipCount) chipCount.textContent = stats.unread || 0;

        // Global Navigation Bell Badge
        const bellBadge = document.querySelector('.bell-badge');
        if (bellBadge) {
          if (stats.unread > 0) {
            bellBadge.style.display = 'block';
            if (bellBadge.clientWidth > 10 || bellBadge.textContent.trim() !== '') {
              bellBadge.textContent = stats.unread > 99 ? '99+' : stats.unread;
            }
          } else {
            bellBadge.style.display = 'none';
          }
        }
      })
      .catch(err => console.error('Error updating stats:', err));
  }

  /* ---- FILTER CHIPS INTERACTIVITY ---- */
  function setupFilters() {
    const chips = document.querySelectorAll('.chip');
    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        chips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');

        let filterText = chip.textContent.replace(/[0-9]+/g, '').trim();
        loadNotifications(filterText);
      });
    });
  }

  /* ---- QUICK ACTIONS ---- */
  function setupQuickActions() {
    const qaBtns = document.querySelectorAll('.qa-btn');
    qaBtns.forEach(btn => {
      const text = btn.textContent.trim().toLowerCase();

      if (text.includes('mark all as read')) {
        btn.onclick = () => {
          fetch('/api/notifications/read-all/', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCSRFToken() },
            body: JSON.stringify({})
          })
          .then(r => r.json())
          .then(res => {
            loadNotifications('all');
            updateStats();
            alert(`All notifications marked as read! (${res.count || 0} updated)`);
          })
          .catch(err => console.error('Error marking all as read:', err));
        };
      }
      else if (text.includes('download history')) {
        btn.onclick = () => {
          window.location.href = '/api/notifications/history/?export=csv';
        };
      }
      else if (text.includes('manage preferences')) {
        btn.onclick = () => {
          openPreferencesModal();
        };
      }
      else if (text.includes('view ai recommendations')) {
        btn.onclick = () => {
          document.querySelectorAll('.chip').forEach(c => {
            c.classList.remove('active');
            if (c.textContent.toLowerCase().includes('ai')) c.classList.add('active');
          });
          loadNotifications('AI Insights');
        };
      }
    });
  }

  /* ---- MANAGE PREFERENCES MODAL ---- */
  function openPreferencesModal() {
    const modal = document.getElementById('preferencesModal');
    const form = document.getElementById('prefForm');
    if (!modal || !form) return;

    // Fetch current user preferences
    fetch('/api/notifications/preferences/')
      .then(r => r.json())
      .then(pref => {
        if (pref && !pref.error) {
          form.querySelectorAll('input[type="checkbox"]').forEach(chk => {
            const name = chk.getAttribute('name');
            if (pref.hasOwnProperty(name)) {
              chk.checked = !!pref[name];
            }
          });
        }
        modal.style.display = 'flex';
      })
      .catch(err => {
        console.error('Error loading preferences:', err);
        modal.style.display = 'flex';
      });

    const closeBtn = document.getElementById('closePrefBtn');
    const cancelBtn = document.getElementById('cancelPrefBtn');
    const closeModal = () => { modal.style.display = 'none'; };
    if (closeBtn) closeBtn.onclick = closeModal;
    if (cancelBtn) cancelBtn.onclick = closeModal;

    form.onsubmit = (e) => {
      e.preventDefault();
      const data = {};
      form.querySelectorAll('input[type="checkbox"]').forEach(chk => {
        data[chk.getAttribute('name')] = chk.checked;
      });

      const submitBtn = form.querySelector('button[type="submit"]');
      const origText = submitBtn ? submitBtn.textContent : 'Save';
      if (submitBtn) submitBtn.textContent = 'Saving...';

      fetch('/api/notifications/preferences/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCSRFToken() },
        body: JSON.stringify(data)
      })
      .then(r => r.json())
      .then(() => {
        if (submitBtn) submitBtn.textContent = origText;
        closeModal();
        alert('Notification preferences saved successfully!');
      })
      .catch(err => {
        console.error('Error saving preferences:', err);
        if (submitBtn) submitBtn.textContent = origText;
        alert('Failed to save preferences. Please try again.');
      });
    };
  }

  /* ---- BOOT ---- */
  function boot() {
    setupFilters();
    setupQuickActions();
    loadNotifications('all');
    updateStats();
    checkReveals();
  }

  document.addEventListener('DOMContentLoaded', boot);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(boot, 50);
  }

})();
