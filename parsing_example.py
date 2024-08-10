from bs4 import BeautifulSoup
import requests
import pandas as pd

# Это URL-адрес веб-страницы, с которой мы хотим получить данные.
url = 'https://new-science.ru/category/news/page/3/'


# Здесь мы используем библиотеку requests для отправки GET-запроса
# к указанному URL-адресу и получения ответа.
# Если получили статус 200 - то все пошло отлично и страница доступна.
response = requests.get(url)
print(response)


# Мы передаем текст ответа от сайта (response.text)
# и указываем парсер, который будет использоваться ("lxml"),
# чтобы создать объект BeautifulSoup для дальнейшего анализа HTML-кода.
bs = BeautifulSoup(response.text,"lxml")
print(bs)


# Здесь мы ищем все элементы <h2 class="post-title"> на странице
# и сохраняем их в переменной temp. Это все заголовки новостей на странице, которые мы хотим собрать.
temp = bs.find_all('h2', 'post-title')
print(temp)

print(f"""h2 содержит внутри себя тег <a> c ссылкой и сам текст \n
      текст самого первого заголовка: {temp[0].text}. \n
      Ссылка, которая хранится внутри: {temp[0].find('a').get('href')}""")


# Мы создаем словарь с ключами "news" и "links",
# которые будут содержать заголовки новостей и ссылки на новости соответственно.
dict_news = {"news": [], "links": []}

for i in temp:
  dict_news["news"].append(i.text)
  #dict_news["links"].append(i.find('a').get('href'))

# Здесь мы используем библиотеку pandas для создания DataFrame
# из словаря dict_news с указанными столбцами "news" и "links".
# Этот DataFrame будет содержать собранные данные новостей.

#df_news = pd.DataFrame(dict_news, columns=["news", "links"])
df_news = pd.DataFrame(dict_news, columns=["news", "links"])

# Это нужно для удобства вывода.
# Можно хранить собранную информацию в любой структуре
df_news