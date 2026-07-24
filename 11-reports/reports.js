/* FINORA — Page 11: Financial Reports Scripts */
(function(){
  'use strict';
  const html=document.documentElement,themeToggle=document.getElementById('themeToggle'),mobileToggle=document.getElementById('mobileToggle'),sidebar=document.getElementById('sidebar'),revealEls=document.querySelectorAll('.reveal');
  let barChart=null,donutChart=null;

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
    barChart=new Chart(ctx,{type:'bar',data:{labels:['Jan','Feb','Mar','Apr','May','Jun','Jul'],datasets:[
      {label:'Income',data:[55000,58000,56000,60000,62000,61000,65000],backgroundColor:'#6366F1',borderRadius:6,barPercentage:.7,categoryPercentage:.6},
      {label:'Expense',data:[35000,36000,34000,38000,38500,37000,36500],backgroundColor:'#EF4444',borderRadius:6,barPercentage:.7,categoryPercentage:.6},
      {label:'Savings',data:[20000,22000,22000,22000,23500,24000,28500],backgroundColor:'#10B981',borderRadius:6,barPercentage:.7,categoryPercentage:.6}
    ]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:bgc(),titleColor:isDark()?'#FFF':'#0F172A',bodyColor:tc(),borderColor:isDark()?'rgba(255,255,255,.1)':'rgba(0,0,0,.1)',borderWidth:1,padding:12}},scales:{x:{grid:{display:false},ticks:{color:tc(),font:{family:'Inter',size:12}}},y:{grid:{color:gc()},ticks:{color:tc(),font:{family:'Inter',size:11},callback:v=>'₹'+(v/1000)+'k'}}}}});
  }

  function initDonutChart(){
    const ctx=document.getElementById('expenseDonutChart');if(!ctx)return;
    donutChart=new Chart(ctx,{type:'doughnut',data:{labels:['Housing','Food','Transport','Shopping','Entertainment','Utilities','Healthcare','Others'],datasets:[{data:[12000,6500,4000,5000,3500,3000,2500,2000],backgroundColor:['#6366F1','#10B981','#3B82F6','#F97316','#A855F7','#06B6D4','#EF4444','#64748B'],borderColor:isDark()?'#0D1526':'#FFF',borderWidth:3,hoverOffset:8}]},options:{responsive:true,maintainAspectRatio:false,cutout:'68%',plugins:{legend:{position:'bottom',labels:{color:tc(),font:{family:'Inter',size:10,weight:'600'},padding:10,usePointStyle:true,pointStyle:'circle'}},tooltip:{backgroundColor:bgc(),titleColor:isDark()?'#FFF':'#0F172A',bodyColor:tc(),borderColor:isDark()?'rgba(255,255,255,.1)':'rgba(0,0,0,.1)',borderWidth:1,padding:12}}}});
  }

  function updateChartsTheme(t){
    const d=t==='dark';
    [barChart,donutChart].forEach(c=>{if(!c)return;if(c.config.type==='bar'){c.options.scales.x.ticks.color=d?'#94A3B8':'#475569';c.options.scales.y.ticks.color=d?'#94A3B8':'#475569';c.options.scales.y.grid.color=d?'rgba(255,255,255,.06)':'rgba(0,0,0,.05)';}if(c.config.type==='doughnut'){c.data.datasets[0].borderColor=d?'#0D1526':'#FFF';c.options.plugins.legend.labels.color=d?'#94A3B8':'#475569';}c.options.plugins.tooltip.backgroundColor=d?'#0D1526':'#FFF';c.options.plugins.tooltip.titleColor=d?'#FFF':'#0F172A';c.options.plugins.tooltip.bodyColor=d?'#94A3B8':'#475569';c.update();});
  }

  /* Health Score Animated Ring */
  function animateHealthRing(){
    const arc=document.getElementById('healthArc'),text=document.getElementById('healthScoreText');
    if(!arc)return;
    const target=91,circumference=327,targetDash=(target/100)*circumference;
    let frame=0;const total=60;
    function tick(){frame++;const t=frame/total,e=1-Math.pow(1-t,3),d=e*targetDash;arc.setAttribute('stroke-dasharray',d+' '+circumference);if(text)text.textContent=Math.round(e*target);if(frame<total)requestAnimationFrame(tick);}
    requestAnimationFrame(tick);
  }

  function boot(){initBarChart();initDonutChart();animateHealthRing();}
  document.addEventListener('DOMContentLoaded',boot);
  if(document.readyState==='complete'||document.readyState==='interactive')setTimeout(boot,50);
})();
