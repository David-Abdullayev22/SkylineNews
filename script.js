// function goToAnotherPage() {
//     window.location.href = 'science_news.html';
// }

// function goToMainPage() {
//     window.location.href = 'index_news.html';
// }

document.getElementById('theme-toggle').addEventListener('click', function() {
    // Переключаем класс dark-mode на элементе body
    document.body.classList.toggle('dark-mode');

    // Переключаем классы на всех элементах, которые должны менять тему
    const elementsToToggle = document.querySelectorAll('header, container, footer, h1, h2, h3, p, .news-item, aside, .header-btn, .header-btn:hover, .btn, h6, .read-more-btn, .read-more-btn:hover');
    elementsToToggle.forEach(function(element) {
        element.classList.toggle('dark-mode');
    });

    // Сохраняем состояние темы в localStorage
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
});

// Устанавливаем тему при загрузке страницы
window.addEventListener('load', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');

        const elementsToToggle = document.querySelectorAll('header, container, footer, h1, h2, h3, p, .news-item, aside, .header-btn, .header-btn:hover, .btn, h6, .read-more-btn, .read-more-btn:hover');
        elementsToToggle.forEach(function(element) {
            element.classList.add('dark-mode');
        });
    }
});
