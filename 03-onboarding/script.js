/* ===================================================
   FINORA — Multi-Step Onboarding Script
   Step Transitions, Progress Bar, Live Summary Sync
   =================================================== */

(function () {
  'use strict';

  /* ---------- STEP CONFIGURATION ---------- */
  const stepsConfig = [
    {
      step: 1,
      title: "Let's Get To Know You",
      subtitle: "Tell us about yourself.",
      progress: "25%",
      nextText: "Next",
      showSkip: true
    },
    {
      step: 2,
      title: "Tell Us About Your Finances",
      subtitle: "Help us understand your financial profile.",
      progress: "50%",
      nextText: "Next",
      showSkip: false
    },
    {
      step: 3,
      title: "Investment Preferences",
      subtitle: "Help us personalize your investment recommendations.",
      progress: "75%",
      nextText: "Next",
      showSkip: false
    },
    {
      step: 4,
      title: "Almost Done",
      subtitle: "Review your information before continuing.",
      progress: "100%",
      nextText: "Finish",
      showSkip: false
    }
  ];

  let currentStep = 1;

  /* ---------- DOM REFERENCES ---------- */
  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const stepIndicator = document.getElementById('stepIndicator');
  const percentageBadge = document.getElementById('percentageBadge');
  const stepTitle = document.getElementById('stepTitle');
  const stepSubtitle = document.getElementById('stepSubtitle');
  const progressFill = document.getElementById('progressFill');

  const btnPrev = document.getElementById('btnPrev');
  const btnNext = document.getElementById('btnNext');
  const btnSkip = document.getElementById('btnSkip');
  const nextBtnText = document.getElementById('nextBtnText');
  const nextBtnIcon = document.getElementById('nextBtnIcon');

  /* ---------- THEME TOGGLE ---------- */
  function getStoredTheme() {
    try {
      return localStorage.getItem('finora-theme');
    } catch (e) {
      return null;
    }
  }

  function updateOnboardingVideo(theme) {
    var video = document.getElementById('onboarding-avatar-video');
    var source = document.getElementById('onboarding-video-src');
    if (video && source) {
      var isDjango = source.getAttribute('data-django') === 'true';
      var basePath = isDjango ? '/static/video/' : './video/';
      var newSrc = basePath + (theme === 'light' ? 'onboarding_white.mp4' : 'onboarding_black.mp4');
      if (source.getAttribute('src') !== newSrc) {
        source.setAttribute('src', newSrc);
        video.load();
        video.play().catch(function() {});
      }
    }
  }

  function setTheme(theme) {
    html.setAttribute('data-theme', theme);
    try {
      localStorage.setItem('finora-theme', theme);
    } catch (e) {
      // silently fail
    }
    updateOnboardingVideo(theme);
  }

  (function initTheme() {
    var stored = getStoredTheme();
    if (stored) {
      setTheme(stored);
    } else {
      setTheme('dark');
    }
  })();

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      var current = html.getAttribute('data-theme');
      setTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  /* ---------- LIVE SUMMARY SYNC FOR STEP 4 ---------- */
  function syncSummaryData() {
    // Helper to safety fetch value
    const getVal = (id) => {
      const el = document.getElementById(id);
      return el ? el.value : '';
    };

    // Personal Info
    const sumName = document.getElementById('sumName');
    const sumAge = document.getElementById('sumAge');
    const sumGender = document.getElementById('sumGender');
    const sumOcc = document.getElementById('sumOcc');
    const sumCity = document.getElementById('sumCity');
    const sumLang = document.getElementById('sumLang');

    if (sumName) sumName.textContent = getVal('fullName') || 'Dev Sharma';
    if (sumAge) sumAge.textContent = getVal('age') || '23';
    if (sumGender) sumGender.textContent = getVal('gender') || 'Male';
    if (sumOcc) sumOcc.textContent = getVal('occupation') || 'Student / Freelancer';
    if (sumCity) sumCity.textContent = getVal('city') || 'Vadodara';
    if (sumLang) sumLang.textContent = getVal('language') || 'English';

    // Financial Info
    const sumIncome = document.getElementById('sumIncome');
    const sumExpenses = document.getElementById('sumExpenses');
    const sumSavings = document.getElementById('sumSavings');
    const sumLoans = document.getElementById('sumLoans');
    const sumUpi = document.getElementById('sumUpi');
    const sumBill = document.getElementById('sumBill');

    if (sumIncome) sumIncome.textContent = getVal('monthlyIncome') || '₹45,000';
    if (sumExpenses) sumExpenses.textContent = getVal('monthlyExpenses') || '₹18,000';
    if (sumSavings) sumSavings.textContent = getVal('savings') || '₹1,25,000';
    if (sumLoans) sumLoans.textContent = getVal('existingLoans') || 'None';
    if (sumUpi) sumUpi.textContent = getVal('upiUsage') || 'Daily (15+ txns/wk)';
    if (sumBill) sumBill.textContent = getVal('billHabit') || 'Always On-Time';

    // Investment Info
    const sumExp = document.getElementById('sumExp');
    const sumEmerg = document.getElementById('sumEmerg');
    const sumBudget = document.getElementById('sumBudget');
    const sumGoal = document.getElementById('sumGoal');
    const sumRisk = document.getElementById('sumRisk');

    if (sumExp) sumExp.textContent = getVal('investExp') || 'Intermediate (1-3 yrs)';
    if (sumEmerg) sumEmerg.textContent = getVal('emergencyFund') || 'Yes (6 Months Saved)';
    if (sumBudget) sumBudget.textContent = getVal('investBudget') || '₹10,000 / month';
    if (sumGoal) sumGoal.textContent = getVal('financialGoal') || 'Wealth Accumulation';
    if (sumRisk) sumRisk.textContent = getVal('riskPref') || 'Moderate';
  }

  /* ---------- UPDATE WIZARD UI ---------- */
  function updateWizard(stepIndex) {
    const config = stepsConfig[stepIndex - 1];

    // Hide all step panes
    document.querySelectorAll('.step-pane').forEach((pane) => {
      pane.classList.remove('active');
    });

    // Activate current pane
    const currentPane = document.getElementById('stepPane' + stepIndex);
    if (currentPane) {
      currentPane.classList.add('active');
    }

    // Sync header text & progress bar
    if (stepIndicator) stepIndicator.textContent = `Step ${config.step} of 4`;
    if (percentageBadge) percentageBadge.textContent = config.progress;
    if (stepTitle) stepTitle.textContent = config.title;
    if (stepSubtitle) stepSubtitle.textContent = config.subtitle;
    if (progressFill) progressFill.style.width = config.progress;

    // Update buttons
    if (stepIndex === 1) {
      if (btnPrev) btnPrev.style.display = 'none';
      if (btnSkip) btnSkip.style.display = 'inline-flex';
    } else {
      if (btnPrev) btnPrev.style.display = 'inline-flex';
      if (btnSkip) btnSkip.style.display = 'none';
    }

    if (nextBtnText) nextBtnText.textContent = config.nextText;
    if (nextBtnIcon) {
      if (config.step === 4) {
        nextBtnIcon.style.display = 'none';
      } else {
        nextBtnIcon.style.display = 'inline-block';
      }
    }

    // Sync summary review when reaching Step 4
    if (stepIndex === 4) {
      syncSummaryData();
    }
  }

  /* ============================================================
     BACKEND INTEGRATION — Fetch API
     ============================================================ */

  const API_BASE = window.location.origin;

  /** Read Django CSRF token from the cookie. */
  function getCSRFToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
  }

  /** Remove error messages. */
  function clearErrors() {
    document.querySelectorAll('.field-error').forEach(el => el.remove());
  }

  /** Show error below a field. */
  function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    const wrapper = field.closest('.form-group');
    if (!wrapper) return;
    const existing = wrapper.querySelector('.field-error');
    if (existing) existing.remove();
    const errorEl = document.createElement('span');
    errorEl.className = 'field-error';
    errorEl.style.cssText = 'color:#ef4444;font-size:12px;margin-top:4px;display:block;';
    errorEl.textContent = message;
    wrapper.appendChild(errorEl);
  }

  /** Backend field → frontend input ID maps. */
  const STEP1_FIELD_MAP = {
    full_name: 'fullName',
    age: 'age',
    gender: 'gender',
    occupation: 'occupation',
    city: 'city',
    preferred_language: 'language',
  };

  const STEP2_FIELD_MAP = {
    monthly_income: 'monthlyIncome',
    monthly_expenses: 'monthlyExpenses',
    savings: 'savings',
    existing_loans: 'existingLoans',
    upi_usage: 'upiUsage',
    bill_payment_habit: 'billHabit',
  };

  const STEP3_FIELD_MAP = {
    investment_experience: 'investExp',
    emergency_fund: 'emergencyFund',
    monthly_investment_budget: 'investBudget',
    financial_goal: 'financialGoal',
    risk_preference: 'riskPref',
    investment_duration: 'investDuration',
  };

  /** Display backend errors. */
  function renderErrors(errors, fieldMap) {
    clearErrors();
    for (const [field, messages] of Object.entries(errors)) {
      const frontId = fieldMap[field] || field;
      const msg = Array.isArray(messages) ? messages[0] : messages;
      showFieldError(frontId, msg);
    }
  }

  /** POST a step's data and return the parsed response. */
  async function postStep(endpoint, payload) {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify(payload),
    });
    return res.json();
  }

  /** Collect Step 1 form data. */
  function getStep1Data() {
    return {
      full_name: document.getElementById('fullName')?.value.trim() || '',
      age: parseInt(document.getElementById('age')?.value, 10) || 0,
      gender: document.getElementById('gender')?.value || '',
      occupation: document.getElementById('occupation')?.value.trim() || '',
      city: document.getElementById('city')?.value.trim() || '',
      preferred_language: document.getElementById('language')?.value || '',
    };
  }

  /** Collect Step 2 form data. */
  function getStep2Data() {
    return {
      monthly_income: document.getElementById('monthlyIncome')?.value.trim() || '',
      monthly_expenses: document.getElementById('monthlyExpenses')?.value.trim() || '',
      savings: document.getElementById('savings')?.value.trim() || '',
      existing_loans: document.getElementById('existingLoans')?.value || '',
      upi_usage: document.getElementById('upiUsage')?.value || '',
      bill_payment_habit: document.getElementById('billHabit')?.value || '',
    };
  }

  /** Collect Step 3 form data. */
  function getStep3Data() {
    return {
      investment_experience: document.getElementById('investExp')?.value || '',
      emergency_fund: document.getElementById('emergencyFund')?.value || '',
      monthly_investment_budget: document.getElementById('investBudget')?.value.trim() || '',
      financial_goal: document.getElementById('financialGoal')?.value || '',
      risk_preference: document.getElementById('riskPref')?.value || '',
      investment_duration: document.getElementById('investDuration')?.value || '',
    };
  }

  /** Set a form field's value safely. */
  function setVal(id, value) {
    const el = document.getElementById(id);
    if (el && value !== null && value !== undefined && value !== '') {
      el.value = value;
    }
  }

  /** Populate form fields from saved profile data (for resume). */
  function populateFromProfile(data) {
    // Step 1
    setVal('fullName', data.full_name);
    setVal('age', data.age);
    setVal('gender', data.gender);
    setVal('occupation', data.occupation);
    setVal('city', data.city);
    setVal('language', data.preferred_language);

    // Step 2
    setVal('monthlyIncome', data.monthly_income);
    setVal('monthlyExpenses', data.monthly_expenses);
    setVal('savings', data.savings);
    setVal('existingLoans', data.existing_loans);
    setVal('upiUsage', data.upi_usage);
    setVal('billHabit', data.bill_payment_habit);

    // Step 3
    setVal('investExp', data.investment_experience);
    setVal('emergencyFund', data.emergency_fund);
    setVal('investBudget', data.monthly_investment_budget);
    setVal('financialGoal', data.financial_goal);
    setVal('riskPref', data.risk_preference);
    setVal('investDuration', data.investment_duration);
  }

  /** Set button to loading state. */
  function setLoading(isLoading) {
    if (!btnNext) return;
    if (isLoading) {
      btnNext.disabled = true;
      btnNext.style.opacity = '0.7';
      if (nextBtnText) nextBtnText.textContent = 'Saving…';
    } else {
      btnNext.disabled = false;
      btnNext.style.opacity = '';
      // Text will be restored by updateWizard
    }
  }

  /* ---------- BUTTON EVENT LISTENERS ---------- */
  if (btnNext) {
    btnNext.addEventListener('click', async function (e) {
      e.preventDefault();
      clearErrors();

      if (currentStep === 1) {
        // ── Save Step 1, then advance ──
        setLoading(true);
        try {
          const result = await postStep('/api/onboarding/step1/', getStep1Data());
          if (result.success) {
            currentStep = 2;
            updateWizard(currentStep);
          } else if (result.errors) {
            renderErrors(result.errors, STEP1_FIELD_MAP);
          } else {
            showFieldError('fullName', result.message || 'Save failed.');
          }
        } catch (err) {
          console.error('Step 1 error:', err);
          showFieldError('fullName', 'Network error. Please try again.');
        } finally {
          setLoading(false);
          updateWizard(currentStep);
        }

      } else if (currentStep === 2) {
        // ── Save Step 2, then advance ──
        setLoading(true);
        try {
          const result = await postStep('/api/onboarding/step2/', getStep2Data());
          if (result.success) {
            currentStep = 3;
            updateWizard(currentStep);
          } else if (result.errors) {
            renderErrors(result.errors, STEP2_FIELD_MAP);
          } else {
            showFieldError('monthlyIncome', result.message || 'Save failed.');
          }
        } catch (err) {
          console.error('Step 2 error:', err);
          showFieldError('monthlyIncome', 'Network error. Please try again.');
        } finally {
          setLoading(false);
          updateWizard(currentStep);
        }

      } else if (currentStep === 3) {
        // ── Save Step 3, then advance ──
        setLoading(true);
        try {
          const result = await postStep('/api/onboarding/step3/', getStep3Data());
          if (result.success) {
            currentStep = 4;
            updateWizard(currentStep);
          } else if (result.errors) {
            renderErrors(result.errors, STEP3_FIELD_MAP);
          } else {
            showFieldError('investExp', result.message || 'Save failed.');
          }
        } catch (err) {
          console.error('Step 3 error:', err);
          showFieldError('investExp', 'Network error. Please try again.');
        } finally {
          setLoading(false);
          updateWizard(currentStep);
        }

      } else if (currentStep === 4) {
        // ── Finish onboarding ──
        setLoading(true);
        try {
          const result = await postStep('/api/onboarding/finish/', {});
          if (result.success) {
            window.location.href = result.data.redirect;
          } else {
            alert(result.message || 'Could not finish onboarding.');
          }
        } catch (err) {
          console.error('Finish error:', err);
          alert('Network error. Please try again.');
        } finally {
          setLoading(false);
        }
      }
    });
  }

  if (btnPrev) {
    btnPrev.addEventListener('click', function (e) {
      e.preventDefault();
      if (currentStep > 1) {
        currentStep--;
        clearErrors();
        updateWizard(currentStep);
      }
    });
  }

  if (btnSkip) {
    btnSkip.addEventListener('click', function (e) {
      e.preventDefault();
      if (currentStep < 4) {
        currentStep++;
        clearErrors();
        updateWizard(currentStep);
      }
    });
  }

  /* ---------- RESUME: Load saved data on page load ---------- */
  async function resumeOnboarding() {
    try {
      const res = await fetch(`${API_BASE}/api/onboarding/review/`, {
        credentials: 'same-origin',
      });
      if (!res.ok) return; // Not logged in or server error — start from step 1
      const json = await res.json();
      if (!json.success) return;

      const data = json.data;

      // If onboarding is already complete, redirect to dashboard
      if (data.onboarding_completed) {
        window.location.href = '/04-dashboard/dashboard.html';
        return;
      }

      // Populate form fields with saved data
      populateFromProfile(data);

      // Jump to the correct step
      if (data.current_step && data.current_step > 1) {
        currentStep = data.current_step;
        updateWizard(currentStep);
      }
    } catch (err) {
      console.error('Resume onboarding error:', err);
      // Fail silently — start from step 1
    }
  }

  // Initialize Step 1 on load, then try to resume
  updateWizard(1);
  resumeOnboarding();

})();
