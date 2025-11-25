/**
 * Главный файл JavaScript
 * Инициализация всех компонентов при загрузке страницы
 */

// Импорт функций из других модулей
// В реальном проекте можно использовать ES6 модули с type="module"

/**
 * Инициализация приложения
 */
async function init() {
    // Загрузка общих компонентов
    await loadComponent('header', 'templates/header.html');
    await loadComponent('footer', 'templates/footer.html');
    
    // Инициализация навигации после загрузки header
    setTimeout(() => {
        initNavigation();
    }, 100);
    
    // Инициализация других компонентов
    initPageSpecific();
}

/**
 * Инициализация специфичных для страницы функций
 */
function initPageSpecific() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    // Можно добавить специфичную логику для каждой страницы
    switch(currentPage) {
        case 'index.html':
        case '':
            initHomePage();
            break;
        case 'about.html':
            initAboutPage();
            break;
        case 'vacancies.html':
            initVacanciesPage();
            break;
    }
}

/**
 * Инициализация главной страницы
 */
function initHomePage() {
    console.log('Инициализация главной страницы');
    // Добавьте специфичную логику для главной страницы
}

/**
 * Инициализация страницы "О нас"
 */
function initAboutPage() {
    console.log('Инициализация страницы "О нас"');
    // Добавьте специфичную логику для страницы "О нас"
}

/**
 * Инициализация страницы "Вакансии"
 */
function initVacanciesPage() {
    console.log('Инициализация страницы "Вакансии"');
    // Добавьте специфичную логику для страницы "Вакансии"
}

// Запуск приложения после загрузки DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Регистрация анимации
const tabs = document.querySelectorAll('.tab');
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');
        const registerBtn = document.getElementById('registerBtn');
        const registerAgreed = document.getElementById('registerAgreed');

        let activeTab = 'login';

        // Переключение вкладок
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const tabType = tab.getAttribute('data-tab');
                
                // Убираем активный класс со всех вкладок
                tabs.forEach(t => t.classList.remove('active'));
                
                // Добавляем активный класс на текущую вкладку
                tab.classList.add('active');
                
                // Обновляем активную вкладку
                activeTab = tabType;
                
                // Переключаем формы и сбрасываем их
                if (tabType === 'login') {
                    loginForm.classList.add('active');
                    registerForm.classList.remove('active');
                    loginForm.reset();
                } else {
                    registerForm.classList.add('active');
                    loginForm.classList.remove('active');
                    registerForm.reset();
                    registerBtn.disabled = !registerAgreed.checked;
                }
            });
        });

        // Обработка формы входа
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const loginData = {
                password: document.getElementById('loginPassword').value,
                phone: document.getElementById('loginPhone').value
            }
        });

        // Обработка формы регистрации
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const regData = {
                email: document.getElementById('registerEmail').value,
                password: document.getElementById('registerPassword').value,
                phone: document.getElementById('registerPhone').value,
                agreed: registerAgreed.checked
            }
        });

        // Управление состоянием кнопки регистрации
        registerAgreed.addEventListener('change', () => {
            registerBtn.disabled = !registerAgreed.checked;
        });
        
        // валидация форм