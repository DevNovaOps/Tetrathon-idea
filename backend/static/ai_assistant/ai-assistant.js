/* ===================================================
   FINORA — Page 7: AI Financial Assistant Scripts
   Theme Toggle, Sidebar, Reveal, Chat API Integration
   =================================================== */
(function () {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const mobileToggle = document.getElementById('mobileToggle');
  const sidebar = document.getElementById('sidebar');
  const chatMessages = document.getElementById('chatMessages');
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const typingIndicator = document.getElementById('typingIndicator');

  let conversationId = null;
  let isWaiting = false;

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
    const trigger = window.innerHeight * 0.95;
    document.querySelectorAll('.reveal').forEach(el => { if (el.getBoundingClientRect().top < trigger) el.classList.add('visible'); });
  }
  window.addEventListener('scroll', checkReveals, { passive: true });
  window.addEventListener('load', checkReveals);
  setTimeout(checkReveals, 100);

  /* ---- HELPERS ---- */
  function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, 10) === 'csrftoken=') {
          cookieValue = decodeURIComponent(cookie.substring(10));
          break;
        }
      }
    }
    return cookieValue;
  }

  function now() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
  }

  function scrollToBottom() {
    if (chatMessages) setTimeout(() => { chatMessages.scrollTop = chatMessages.scrollHeight; }, 100);
  }

  function showTyping() {
    if (typingIndicator) typingIndicator.style.display = 'flex';
    scrollToBottom();
  }

  function hideTyping() {
    if (typingIndicator) typingIndicator.style.display = 'none';
  }

  function clearStaticMessages() {
    // Remove all static placeholder messages from the HTML
    const msgs = chatMessages.querySelectorAll('.message');
    msgs.forEach(m => {
      if (m.id !== 'typingIndicator') m.remove();
    });
  }

  function addAIMessage(text, chips, isSummary) {
    let chipsHtml = '';
    if (chips && chips.length > 0) {
      chipsHtml = '<div class="suggestion-chips">' +
        chips.map(c => `<span class="chip">${c}</span>`).join('') +
        '</div>';
    }

    let summaryClass = isSummary ? ' summary-bubble' : '';
    let summaryBtn = '';
    if (isSummary) {
      summaryBtn = '<a href="../08-risk-profile/risk-profile.html" class="btn btn-primary btn-inline">View Risk Assessment →</a>';
    }

    const msgHtml = `
    <div class="message ai-message fade-in">
      <div class="msg-avatar ai-avatar">🤖</div>
      <div class="msg-bubble ai-bubble${summaryClass}">
        <div class="msg-sender">Finora AI</div>
        <p>${text.replace(/\n/g, '<br>')}</p>
        ${chipsHtml}
        ${summaryBtn}
        <span class="msg-time">${now()}</span>
      </div>
    </div>`;
    typingIndicator.insertAdjacentHTML('beforebegin', msgHtml);
    bindChips();
    scrollToBottom();
  }

  function addUserMessage(text) {
    const msgHtml = `
    <div class="message user-message fade-in">
      <div class="msg-bubble user-bubble">
        <p>${text}</p>
        <span class="msg-time">${now()}</span>
      </div>
      <div class="msg-avatar user-avatar">D</div>
    </div>`;
    typingIndicator.insertAdjacentHTML('beforebegin', msgHtml);
    scrollToBottom();
    // Return the newly inserted message element
    return typingIndicator.previousElementSibling;
  }

  /* ---- STEPPER UPDATE ---- */
  function updateStepper(step) {
    const steps = document.querySelectorAll('.stepper-step');
    steps.forEach((el, i) => {
      el.classList.remove('done', 'active');
      if (i < step - 1) {
        el.classList.add('done');
        // Replace dot content with check SVG
        const dot = el.querySelector('.step-dot');
        if (dot) dot.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>';
      } else if (i === step - 1) {
        el.classList.add('active');
        const dot = el.querySelector('.step-dot');
        if (dot) dot.textContent = step;
      } else {
        const dot = el.querySelector('.step-dot');
        if (dot) dot.textContent = i + 1;
      }
    });
  }

  /* ---- SUMMARY PANEL UPDATE ---- */
  function updateSummaryPanel(items) {
    if (!items || items.length === 0) return;
    const list = document.querySelector('.summary-list');
    if (!list) return;
    list.innerHTML = '';
    items.forEach(item => {
      list.innerHTML += `
      <div class="summary-item">
        <span class="sum-label">${item.label}</span>
        <span class="sum-value">${item.value}</span>
      </div>`;
    });
  }

  function updateSummaryStatus(completed) {
    const statusText = document.querySelector('.status-text');
    if (statusText) {
      statusText.textContent = completed ? 'Assessment Complete' : 'In Progress...';
    }
  }

  /* ---- CHIP CLICK HANDLER ---- */
  function bindChips() {
    document.querySelectorAll('.chip').forEach(chip => {
      chip.addEventListener('click', function handler() {
        if (isWaiting) return;
        sendAnswer(this.textContent.trim());
        this.removeEventListener('click', handler);
      });
    });
  }

  /* ---- SEND ANSWER ---- */
  async function sendAnswer(answer) {
    if (isWaiting || !answer.trim()) return;
    isWaiting = true;

    const userMsgEl = addUserMessage(answer);
    if (chatInput) chatInput.value = '';
    showTyping();

    try {
      const res = await fetch('/api/assistant/message/', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json', 
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ answer: answer })
      });

      if (res.status === 401 || res.status === 403) {
        window.location.href = '/';
        return;
      }

      const json = await res.json();
      hideTyping();

      if (json.success && json.data) {
        const d = json.data;
        conversationId = d.conversation_id;

        // If the backend parsed and formatted the answer, update the user bubble
        if (d.formatted_answer && userMsgEl) {
          const p = userMsgEl.querySelector('p');
          if (p) p.textContent = d.formatted_answer;
        }

        if (d.error) {
          addAIMessage(d.assistant_message, d.chips, false);
          isWaiting = false;
          return;
        }

        if (d.step) updateStepper(d.step);
        if (d.summary_items) updateSummaryPanel(d.summary_items);

        if (d.completed) {
          // Final summary
          addAIMessage(d.assistant_message, null, true);
          updateSummaryStatus(true);
          disableInput();
        } else {
          addAIMessage(d.assistant_message, d.chips, false);
        }
      }
    } catch (err) {
      hideTyping();
      addAIMessage("I'm having trouble connecting. Please try again.", null, false);
      console.error('API Error:', err);
    }
    isWaiting = false;
  }

  function disableInput() {
    if (chatInput) { chatInput.disabled = true; chatInput.placeholder = 'Assessment complete!'; }
    if (sendBtn) sendBtn.disabled = true;
  }

  /* ---- START CONVERSATION ---- */
  async function startConversation() {
    clearStaticMessages();
    showTyping();

    try {
      const res = await fetch('/api/assistant/start/', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json', 
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCSRFToken()
        }
      });

      if (res.status === 401 || res.status === 403) {
        window.location.href = '/';
        return;
      }

      const json = await res.json();
      hideTyping();

      if (json.success && json.data) {
        const d = json.data;
        conversationId = d.conversation_id;

        if (d.resumed && d.messages) {
          // Re-render existing messages
          d.messages.forEach(msg => {
            if (msg.role === 'assistant') addAIMessage(msg.content, null, false);
            else addUserMessage(msg.content);
          });
          // Show current question with chips
          if (d.question) addAIMessage(d.question, d.chips, false);
          if (d.step) updateStepper(d.step);
          if (d.summary_items) updateSummaryPanel(d.summary_items);
        } else {
          // Fresh start — greeting + first question
          addAIMessage(d.assistant_message, null, false);
          if (d.question) addAIMessage(d.question, d.chips, false);
          updateStepper(1);
        }
      }
    } catch (err) {
      hideTyping();
      addAIMessage("Welcome! Let's begin your financial assessment.", null, false);
      console.error('Start Error:', err);
    }
  }

  /* ---- INPUT HANDLERS ---- */
  if (sendBtn) {
    sendBtn.addEventListener('click', () => {
      if (chatInput && chatInput.value.trim()) sendAnswer(chatInput.value.trim());
    });
  }
  if (chatInput) {
    chatInput.addEventListener('keydown', e => {
      if (e.key === 'Enter' && chatInput.value.trim()) sendAnswer(chatInput.value.trim());
    });
  }

  /* ---- INIT ---- */
  document.addEventListener('DOMContentLoaded', startConversation);
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    startConversation();
  }

})();
