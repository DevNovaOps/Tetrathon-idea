/* ===================================================
   FINORA — Page 7: AI Assistant Script
   API Integration & Dynamic Chat Interface
   =================================================== */

(function () {
  'use strict';

  const chatMessages = document.getElementById('chatMessages');
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const typingIndicator = document.getElementById('typingIndicator');
  
  let currentStep = 1;
  let isAwaitingResponse = false;
  let isConversationComplete = false;

  // Initialize
  document.addEventListener('DOMContentLoaded', () => {
    // Clear static chat
    if (chatMessages) {
        // Keep only typing indicator if present, but for simplicity let's wipe and append it dynamically
        chatMessages.innerHTML = ''; 
        startConversation();
    }
  });

  async function apiCall(endpoint, method = 'GET', body = null) {
      const options = {
          method,
          headers: {
              'Content-Type': 'application/json',
              'X-Requested-With': 'XMLHttpRequest'
          }
      };
      if (body) options.body = JSON.stringify(body);
      
      const res = await fetch(endpoint, options);
      if (res.status === 401 || res.status === 403) {
          window.location.href = '../01-landing-page/index.html';
          throw new Error("Unauthorized");
      }
      return await res.json();
  }

  function showTyping() {
      const typingHtml = `
      <div class="message ai-message fade-in" id="dynamicTyping">
        <div class="msg-avatar ai-avatar">🤖</div>
        <div class="msg-bubble ai-bubble typing-bubble">
          <div class="typing-dots"><span></span><span></span><span></span></div>
        </div>
      </div>`;
      chatMessages.insertAdjacentHTML('beforeend', typingHtml);
      scrollToBottom();
  }

  function hideTyping() {
      const typingEl = document.getElementById('dynamicTyping');
      if (typingEl) typingEl.remove();
  }

  function scrollToBottom() {
      setTimeout(() => { chatMessages.scrollTop = chatMessages.scrollHeight; }, 100);
  }

  function getTime() {
      const now = new Date();
      let h = now.getHours();
      let m = now.getMinutes();
      const ampm = h >= 12 ? 'PM' : 'AM';
      h = h % 12 || 12;
      m = m < 10 ? '0' + m : m;
      return `${h}:${m} ${ampm}`;
  }

  function appendAIMessage(message, choices = null) {
      let chipsHtml = '';
      if (choices && choices.length > 0) {
          chipsHtml = `<div class="suggestion-chips">`;
          choices.forEach(choice => {
              chipsHtml += `<span class="chip" onclick="window.selectChip('${choice}')">${choice}</span>`;
          });
          chipsHtml += `</div>`;
      }
      
      const html = `
      <div class="message ai-message fade-in">
        <div class="msg-avatar ai-avatar">🤖</div>
        <div class="msg-bubble ai-bubble">
          <p>${message.replace(/\\n/g, '<br>')}</p>
          ${chipsHtml}
          <span class="msg-time">${getTime()}</span>
        </div>
      </div>`;
      
      chatMessages.insertAdjacentHTML('beforeend', html);
      scrollToBottom();
  }

  function appendUserMessage(message) {
      const html = `
      <div class="message user-message fade-in">
        <div class="msg-bubble user-bubble">
          <p>${message}</p>
          <span class="msg-time">${getTime()}</span>
        </div>
        <div class="msg-avatar user-avatar">D</div>
      </div>`;
      
      chatMessages.insertAdjacentHTML('beforeend', html);
      scrollToBottom();
  }
  
  function appendFinalSummary(summaryStr, riskLevel) {
      const html = `
      <div class="message ai-message fade-in">
        <div class="msg-avatar ai-avatar">🤖</div>
        <div class="msg-bubble ai-bubble summary-bubble">
          <p>✅ Assessment Complete!</p>
          <p>${summaryStr.replace(/\\n/g, '<br>')}</p>
          <a href="../08-risk-profile/risk-profile.html" class="btn btn-primary btn-inline" style="margin-top:10px;">View Risk Profile →</a>
          <span class="msg-time">${getTime()}</span>
        </div>
      </div>`;
      
      chatMessages.insertAdjacentHTML('beforeend', html);
      scrollToBottom();
      
      // Update Right Panel
      document.querySelector('.summary-sub').textContent = "Assessment Complete";
      const statusText = document.querySelector('.status-text');
      if (statusText) statusText.textContent = `Risk Level: ${riskLevel}`;
      
      // Update Stepper
      updateStepper(7);
  }

  function updateStepper(stepNum) {
      document.querySelectorAll('.stepper-step').forEach(stepEl => {
          const s = parseInt(stepEl.getAttribute('data-step'));
          if (s < stepNum) {
              stepEl.classList.add('done');
              stepEl.classList.remove('active');
              // Replace dot with checkmark
              const dot = stepEl.querySelector('.step-dot');
              if (dot) dot.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>';
          } else if (s === stepNum) {
              stepEl.classList.add('active');
              stepEl.classList.remove('done');
          } else {
              stepEl.classList.remove('active');
              stepEl.classList.remove('done');
          }
      });
  }

  async function startConversation() {
      showTyping();
      isAwaitingResponse = true;
      try {
          const res = await apiCall('/api/assistant/start/', 'POST');
          hideTyping();
          if (res.success && res.data) {
              if (res.data.assistant_message) {
                  appendAIMessage(res.data.assistant_message);
              }
              if (res.data.question) {
                  setTimeout(() => appendAIMessage(res.data.question, res.data.choices), 800);
              }
              updateStepper(res.data.step);
              currentStep = res.data.step;
          }
      } catch (e) {
          hideTyping();
          appendAIMessage("Connection error. Please try again later.");
      }
      isAwaitingResponse = false;
  }

  async function sendMessage(text) {
      if (!text.trim() || isAwaitingResponse || isConversationComplete) return;
      
      appendUserMessage(text);
      chatInput.value = '';
      showTyping();
      isAwaitingResponse = true;
      
      // Update summary list optimistically based on current step
      updateSummaryPanelOptimistic(text);
      
      try {
          const res = await apiCall('/api/assistant/message/', 'POST', { answer: text });
          hideTyping();
          if (res.success && res.data) {
              if (res.data.completed) {
                  isConversationComplete = true;
                  appendFinalSummary(res.data.summary, res.data.risk_profile.level);
              } else {
                  if (res.data.assistant_message) {
                      appendAIMessage(res.data.assistant_message);
                  }
                  if (res.data.question) {
                      setTimeout(() => appendAIMessage(res.data.question, res.data.choices), 800);
                  }
                  updateStepper(res.data.step);
                  currentStep = res.data.step;
              }
          }
      } catch (e) {
          hideTyping();
          appendAIMessage("Sorry, I encountered an error processing your response.");
      }
      isAwaitingResponse = false;
  }

  // Handle global chip click
  window.selectChip = function(text) {
      sendMessage(text);
  };

  if (sendBtn) {
      sendBtn.addEventListener('click', () => sendMessage(chatInput.value));
  }
  
  if (chatInput) {
      chatInput.addEventListener('keypress', (e) => {
          if (e.key === 'Enter') sendMessage(chatInput.value);
      });
  }

  // Populate Summary List based on step (rough approximation for immediate visual feedback)
  const summaryLabels = [
      "Monthly Income", "Monthly Expenses", "Savings", "Emergency Fund", "Investment Exp.", "Risk Preference"
  ];
  function updateSummaryPanelOptimistic(text) {
      const idx = currentStep - 1;
      if (idx >= 0 && idx < 6) {
          const items = document.querySelectorAll('.summary-item .sum-value');
          if (items[idx]) {
              items[idx].textContent = text;
              items[idx].classList.add('green-text'); // highlight update
          }
      }
  }

})();
