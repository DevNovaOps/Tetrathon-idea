/* ===================================================
   FINORA — Page 8: Risk Assessment Result Scripts
   Gauge Animation, Theme Toggle, Reveal
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');

  /* ---- THEME ---- */
  function stored() { try { return localStorage.getItem('finora-theme'); } catch(e) { return null; } }
  function setTheme(t) { html.setAttribute('data-theme', t); try { localStorage.setItem('finora-theme', t); } catch(e){} }
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
    document.querySelectorAll('.reveal').forEach(el => { 
      if (el.getBoundingClientRect().top < trigger) el.classList.add('visible'); 
    });
  }
  window.addEventListener('scroll', checkReveals, { passive: true });
  window.addEventListener('load', checkReveals);
  setTimeout(checkReveals, 100);

  /* ---- ANIMATED RISK GAUGE ---- */
  function animateRiskGauge(fraction) {
    const arc = document.getElementById('riskGaugeArc');
    const needle = document.getElementById('riskNeedle');
    if (!arc) return;

    const ARC_LENGTH = 314;
    const targetDash = fraction * ARC_LENGTH;

    let frame = 0;
    const totalFrames = 70;

    function tick() {
      frame++;
      const t = frame / totalFrames;
      const eased = 1 - Math.pow(1 - t, 3);
      const progress = eased * targetDash;
      arc.setAttribute('stroke-dasharray', progress + ' ' + ARC_LENGTH);

      if (frame < totalFrames) {
        requestAnimationFrame(tick);
      } else {
        // Position needle at Moderate (~50%)
        if (needle) {
          const angle = Math.PI * (1 - fraction); // from left (π) to right (0)
          const needleLength = 80;
          const cx = 130;
          const cy = 135;
          const x2 = cx + needleLength * Math.cos(angle);
          const y2 = cy - needleLength * Math.sin(angle);
          needle.setAttribute('x2', x2);
          needle.setAttribute('y2', y2);
          needle.setAttribute('opacity', '1');
          needle.style.transition = 'all 0.5s ease';
        }
      }
    }

    requestAnimationFrame(tick);
  }

  /* ---- BOOT ---- */
  /* ---- BOOT AND FETCH ---- */
  async function boot() {
    try {
      const res = await fetch('/api/risk-profile/');
      if (res.status === 401 || res.status === 403) {
        window.location.href = '/';
        return;
      }
      
      const json = await res.json();
      if (json.success && json.data) {
        populateUI(json.data);
      } else {
        animateRiskGauge(0.5); // Fallback
      }
    } catch (e) {
      console.error(e);
      animateRiskGauge(0.5); // Fallback
    }
  }

  function populateUI(data) {
    // Gauge & Score
    const fraction = Math.max(0, Math.min(100, data.risk_score)) / 100;
    animateRiskGauge(fraction);
    
    const riskLevelText = document.getElementById('riskLevelText');
    if (riskLevelText) riskLevelText.textContent = data.risk_bucket;
    
    // Confidence
    const confBadge = document.querySelector('.confidence-badge');
    if (confBadge) confBadge.innerHTML = `<span class="pulse-dot"></span> ${data.confidence_score}% Confidence`;
    
    // About You Text (AI Explanation)
    const aboutText = document.querySelector('.about-text');
    if (aboutText && data.ai_summary && data.ai_summary.natural_language_explanation) {
      aboutText.innerHTML = `<p>${data.ai_summary.natural_language_explanation}</p>`;
    }

    // Suitable Investments
    const suitableList = document.querySelector('.suitable-list');
    if (suitableList && data.portfolio_allocation && data.portfolio_allocation.length > 0) {
      suitableList.innerHTML = '';
      data.portfolio_allocation.forEach(port => {
        // Simple mapping for color/emoji based on risk
        let color = 'green'; let emoji = '📈';
        if (port.risk === 'Moderate') { color = 'blue'; emoji = '🏦'; }
        else if (port.risk === 'High' || port.risk === 'Very High') { color = 'orange'; emoji = '⚡'; }
        else if (port.risk === 'Very Low') { color = 'purple'; emoji = '⚖️'; }

        suitableList.innerHTML += `
          <div class="suitable-item">
            <div class="suit-icon ${color}-bg">${emoji}</div>
            <div class="suit-info"><span class="suit-name">${port.name} (${port.allocation_pct}%)</span><span class="suit-meta">${port.risk} Risk · ${port.cagr} Returns</span></div>
          </div>
        `;
      });
    }
    
    // Risk Breakdown Grid
    const grid = document.querySelector('.breakdown-grid');
    if (grid && data.risk_breakdown && data.risk_breakdown.length > 0) {
      grid.innerHTML = '';
      data.risk_breakdown.forEach((f, idx) => {
        grid.innerHTML += `
          <div class="metric-mini-card glass-card reveal visible reveal--delay-${idx}">
            <div class="metric-emoji ${f.color}-bg">${f.emoji}</div>
            <span class="metric-title">${f.title}</span>
            <span class="metric-val ${f.color}-text">${f.percentage}% (${f.status})</span>
          </div>
        `;
      });
    }

    // AI Insights (Recommendations)
    const insightsGrid = document.querySelector('.insights-grid');
    if (insightsGrid && data.recommendations && data.recommendations.length > 0) {
      insightsGrid.innerHTML = '';
      data.recommendations.forEach((rec, idx) => {
        insightsGrid.innerHTML += `
          <div class="insight-card glass-card reveal visible reveal--delay-${idx}">
            <div class="insight-icon blue-bg"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg></div>
            <div class="insight-body">
              <h4>${rec.action} <span style="font-size: 0.8em; opacity: 0.8; margin-left: 8px;">(Priority: ${rec.priority})</span></h4>
              <p>${rec.reason} <br/><strong>Benefit:</strong> ${rec.benefit} <br/><em>Impact: -${rec.risk_reduction_estimate} Risk | Time: ${rec.estimated_completion_time}</em></p>
            </div>
          </div>
        `;
      });
    }
    
    // Investment Readiness CTA
    const ctaContent = document.querySelector('.cta-content');
    if (ctaContent && data.investment_readiness) {
      ctaContent.innerHTML = `
        <h3 class="cta-title">Investment Readiness: ${data.investment_readiness.percentage}% (${data.investment_readiness.readiness_level})</h3>
        <p class="cta-text">${data.investment_readiness.reason} <br/><strong>Next Action:</strong> ${data.investment_readiness.next_action}</p>
      `;
    }
    
    // Educational Disclaimer
    if (data.educational_disclaimer) {
      const footer = document.querySelector('.cta-section');
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

  document.addEventListener('DOMContentLoaded', boot);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(boot, 50);
  }

})();
