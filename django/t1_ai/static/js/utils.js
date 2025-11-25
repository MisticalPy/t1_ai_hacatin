/**
 * Утилиты и вспомогательные функции
 */

/**
 * Загружает HTML компонент в указанный элемент
 * @param {string} elementId - ID элемента, в который загружается компонент
 * @param {string} filePath - Путь к HTML файлу компонента
 */
function loadComponent(elementId, filePath) {
    return fetch(filePath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка загрузки компонента: ${response.statusText}`);
            }
            return response.text();
        })
        .then(html => {
            const element = document.getElementById(elementId);
            if (element) {
                element.innerHTML = html;
                return true;
            } else {
                console.warn(`Элемент с ID "${elementId}" не найден`);
                return false;
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке компонента:', error);
            return false;
        });
}

/**
 * Устанавливает активную ссылку в навигации на основе текущего URL
 */
function setActiveNavLink() {
    const currentPath = window.location.pathname;
    const currentPage = currentPath.split('/').pop() || 'index.html';
    
    const navLinks = document.querySelectorAll('.nav__link');
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentPage || 
            (currentPage === '' && linkPath === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * Дебаунс функция для оптимизации событий
 * @param {Function} func - Функция для выполнения
 * @param {number} wait - Время ожидания в миллисекундах
 * @returns {Function} - Дебаунсированная функция
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Проверяет, является ли устройство мобильным
 * @returns {boolean}
 */
function isMobile() {
    return window.innerWidth <= 768;
}

/**
 * Плавная прокрутка к элементу
 * @param {string} selector - CSS селектор элемента
 */
function scrollToElement(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

