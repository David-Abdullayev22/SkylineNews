import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_news():
    base_url = 'https://www.gazeta.ru'
    url = urljoin(base_url, '/news/')
    print(f"Fetching URL: {url}")
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')

    with open('index.html', 'r', encoding='utf-8') as file:
        template_soup = BeautifulSoup(file, 'html.parser')
    
    main_section = template_soup.find('main', id='news-content')
    main_section.clear()

    intro_text = "Главные новости:"
    intro_tag = template_soup.new_tag('h6')
    intro_tag.string = intro_text
    main_section.append(intro_tag)

    if not os.path.exists('articles'):
        os.makedirs('articles')

    if not os.path.exists('images'):
        os.makedirs('images')

    for index, item in enumerate(soup.find_all('div', class_='b_ear-textblock')):
        title = item.get_text()
        relative_link = item.find('a', class_='b_ear m_techlisting   ')
        link = urljoin(base_url, relative_link)
        
        article_response = requests.get(link)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        
        article_content_div = article_soup.find('div', class_='b_ear m_techlisting')
        if not article_content_div:
            article_content_div = article_soup.find('div', class_='b_ear-textblock')
        if not article_content_div:
            article_content_div = article_soup.find('div', class_='b_ear-title')
        if not article_content_div:
            article_content_div = article_soup.find('div', id='content')

        article_content = article_content_div.get_text(strip=True) if article_content_div else 'Содержание статьи не найдено'
        #print(article_content)

         # Парсинг изображения
        img_tag = article_content_div.find('div', class_='b_ear-image')
        img_url = urljoin(base_url, img_tag['src']) if img_tag else None
        img_filename = None
        
        if img_url:
        #     Скачиваем изображение и сохраняем его
            img_data = requests.get(img_url).content
            img_filename = os.path.join('images', os.path.basename(urlparse(img_url).path))
            with open(img_filename, 'wb') as img_file:
                img_file.write(img_data)
        else:
            img_filename = 'images/default-news.jpg'  # Путь к изображению по умолчанию
        
        article_filename = f'articles_main/article_{index + 1}.html'
        with open(article_filename, 'w', encoding='utf-8') as file:
            file.write(f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{title}</title><link href="../../style.css" rel="stylesheet" /></head><body><header><div class="logo"><img alt="logo company" class="logoimg" src="../../images/davdi.png" /><h1>Skyline News</h1></div><div class="header-buttons"><a class="header-btn" href="../../index.html">Главные новости</a><a class="header-btn" href="#">Региональные новости</a></div><div class="mode-button"><button class="header-btn" id="theme-toggle">Сменить тему</button></div></header><div class="container"><aside><h3>ТЕМЫ:</h3><ul><li><img alt="News Icon" src="../../images/fireicon.png" /><h4>ЧП</h4><a class="btn" href="#">Читать</a></li><li><img alt="News Icon" src="../../images/politicicon.png" /><h4>Политика</h4><a class="btn" href="#">Читать</a></li><li><img alt="News Icon" src="../../images/scienceicon.png" /><h4>Наука</h4><a class="btn" href="#" onclick="window.location.href=\'../../science_news.html\'">Читать</a></li><li><img alt="News Icon" src="../../images/sporticon.png" /><h4>Спорт</h4><a class="btn" href="#">Читать</a></li><li><img alt="News Icon" src="../../images/iticon.png" /><h4>IT</h4><a class="btn" href="#">Читать</a></li><li><img alt="News Icon" src="../../images/earthicon.png" /><h4>Природа</h4><a class="btn" href="#">Читать</a></li><li><img alt="News Icon" src="../../images/foodicon.png" /><h4>Кулинария</h4><a class="btn" href="#">Читать</a></li></ul><a class="btn" href="#">Читать все новости</a></aside><main><h2>{title}</h2><img src="../../{img_filename}" alt="News Image"/><p>{article_content}</p></main></div><footer><p>Davdi Все права защищены ©2024</p></footer><script src="../../script.js"></script></body></html>')



        news_item = template_soup.new_tag('div', **{'class': 'news-item'})
        
        img_display_tag = template_soup.new_tag('img', src=img_filename, alt='News Image')
        
        news_text = template_soup.new_tag('div', **{'class': 'news-text'})
        title_tag = template_soup.new_tag('h2')
        title_tag.string = title
        
        content_tag = template_soup.new_tag('p', class_='b_article-text')
        content_tag.string = article_content[:150] + '...'
        
        read_more_btn = template_soup.new_tag('a', href=article_filename, **{'class': 'read-more-btn'})
        read_more_btn.string = 'Читать далее'
        
        news_text.append(title_tag)
        news_text.append(content_tag)
        news_text.append(read_more_btn)
        news_item.append(img_display_tag)
        news_item.append(news_text)
        
        main_section.append(news_item)
    
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(str(template_soup))

    print("Finished updating HTML")

if __name__ == '__main__':
    get_news()
