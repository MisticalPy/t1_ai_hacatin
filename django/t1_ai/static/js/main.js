/**
 * Главный файл JavaScript
 * Инициализация всех компонентов при загрузке страницы
 */

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

function init() {
    const tabs = document.querySelectorAll('.tab');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const registerBtn = document.getElementById('registerBtn');
    const registerAgreed = document.getElementById('registerAgreed');

    let activeTab = 'login';

    registerAgreed.addEventListener('change', () => {
        registerBtn.disabled = !registerAgreed.checked;
    });

    const loginBtn = document.querySelector('[data-tab="login"]');
    if (loginBtn) {
        loginBtn.addEventListener('click', () => {
            window.location.href = window.location.origin + '/users/login';
        });
    }

    const registerBtnEl = document.querySelector('[data-tab="register"]');
    if (registerBtnEl) {
        registerBtnEl.addEventListener('click', () => {
            window.location.href = window.location.origin + '/users/register';
        });
    }

    const getCookie = name =>
        document.cookie
            .split('; ')
            .find(row => row.startsWith(name + '='))
            ?.split('=')[1] || null;

    const logoutBtn = document.querySelector('.btn_logout');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            fetch('/users/logout/', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') }
            }).then(() => location.href = '/');
        });
    }
}
