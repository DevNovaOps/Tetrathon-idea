/* FINORA — Dynamic Financial Reports Scripts */
(function(){
  'use strict';
  const html=document.documentElement,themeToggle=document.getElementById('themeToggle'),mobileToggle=document.getElementById('mobileToggle'),sidebar=document.getElementById('sidebar'),revealEls=document.querySelectorAll('.reveal');
  let barChart=null,donutChart=null;
  let currentMonth = null;
  let currentYear = null;
  
  const API_BASE = window.location.origin;

  function stored(){try{return localStorage.getItem('finora-theme')}catch(e){return null}}
  function setTheme(t){html.setAttribute('data-theme',t);try{localStorage.setItem('finora-theme',t)}catch(e){}updateChartsTheme(t);}
  setTheme(stored()||'dark');
  if(themeToggle)themeToggle.addEventListener('click',()=>{setTheme(html.getAttribute('data-theme')==='dark'?'light':'dark');});
  if(mobileToggle&&sidebar){mobileToggle.addEventListener('click',e=>{e.stopPropagation();sidebar.classList.toggle('open');});document.addEventListener('click',e=>{if(sidebar.classList.contains('open')&&!sidebar.contains(e.target)&&e.target!==mobileToggle)sidebar.classList.remove('open');});}

  function checkReveals(){const t=window.innerHeight*.92;revealEls.forEach(el=>{if(el.getBoundingClientRect().top<t)el.classList.add('visible');});}
  window.addEventListener('scroll',checkReveals,{passive:true});window.addEventListener('load',checkReveals);setTimeout(checkReveals,100);

  function isDark(){return(html.getAttribute('data-theme')||'dark')==='dark';}
  function tc(){return isDark()?'#94A3B8':'#475569';}
  function gc(){return isDark()?'rgba(255,255,255,.06)':'rgba(0,0,0,.05)';}
  function bgc(){return isDark()?'#0D1526':'#FFFFFF';}

  function initBarChart(){
    const ctx=document.getElementById('monthlyBarChart');if(!ctx)return;
    barChart=new Chart(ctx,{type:'bar',data:{labels:[],datasets:[]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:bgc(),titleColor:isDark()?'#FFF':'#0F172A',bodyColor:tc(),borderColor:isDark()?'rgba(255,255,255,.1)':'rgba(0,0,0,.1)',borderWidth:1,padding:12}},scales:{x:{grid:{display:false},ticks:{color:tc(),font:{family:'Inter',size:12}}},y:{grid:{color:gc()},ticks:{color:tc(),font:{family:'Inter',size:11},callback:v=>'₹'+(v/1000)+'k'}}}}});
  }

  function initDonutChart(){
    const ctx=document.getElementById('expenseDonutChart');if(!ctx)return;
    donutChart=new Chart(ctx,{type:'doughnut',data:{labels:[],datasets:[{data:[],backgroundColor:['#6366F1','#10B981','#3B82F6','#F97316','#A855F7','#06B6D4','#EF4444','#64748B'],borderColor:isDark()?'#0D1526':'#FFF',borderWidth:3,hoverOffset:8}]},options:{responsive:true,maintainAspectRatio:false,cutout:'68%',plugins:{legend:{position:'bottom',labels:{color:tc(),font:{family:'Inter',size:10,weight:'600'},padding:10,usePointStyle:true,pointStyle:'circle'}},tooltip:{backgroundColor:bgc(),titleColor:isDark()?'#FFF':'#0F172A',bodyColor:tc(),borderColor:isDark()?'rgba(255,255,255,.1)':'rgba(0,0,0,.1)',borderWidth:1,padding:12}}}});
  }

  function updateChartsTheme(t){
    const d=t==='dark';
    [barChart,donutChart].forEach(c=>{if(!c)return;if(c.config.type==='bar'){c.options.scales.x.ticks.color=d?'#94A3B8':'#475569';c.options.scales.y.ticks.color=d?'#94A3B8':'#475569';c.options.scales.y.grid.color=d?'rgba(255,255,255,.06)':'rgba(0,0,0,.05)';}if(c.config.type==='doughnut'){c.data.datasets[0].borderColor=d?'#0D1526':'#FFF';c.options.plugins.legend.labels.color=d?'#94A3B8':'#475569';}c.options.plugins.tooltip.backgroundColor=d?'#0D1526':'#FFF';c.options.plugins.tooltip.titleColor=d?'#FFF':'#0F172A';c.options.plugins.tooltip.bodyColor=d?'#94A3B8':'#475569';c.update();});
  }

  function animateHealthRing(targetScore){
    const arc=document.getElementById('healthArc'),text=document.getElementById('healthScoreText');
    const statusText=document.getElementById('healthStatusText');
    if(!arc)return;
    const target=targetScore||0,circumference=327,targetDash=(target/100)*circumference;
    let frame=0;const total=60;
    function tick(){frame++;const t=frame/total,e=1-Math.pow(1-t,3),d=e*targetDash;arc.setAttribute('stroke-dasharray',d+' '+circumference);if(text)text.textContent=Math.round(e*target);if(frame<total)requestAnimationFrame(tick);}
    requestAnimationFrame(tick);
  }

  function renderData(data) {
      // 1. Top Summary — use pre-formatted values from API
      const tsVals = document.querySelectorAll('.ts-val');
      if (tsVals.length >= 4) {
          tsVals[0].textContent = data.summary.total_income;
          tsVals[1].textContent = data.summary.total_expenses;
          tsVals[2].textContent = data.summary.total_savings;
          tsVals[3].textContent = data.summary.investment_value;
      }

      // 2. Bar Chart
      if (barChart && data.charts.monthly) {
          barChart.data.labels = data.charts.monthly.labels;
          barChart.data.datasets = data.charts.monthly.datasets;
          barChart.update();
      }

      // 3. Expense Donut
      if (donutChart && data.charts.expenses) {
          donutChart.data.labels = data.charts.expenses.labels;
          donutChart.data.datasets[0].data = data.charts.expenses.datasets[0].data;
          donutChart.update();
      }

      // 4. Performance Metrics
      const pVals = document.querySelectorAll('.perf-val');
      if (pVals.length >= 5) {
          pVals[0].textContent = data.performance.savings_rate;
          pVals[1].textContent = data.performance.investment_growth;
          pVals[2].textContent = data.performance.credit_score_change;
          pVals[3].textContent = data.performance.expense_reduction;
          pVals[4].textContent = data.performance.emergency_fund_months;
      }

      // 5. AI Insights
      const insightsGrid = document.querySelector('.insights-grid');
      if (insightsGrid && data.insights) {
          insightsGrid.innerHTML = '';
          const icons = ['✓', '⚠', '📈', '💳', '🛡️'];
          const colors = ['green-bg', 'orange-bg', 'blue-bg', 'purple-bg', 'cyan-bg'];
          data.insights.forEach((ins, idx) => {
              const div = document.createElement('div');
              div.className = `ins-card glass-card reveal ${idx > 0 ? 'reveal--d' + Math.min(idx, 5) : ''} visible`;
              div.innerHTML = `<div class="ins-icon ${colors[idx % colors.length]}">${icons[idx % icons.length]}</div><div class="ins-body"><h4>${ins.title}</h4><p>${ins.description}</p></div>`;
              insightsGrid.appendChild(div);
          });
      }

      // 6. Financial Health Score
      if (data.health) {
          animateHealthRing(data.health.score);
          const healthVerdict = document.querySelector('.health-verdict');
          if (healthVerdict) {
              healthVerdict.textContent = data.health.explanation;
              healthVerdict.style.color = data.health.score >= 80 ? '#10B981' : (data.health.score >= 50 ? '#F59E0B' : '#EF4444');
          }
      }
      
      // Update Month Selector Dropdown options if first load
      const selector = document.querySelector('.month-selector');
      if (selector && !selector.querySelector('select')) {
          // Keep SVG, create an invisible select on top
          const sel = document.createElement('select');
          sel.style.position = 'absolute';
          sel.style.top = '0';
          sel.style.left = '0';
          sel.style.width = '100%';
          sel.style.height = '100%';
          sel.style.opacity = '0';
          sel.style.cursor = 'pointer';
          
          data.available_months.forEach(m => {
              const opt = document.createElement('option');
              opt.value = m.value;
              opt.textContent = m.label;
              sel.appendChild(opt);
          });
          
          sel.addEventListener('change', (e) => {
              const val = e.target.value.split('-');
              currentYear = val[0];
              currentMonth = val[1];
              selector.querySelector('span').textContent = e.target.options[e.target.selectedIndex].text;
              fetchReports();
          });
          
          selector.style.position = 'relative';
          selector.appendChild(sel);
          
          if (!currentMonth) {
              const initial = data.available_months[0];
              const parts = initial.value.split('-');
              currentYear = parts[0];
              currentMonth = parts[1];
              selector.querySelector('span').textContent = initial.label;
              sel.value = initial.value;
          }
      }
      
      // 8. Update download card descriptions dynamically
      updateDownloadLabels();
  }
  
  function updateDownloadLabels() {
      const cards = document.querySelectorAll('.dl-card');
      if (!cards.length || !currentMonth || !currentYear) return;
      
      const yr = parseInt(currentYear);
      const mo = parseInt(currentMonth);
      const monthNames = ['','January','February','March','April','May','June','July','August','September','October','November','December'];
      const currentLabel = monthNames[mo] + ' ' + yr;
      
      // Quarter calculation
      const q = Math.ceil(mo / 3);
      const qLabel = 'Q' + q + ' ' + yr + ' breakdown';
      
      // FY calculation (Indian FY: April to March)
      let fyLabel;
      if (mo >= 4) {
          fyLabel = 'FY ' + yr + '-' + String(yr + 1).slice(-2);
      } else {
          fyLabel = 'FY ' + (yr - 1) + '-' + String(yr).slice(-2);
      }
      
      const descMap = [
          currentLabel + ' summary',
          qLabel,
          fyLabel,
          'Portfolio details',
          'Score history',
          'Overall analysis'
      ];
      
      cards.forEach((card, i) => {
          const p = card.querySelector('p');
          if (p && descMap[i]) p.textContent = descMap[i];
      });
  }

  async function fetchReports() {
      try {
          let url = `${API_BASE}/api/reports/`;
          if (currentMonth && currentYear) {
              url += `?month=${currentMonth}&year=${currentYear}`;
          }
          const resp = await fetch(url);
          if (resp.ok) {
              const data = await resp.json();
              renderData(data);
          }
      } catch (err) {
          console.error("Error fetching report data", err);
      }
  }
  
  function setupExportButtons() {
      const typeMap = {
          'Monthly Report': 'monthly',
          'Quarterly Report': 'quarterly',
          'Annual Report': 'annual',
          'Investment Summary': 'investment',
          'Credit Report': 'credit',
          'Financial Health': 'financial-health'
      };
      
      document.querySelectorAll('.dl-card').forEach(card => {
          const btn = card.querySelector('button');
          const title = card.querySelector('h4').textContent.trim();
          const reportType = typeMap[title] || 'monthly';
          
          btn.addEventListener('click', () => {
              btn.textContent = 'Generating...';
              btn.disabled = true;
              let url = `${API_BASE}/api/reports/export/?type=${reportType}`;
              if (currentMonth && currentYear) {
                  url += `&month=${currentMonth}&year=${currentYear}`;
              }
              
              window.open(url, '_blank');
              
              setTimeout(() => {
                  btn.textContent = 'Download PDF';
                  btn.disabled = false;
              }, 2000);
          });
      });
  }

  function boot(){
      initBarChart();
      initDonutChart();
      setupExportButtons();
      fetchReports();
  }
  document.addEventListener('DOMContentLoaded',boot);
  if(document.readyState==='complete'||document.readyState==='interactive')setTimeout(boot,50);
})();
