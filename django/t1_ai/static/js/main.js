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

    // Чекбокс "согласен" для регистрации
    if (registerAgreed && registerBtn) {
        registerBtn.disabled = !registerAgreed.checked; // начальное состояние

        registerAgreed.addEventListener('change', () => {
            registerBtn.disabled = !registerAgreed.checked;
        });
    }

    // Переход на логин по табу
    const loginBtn = document.querySelector('[data-tab="login"]');
    if (loginBtn) {
        loginBtn.addEventListener('click', () => {
            window.location.href = window.location.origin + '/users/login';
        });
    }

    // Переход на регистрацию по табу
    const registerBtnEl = document.querySelector('[data-tab="register"]');
    if (registerBtnEl) {
        registerBtnEl.addEventListener('click', () => {
            window.location.href = window.location.origin + '/users/register';
        });
    }

    // Логаут по кнопке .btn_logout через fetch
    const logoutBtn = document.querySelector('.btn_logout');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();

            fetch('/users/logout/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            }).then(() => {
                window.location.href = '/';
            });
        });
    }
}

// Утилита для получения cookie (Django CSRF)
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}
