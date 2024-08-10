import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_news():
    base_url = 'https://www.gazeta.ru'
    url = urljoin(base_url, '/news/')
    print(f"Fetching URL: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Открытие основного HTML-шаблона
    with open('index.html', 'r', encoding='utf-8') as file:
        template_soup = BeautifulSoup(file, 'html.parser')
    
    # Поиск основного контейнера для новостей
    main_section = template_soup.find('main', id='news-content')

    if main_section is None:
        print("Main section with id 'news-content' not found in the template.")
        return

    # Очистка текущих новостей
    main_section.clear()

    # Добавление вводного текста
    intro_text = "Главные новости:"
    intro_tag = template_soup.new_tag('h6')
    intro_tag.string = intro_text
    main_section.append(intro_tag)

    # Парсинг новостей
    for item in soup.find_all('div', class_='item'):  # Обновите класс в зависимости от структуры сайта
        title_tag = item.find('a', class_='title')  # Обновите класс в зависимости от структуры сайта
        if not title_tag:
            continue
        
        title = title_tag.get_text(strip=True)
        relative_link = title_tag['href']
        link = urljoin(base_url, relative_link)
        
        # Создание нового элемента для новости
        news_item = template_soup.new_tag('div', **{'class': 'news-item'})
        
        # Добавление изображения (пока что используется изображение по умолчанию)
        img_tag = template_soup.new_tag('img', src='images/default-news.jpg', alt='News Image')
        
        news_text = template_soup.new_tag('div', **{'class': 'news-text'})
        
        # Создание элемента h2 для заголовка новости
        title_tag = template_soup.new_tag('h2')
        title_tag.string = title
        
        news_text.append(title_tag)
        news_item.append(img_tag)
        news_item.append(news_text)
        
        main_section.append(news_item)
    
    # Сохранение обновленного HTML в файл
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(str(template_soup))

    print("Finished updating HTML")

if __name__ == '__main__':
    get_news()
