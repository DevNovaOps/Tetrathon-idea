/* FINORA — Page 14: Achievements Scripts */
(function(){
  'use strict';
  const html=document.documentElement,themeToggle=document.getElementById('themeToggle'),mobileToggle=document.getElementById('mobileToggle'),sidebar=document.getElementById('sidebar'),revealEls=document.querySelectorAll('.reveal');
  function stored(){try{return localStorage.getItem('finora-theme')}catch(e){return null}}
  function setTheme(t){html.setAttribute('data-theme',t);try{localStorage.setItem('finora-theme',t)}catch(e){}}
  setTheme(stored()||'dark');
  if(themeToggle)themeToggle.addEventListener('click',()=>{setTheme(html.getAttribute('data-theme')==='dark'?'light':'dark');});
  if(mobileToggle&&sidebar){mobileToggle.addEventListener('click',e=>{e.stopPropagation();sidebar.classList.toggle('open');});document.addEventListener('click',e=>{if(sidebar.classList.contains('open')&&!sidebar.contains(e.target)&&e.target!==mobileToggle)sidebar.classList.remove('open');});}
  function checkReveals(){const t=window.innerHeight*.92;revealEls.forEach(el=>{if(el.getBoundingClientRect().top<t)el.classList.add('visible');});}
  window.addEventListener('scroll',checkReveals,{passive:true});window.addEventListener('load',checkReveals);setTimeout(checkReveals,100);

  /* Modal Helpers */
  const explainModal = document.getElementById('explainModal');
  const closeExplainBtn = document.getElementById('closeExplainBtn');
  if(closeExplainBtn && explainModal){
    closeExplainBtn.addEventListener('click', () => { explainModal.style.display = 'none'; });
    explainModal.addEventListener('click', (e) => { if(e.target === explainModal) explainModal.style.display = 'none'; });
  }

  function openExplainModal(achId){
    if(!achId || !explainModal) return;
    explainModal.style.display = 'flex';
    document.getElementById('explainTitle').textContent = "Loading Insight...";
    document.getElementById('explainText').textContent = "Analyzing deterministic AI progression rules...";
    document.getElementById('explainSteps').innerHTML = "<li>Loading action steps...</li>";

    fetch(`/api/achievements/explain/${achId}/`)
      .then(r => r.json())
      .then(data => {
        document.getElementById('explainIcon').textContent = data.badge_icon || "🏆";
        document.getElementById('explainTitle').textContent = data.title;
        const statusEl = document.getElementById('explainStatus');
        statusEl.textContent = `${data.status} (+${data.xp_reward || 50} XP)`;
        statusEl.style.color = data.status && data.status.includes('Unlocked') ? '#10B981' : '#F59E0B';
        
        document.getElementById('explainText').textContent = data.explanation;
        document.getElementById('explainProgressText').textContent = data.progress_text || "100 / 100";
        document.getElementById('explainProgressBar').style.width = `${data.progress_pct || 100}%`;

        const stepsUl = document.getElementById('explainSteps');
        stepsUl.innerHTML = '';
        if(data.action_steps && data.action_steps.length > 0){
          data.action_steps.forEach(step => {
            const li = document.createElement('li');
            li.style.marginBottom = "8px";
            li.textContent = step;
            stepsUl.appendChild(li);
          });
        } else {
          stepsUl.innerHTML = "<li>Maintain consistent financial habits across Finora to unlock this badge.</li>";
        }
      })
      .catch(err => {
        console.error("Error loading achievement explanation:", err);
        document.getElementById('explainTitle').textContent = "Insight Unavailable";
      });
  }

  /* Load Live Achievements Data */
  function loadAchievementsData(){
    fetch('/api/achievements/')
      .then(r => r.json())
      .then(data => {
        if(!data) return;

        // Row 1: Summary
        if(data.summary){
          const sumVals = document.querySelectorAll('.ach-sum .ach-sum-val');
          if(sumVals.length >= 4){
            sumVals[0].textContent = data.summary.unlocked_count;
            sumVals[1].textContent = data.summary.completion_pct;
            sumVals[2].textContent = data.summary.current_level;
            sumVals[3].textContent = data.summary.current_streak;
          }
        }

        // Row 2: Unlocked Achievements Grid
        if(data.unlocked_achievements && data.unlocked_achievements.length > 0){
          const bGrid = document.querySelector('.badges-grid');
          if(bGrid){
            bGrid.innerHTML = '';
            const colors = ['green-bg', 'blue-bg', 'orange-bg', 'purple-bg', 'cyan-bg', 'emerald-bg'];
            data.unlocked_achievements.forEach((ach, idx) => {
              const dClass = idx > 0 ? `reveal--d${idx % 4}` : '';
              const colorClass = colors[idx % colors.length];
              const card = document.createElement('div');
              card.className = `ach-card glass-card unlocked reveal visible ${dClass}`;
              card.style.cursor = 'pointer';
              card.innerHTML = `
                <div class="ach-icon ${colorClass}">${ach.icon}</div>
                <h4>${ach.title}</h4>
                <p>${ach.description}</p>
                <div class="ach-status"><span class="ach-earned green-text">✓ Earned (${ach.unlocked_at || 'Recently'})</span></div>
              `;
              card.onclick = () => openExplainModal(ach.id);
              bGrid.appendChild(card);
            });
          }
        }

        // Row 3: Locked / Next Achievements Grid
        if(data.locked_milestones && data.locked_milestones.length > 0){
          const lGrid = document.querySelector('.locked-grid');
          if(lGrid){
            lGrid.innerHTML = '';
            data.locked_milestones.forEach((mile, idx) => {
              const dClass = idx > 0 ? `reveal--d${idx % 5}` : '';
              const card = document.createElement('div');
              card.className = `locked-card glass-card reveal visible ${dClass}`;
              card.style.cursor = 'pointer';
              card.innerHTML = `
                <div class="locked-icon">${mile.icon}</div>
                <h4>${mile.title}</h4>
                <p>${mile.description}</p>
                <div class="locked-bar"><div class="locked-bar-fill" style="width:${mile.progress_pct || 0}%"></div></div>
                <span class="locked-progress">${mile.progress_text || ''}</span>
              `;
              card.onclick = () => openExplainModal(mile.id);
              lGrid.appendChild(card);
            });
          }
        }

        // Row 4: User Statistics Grid
        if(data.statistics){
          const st = data.statistics;
          const uVals = document.querySelectorAll('.user-stats-grid .ustat-val');
          if(uVals.length >= 6){
            uVals[0].textContent = st.courses_completed;
            uVals[1].textContent = st.reports_generated;
            uVals[2].textContent = st.ai_assessments;
            uVals[3].textContent = st.investment_plans;
            uVals[4].textContent = st.financial_goals;
            uVals[5].textContent = st.learning_hours;
          }
        }
      })
      .catch(err => console.error("Error loading live achievements data:", err));
  }

  document.addEventListener('DOMContentLoaded', () => {
    loadAchievementsData();
  });
  if(document.readyState==='complete'||document.readyState==='interactive'){
    setTimeout(loadAchievementsData, 50);
  }
})();
