/* FINORA — Page 13: Educational Hub Scripts */
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

  /* Learning Progress Ring */
  function animateRing(targetPct){
    const arc=document.getElementById('learnArc'),text=document.getElementById('learnPctText');if(!arc)return;
    const target=typeof targetPct === 'number' ? targetPct : 60;
    const circumference=327,targetDash=(target/100)*circumference;
    let frame=0;const total=60;
    function tick(){frame++;const t=frame/total,e=1-Math.pow(1-t,3),d=e*targetDash;arc.setAttribute('stroke-dasharray',d+' '+circumference);if(text)text.textContent=Math.round(e*target)+'%';if(frame<total)requestAnimationFrame(tick);}
    requestAnimationFrame(tick);
  }

  /* Modal Helpers */
  const lessonModal = document.getElementById('lessonModal');
  const closeLessonBtn = document.getElementById('closeLessonBtn');
  if(closeLessonBtn && lessonModal){
    closeLessonBtn.addEventListener('click', () => { lessonModal.style.display = 'none'; });
    lessonModal.addEventListener('click', (e) => { if(e.target === lessonModal) lessonModal.style.display = 'none'; });
  }

  let currentLessonId = null;

  function openLessonModal(lessonId){
    if(!lessonId || !lessonModal) return;
    currentLessonId = lessonId;
    lessonModal.style.display = 'flex';
    document.getElementById('lessonTitle').textContent = "Loading Lesson...";
    document.getElementById('lessonContent').innerHTML = "<p>Please wait while we load your AI-curated lesson...</p>";
    document.getElementById('quizSection').style.display = 'none';
    document.getElementById('lessonVideoContainer').style.display = 'none';

    fetch(`/api/learning/lesson/${lessonId}/`)
      .then(r => r.json())
      .then(data => {
        if(data.error){
          document.getElementById('lessonTitle').textContent = "Lesson Not Found";
          return;
        }
        document.getElementById('lessonCourseBadge').textContent = data.course_title || "Course Lesson";
        document.getElementById('lessonTitle').textContent = data.title;
        document.getElementById('lessonDuration').textContent = `⏱ ${data.duration}`;
        document.getElementById('lessonXp').textContent = `🎁 +${data.xp_reward} XP`;
        
        // Render content with basic markdown formatting
        let contentHtml = data.content || "";
        if(data.article) contentHtml = data.article;
        contentHtml = contentHtml.replace(/^### (.*$)/gim, '<h3>$1</h3>')
                                 .replace(/^## (.*$)/gim, '<h2>$1</h2>')
                                 .replace(/^\*\* (.*$)/gim, '<h4>$1</h4>')
                                 .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
                                 .replace(/\n\n/g, '<br><br>');
        document.getElementById('lessonContent').innerHTML = contentHtml;

        if(data.video_url){
          const vid = document.getElementById('lessonVideo');
          vid.src = data.video_url;
          vid.style.display = 'block';
          document.getElementById('lessonVideoContainer').style.display = 'block';
        }

        // Setup Quiz
        if(data.quiz){
          const qSec = document.getElementById('quizSection');
          qSec.style.display = 'block';
          document.getElementById('quizQuestion').textContent = data.quiz.question;
          const optsDiv = document.getElementById('quizOptions');
          optsDiv.innerHTML = '';
          data.quiz.options.forEach((opt, idx) => {
            const lbl = document.createElement('label');
            lbl.style.display = 'flex';
            lbl.style.alignItems = 'center';
            lbl.style.gap = '10px';
            lbl.style.cursor = 'pointer';
            lbl.style.background = 'rgba(255,255,255,0.05)';
            lbl.style.padding = '12px 16px';
            lbl.style.borderRadius = '8px';
            lbl.innerHTML = `<input type="radio" name="quizOpt" value="${idx}" style="cursor:pointer;"> <span>${opt}</span>`;
            optsDiv.appendChild(lbl);
          });
          document.getElementById('quizFeedback').textContent = '';
        }

        // Setup Prev/Next buttons
        const prevBtn = document.getElementById('prevLessonBtn');
        const nextBtn = document.getElementById('nextLessonBtn');
        if(data.prev_lesson_id){
          prevBtn.style.display = 'inline-block';
          prevBtn.onclick = () => openLessonModal(data.prev_lesson_id);
        } else {
          prevBtn.style.display = 'none';
        }
        if(data.next_lesson_id){
          nextBtn.style.display = 'inline-block';
          nextBtn.onclick = () => openLessonModal(data.next_lesson_id);
        } else {
          nextBtn.style.display = 'none';
        }

        const markBtn = document.getElementById('markCompleteBtn');
        if(data.completed){
          markBtn.textContent = "Completed ✓";
          markBtn.style.background = "var(--emerald-bg, #10B981)";
        } else {
          markBtn.textContent = "Mark Lesson Complete ✓";
          markBtn.style.background = "";
          markBtn.onclick = () => completeCurrentLesson();
        }
      })
      .catch(err => console.error("Error loading lesson:", err));
  }

  function completeCurrentLesson(){
    if(!currentLessonId) return;
    const markBtn = document.getElementById('markCompleteBtn');
    markBtn.textContent = "Saving...";
    fetch(`/api/learning/lesson/${currentLessonId}/complete/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    })
    .then(r => r.json())
    .then(res => {
      markBtn.textContent = "Completed ✓";
      markBtn.style.background = "#10B981";
      if(res.unlocked && res.unlocked.length > 0){
        openBadgeModal(res.unlocked[0]);
      }
      loadDashboardData();
    })
    .catch(e => {
      console.error("Error completing lesson:", e);
      markBtn.textContent = "Completed ✓";
    });
  }

  const submitQuizBtn = document.getElementById('submitQuizBtn');
  if(submitQuizBtn){
    submitQuizBtn.addEventListener('click', () => {
      if(!currentLessonId) return;
      const sel = document.querySelector('input[name="quizOpt"]:checked');
      if(!sel){
        document.getElementById('quizFeedback').textContent = "⚠️ Please select an option first.";
        document.getElementById('quizFeedback').style.color = "#F59E0B";
        return;
      }
      submitQuizBtn.textContent = "Evaluating AI Quiz...";
      fetch(`/api/learning/quiz/${currentLessonId}/submit/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ selected_option: parseInt(sel.value) })
      })
      .then(r => r.json())
      .then(res => {
        submitQuizBtn.textContent = "Submit Quiz Answer";
        const fb = document.getElementById('quizFeedback');
        fb.textContent = res.explanation;
        if(res.passed){
          fb.style.color = "#10B981";
          const markBtn = document.getElementById('markCompleteBtn');
          markBtn.textContent = "Completed ✓ (Quiz Passed)";
          markBtn.style.background = "#10B981";
          if(res.unlocked && res.unlocked.length > 0){
            setTimeout(() => openBadgeModal(res.unlocked[0]), 300);
          }
          loadDashboardData();
        } else {
          fb.style.color = "#EF4444";
        }
      })
      .catch(e => {
        console.error("Error submitting quiz:", e);
        submitQuizBtn.textContent = "Submit Quiz Answer";
      });
    });
  }

  const articleModal = document.getElementById('articleModal');
  const closeArticleBtn = document.getElementById('closeArticleBtn');
  if(closeArticleBtn && articleModal){
    closeArticleBtn.addEventListener('click', () => { articleModal.style.display = 'none'; });
    articleModal.addEventListener('click', (e) => { if(e.target === articleModal) articleModal.style.display = 'none'; });
  }

  function openArticleModal(art){
    if(!art || !articleModal) return;
    articleModal.style.display = 'flex';
    document.getElementById('articleTitle').textContent = art.title;
    document.getElementById('articleTag').textContent = art.tag;
    document.getElementById('articleTag').className = `art-tag ${art.tag_color || 'blue-tag'}`;
    document.getElementById('articleMeta').textContent = `${art.read_time} · ${art.difficulty}`;
    document.getElementById('articleSummary').textContent = art.summary;
    document.getElementById('articleBody').innerHTML = (art.content || "").replace(/\n\n/g, '<br><br>');
    const extLink = document.getElementById('articleExtLink');
    if(art.url){
      extLink.href = art.url;
      extLink.style.display = 'inline-flex';
    } else {
      extLink.href = "https://zerodha.com/varsity/";
      extLink.style.display = 'inline-flex';
    }
  }

  const tipModal = document.getElementById('tipModal');
  const closeTipBtn = document.getElementById('closeTipBtn');
  const closeTipActionBtn = document.getElementById('closeTipActionBtn');
  if(tipModal){
    if(closeTipBtn) closeTipBtn.addEventListener('click', () => { tipModal.style.display = 'none'; });
    if(closeTipActionBtn) closeTipActionBtn.addEventListener('click', () => { tipModal.style.display = 'none'; });
    tipModal.addEventListener('click', (e) => { if(e.target === tipModal) tipModal.style.display = 'none'; });
  }

  function openTipModal(tip){
    if(!tip || !tipModal) return;
    tipModal.style.display = 'flex';
    document.getElementById('tipModalIcon').textContent = tip.icon || '🤖';
    document.getElementById('tipModalTitle').textContent = tip.title || 'Finora AI Insight';
    document.getElementById('tipModalContent').textContent = tip.content || '';
  }

  const badgeModal = document.getElementById('badgeModal');
  const closeBadgeBtn = document.getElementById('closeBadgeBtn');
  const closeBadgeActionBtn = document.getElementById('closeBadgeActionBtn');
  if(badgeModal){
    if(closeBadgeBtn) closeBadgeBtn.addEventListener('click', () => { badgeModal.style.display = 'none'; });
    if(closeBadgeActionBtn) closeBadgeActionBtn.addEventListener('click', () => { badgeModal.style.display = 'none'; });
    badgeModal.addEventListener('click', (e) => { if(e.target === badgeModal) badgeModal.style.display = 'none'; });
  }

  function openBadgeModal(b){
    if(!b || !badgeModal) return;
    badgeModal.style.display = 'flex';
    document.getElementById('badgeModalIcon').textContent = b.icon || '🏅';
    document.getElementById('badgeModalTitle').textContent = b.title || 'Badge Title';
    const statusEl = document.getElementById('badgeModalStatus');
    if(statusEl){
      if(b.unlocked){
        statusEl.textContent = 'Unlocked ✓';
        statusEl.style.background = 'rgba(16, 185, 129, 0.2)';
        statusEl.style.color = '#10b981';
        statusEl.style.borderColor = 'rgba(16, 185, 129, 0.3)';
      } else {
        statusEl.textContent = 'Locked 🔒';
        statusEl.style.background = 'rgba(245, 158, 11, 0.2)';
        statusEl.style.color = '#f59e0b';
        statusEl.style.borderColor = 'rgba(245, 158, 11, 0.3)';
      }
    }
    const xpEl = document.getElementById('badgeModalXp');
    if(xpEl) xpEl.textContent = `+${b.xp || 50} XP`;
    document.getElementById('badgeModalDesc').textContent = b.description || 'Complete learning tasks to earn this badge.';
  }

  /* Load Live Dashboard Data */
  function loadDashboardData(){
    fetch('/api/learning/dashboard/')
      .then(r => r.json())
      .then(data => {
        if(!data || !data.progress) return;

        // Row 1: Progress Summary
        animateRing(data.progress.completion_pct);
        const statVals = document.querySelectorAll('.stat-card .stat-val');
        if(statVals.length >= 3){
          statVals[0].innerHTML = `${data.progress.lessons_completed} <span class="stat-dim">/ ${data.progress.total_lessons || 30}</span>`;
          statVals[1].textContent = data.progress.current_level || "Intermediate";
          statVals[2].textContent = `${data.progress.learning_streak || 0} Days`;
        }

        // Row 2: Featured Course
        if(data.featured_course){
          const feat = data.featured_course;
          const featTitle = document.querySelector('.featured-title');
          const featDesc = document.querySelector('.featured-desc');
          const featMeta = document.querySelector('.featured-meta');
          const featProgLabel = document.querySelector('.featured-progress-labels .green-text');
          const featProgFill = document.querySelector('.featured-progress-wrap .progress-fill');
          const contBtn = document.querySelector('.featured-left .btn-primary');

          if(featTitle) featTitle.textContent = feat.title;
          if(featDesc) featDesc.textContent = feat.description;
          if(featMeta) featMeta.innerHTML = `<span>${feat.hours_text}</span><span>${feat.lessons_text}</span><span>${feat.difficulty_text}</span>`;
          if(featProgLabel) featProgLabel.textContent = `${feat.progress_pct}%`;
          if(featProgFill) featProgFill.style.width = `${feat.progress_pct}%`;
          if(contBtn){
            contBtn.onclick = () => {
              if(feat.next_lesson_id) openLessonModal(feat.next_lesson_id);
              else alert("No remaining lessons in featured course!");
            };
          }
        }

        // Row 3: Categories Grid
        if(data.categories && data.categories.length > 0){
          const catGrid = document.querySelector('.cat-grid');
          if(catGrid){
            catGrid.innerHTML = '';
            data.categories.forEach((cat, idx) => {
              const dClass = idx > 0 ? `reveal--d${idx % 6}` : '';
              const card = document.createElement('div');
              card.className = `cat-card glass-card reveal visible ${dClass}`;
              card.style.cursor = 'pointer';
              card.innerHTML = `
                <span class="cat-icon ${cat.bg_class || 'purple-bg'}">${cat.icon}</span>
                <h4>${cat.name}</h4>
                <p>${cat.description}</p>
                <span class="cat-count">${cat.lesson_count_text}</span>
              `;
              card.onclick = () => {
                if(cat.id){
                  fetch(`/api/learning/course/${cat.id}/`)
                    .then(r => r.json())
                    .then(cData => {
                      if(cData && cData.lessons && cData.lessons.length > 0){
                        openLessonModal(cData.lessons[0].id);
                      } else {
                        alert(`Explore our curated lessons in ${cat.name}!`);
                      }
                    });
                } else {
                  alert(`Starting ${cat.name} module...`);
                }
              };
              catGrid.appendChild(card);
            });
          }
        }

        // Row 4: Recommended Articles
        if(data.articles && data.articles.length > 0){
          const artGrid = document.querySelector('.articles-grid');
          if(artGrid){
            artGrid.innerHTML = '';
            data.articles.forEach((art, idx) => {
              const dClass = idx > 0 ? `reveal--d${idx % 5}` : '';
              const card = document.createElement('div');
              card.className = `article-card glass-card reveal visible ${dClass}`;
              card.style.cursor = 'pointer';
              card.innerHTML = `
                <span class="art-tag ${art.tag_color || ''}">${art.tag}</span>
                <h4>${art.title}</h4>
                <p>${art.summary}</p>
                <span class="art-meta">${art.read_time} · ${art.difficulty}</span>
              `;
              card.onclick = () => openArticleModal(art);
              artGrid.appendChild(card);
            });
          }
        }

        // Row 5: AI Learning Tips
        if(data.tips && data.tips.length > 0){
          const tipsGrid = document.querySelector('.tips-grid');
          if(tipsGrid){
            tipsGrid.innerHTML = '';
            data.tips.forEach((tip, idx) => {
              const dClass = idx > 0 ? `reveal--d${idx % 4}` : '';
              const card = document.createElement('div');
              card.className = `tip-card glass-card reveal visible ${dClass}`;
              card.style.cursor = 'pointer';
              card.innerHTML = `
                <div class="tip-icon ${tip.icon_bg || 'green-bg'}">${tip.icon}</div>
                <div class="tip-body">
                  <h4>${tip.title}</h4>
                  <p>${tip.content}</p>
                </div>
              `;
              card.onclick = () => openTipModal(tip);
              tipsGrid.appendChild(card);
            });
          }
        }

        // Row 6: Badges Preview
        if(data.badges_preview && data.badges_preview.length > 0){
          const badgeRow = document.querySelector('.badge-row');
          if(badgeRow){
            badgeRow.innerHTML = '';
            data.badges_preview.forEach(b => {
              const item = document.createElement('div');
              item.className = `badge-item ${b.unlocked ? 'unlocked' : ''}`;
              item.style.cursor = 'pointer';
              item.innerHTML = `<span class="badge-emoji">${b.icon}</span><span class="badge-name">${b.title}</span>`;
              item.onclick = () => openBadgeModal(b);
              badgeRow.appendChild(item);
            });
          }
        }
      })
      .catch(err => {
        console.error("Error loading live learning dashboard:", err);
        animateRing(60);
      });
  }

  document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();
  });
  if(document.readyState==='complete'||document.readyState==='interactive'){
    setTimeout(loadDashboardData, 50);
  }
})();
