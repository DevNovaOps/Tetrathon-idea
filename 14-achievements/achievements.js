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
})();
