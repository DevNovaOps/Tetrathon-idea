/**
 * Finora Auth — script.js
 * Theme toggle, form switching, password toggles, ripple, parallax
 */

document.addEventListener('DOMContentLoaded', () => {

    /* ─── Theme Toggle (same pattern as 01-landing-page) ───────── */
    const html        = document.documentElement;
    const themeToggle = document.getElementById('themeToggle');

    function getStoredTheme() {
        try { return localStorage.getItem('finora-theme'); }
        catch (e) { return null; }
    }

    function setTheme(theme) {
        html.setAttribute('data-theme', theme);
        try { localStorage.setItem('finora-theme', theme); }
        catch (e) { /* ignore */ }
    }

    // Initialise — default dark, but respect stored preference
    (function initTheme() {
        const stored = getStoredTheme();
        setTheme(stored || 'dark');
    })();

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const current = html.getAttribute('data-theme');
            setTheme(current === 'dark' ? 'light' : 'dark');

            // Small spin animation on toggle
            themeToggle.style.transform = 'scale(0.85) rotate(180deg)';
            setTimeout(() => {
                themeToggle.style.transform = '';
            }, 280);
        });
    }

    /* ─── Form Elements ─────────────────────────────────────────── */
    const loginForm  = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const goToSignup = document.getElementById('goToSignup');
    const goToLogin  = document.getElementById('goToLogin');

    /* ─── Form Switching ────────────────────────────────────────── */
    function switchTo(outForm, inForm, outClass, inClass) {
        outForm.classList.remove('active', 'enter-right', 'enter-left');
        inForm.classList.remove('enter-right', 'enter-left');

        outForm.classList.add(outClass);

        setTimeout(() => {
            outForm.classList.remove(outClass, 'active');
            outForm.style.display = 'none';

            inForm.style.display = 'flex';
            inForm.classList.add(inClass);

            requestAnimationFrame(() => {
                setTimeout(() => {
                    inForm.classList.remove(inClass);
                    inForm.classList.add('active');
                }, 20);
            });
        }, 330);
    }

    if (goToSignup) {
        goToSignup.addEventListener('click', () => {
            switchTo(loginForm, signupForm, 'exit-left', 'enter-right');
        });
    }
    if (goToLogin) {
        goToLogin.addEventListener('click', () => {
            switchTo(signupForm, loginForm, 'exit-right', 'enter-left');
        });
    }

    /* ─── Password Toggles ──────────────────────────────────────── */
    function setupPasswordToggle(toggleId, inputId) {
        const toggle = document.getElementById(toggleId);
        const input  = document.getElementById(inputId);
        if (!toggle || !input) return;

        toggle.addEventListener('click', () => {
            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';
            const eyeOpen   = toggle.querySelector('.eye-open');
            const eyeClosed = toggle.querySelector('.eye-closed');
            if (eyeOpen)   eyeOpen.style.display   = isPassword ? 'none'  : 'block';
            if (eyeClosed) eyeClosed.style.display  = isPassword ? 'block' : 'none';
        });
    }

    setupPasswordToggle('loginPwdToggle',      'loginPassword');
    setupPasswordToggle('signupPwdToggle',     'signupPassword');
    setupPasswordToggle('signupConfirmToggle', 'signupConfirm');

    /* ─── Ripple on Primary Buttons ─────────────────────────────── */
    document.querySelectorAll('.btn-primary').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const container = btn.querySelector('.btn-ripple');
            if (!container) return;

            const ripple = document.createElement('span');
            ripple.classList.add('ripple-effect');

            const rect = btn.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x    = e.clientX - rect.left  - size / 2;
            const y    = e.clientY - rect.top   - size / 2;

            Object.assign(ripple.style, {
                width:  size + 'px',
                height: size + 'px',
                left:   x    + 'px',
                top:    y    + 'px',
            });

            container.appendChild(ripple);
            ripple.addEventListener('animationend', () => ripple.remove());
        });
    });

    /* ─── Parallax / 3D tilt on Lock Cube ─────────────────────── */
    const cube      = document.getElementById('lockCube');
    const authRight = document.getElementById('authRight');

    if (cube && authRight) {
        let targetX = 0, targetY = 0, curX = 0, curY = 0;

        authRight.addEventListener('mousemove', (e) => {
            const r  = authRight.getBoundingClientRect();
            targetX  = ((e.clientX - r.left  - r.width  / 2) / r.width)  * 16;
            targetY  = ((e.clientY - r.top   - r.height / 2) / r.height) * 16;
        });

        authRight.addEventListener('mouseleave', () => {
            targetX = 0; targetY = 0;
        });

        (function animateCube() {
            curX += (targetX - curX) * 0.08;
            curY += (targetY - curY) * 0.08;
            cube.style.transform = `rotateY(${curX}deg) rotateX(${-curY}deg)`;
            requestAnimationFrame(animateCube);
        })();
    }

    /* ─── Prevent default submit ────────────────────────────────── */
    document.querySelectorAll('form').forEach(f => {
        f.addEventListener('submit', e => e.preventDefault());
    });

});
