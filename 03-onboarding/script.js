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

  function setTheme(theme) {
    html.setAttribute('data-theme', theme);
    try {
      localStorage.setItem('finora-theme', theme);
    } catch (e) {
      // silently fail
    }
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

  /* ---------- BUTTON EVENT LISTENERS ---------- */
  if (btnNext) {
    btnNext.addEventListener('click', function (e) {
      e.preventDefault();
      if (currentStep < 4) {
        currentStep++;
        updateWizard(currentStep);
      } else {
        // UI only finish feedback
        btnNext.style.transform = 'scale(0.96)';
        setTimeout(() => { btnNext.style.transform = ''; }, 150);
      }
    });
  }

  if (btnPrev) {
    btnPrev.addEventListener('click', function (e) {
      e.preventDefault();
      if (currentStep > 1) {
        currentStep--;
        updateWizard(currentStep);
      }
    });
  }

  if (btnSkip) {
    btnSkip.addEventListener('click', function (e) {
      e.preventDefault();
      if (currentStep < 4) {
        currentStep++;
        updateWizard(currentStep);
      }
    });
  }

  // Initialize Step 1 on load
  updateWizard(1);

})();
