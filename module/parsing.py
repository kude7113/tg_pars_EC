import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

from module.TG_API import send_news

# URL сайта для парсинга
URL = "https://www.gazeta.ru/"

# Хранилище для последней обработанной новости
last_seen_time = None

# Структура для хранения новостей
class NewsItem:
    def __init__(self, title, url, pub_time):
        self.title = title
        self.url = url
        self.pub_time = pub_time




def get_news():
    """
    Функция парсинга главных новостей с gazeta.ru.
    Возвращает список новых новостей в формате NewsItem.
    """
    global last_seen_time

    response = requests.get(URL)
    if response.status_code != 200:
        print(f"Ошибка подключения к сайту: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Найти блоки с заголовками новостей
    title_blocks = soup.find_all('div', class_='b_ear-title')

    new_news = []
    latest_time = None

    for title_elem in title_blocks:
        link_elem = title_elem.find_parent('a')  # Находим родительский тег <a>
        time_elem = link_elem.find('time', class_='b_ear-time') if link_elem else None  # Ищем внутри <a>

        if not title_elem or not time_elem or not link_elem:
            continue

        title = title_elem.text.strip()
        link = link_elem['href'] if 'href' in link_elem.attrs else None
        if link and not link.startswith('http'):
            link = URL + link  # Формируем полный URL для относительных ссылок

        try:
            pub_time_str = time_elem["datetime"]  # Извлекаем datetime атрибут
            pub_time = datetime.strptime(pub_time_str, "%Y-%m-%dT%H:%M:%S%z")
        except (ValueError, KeyError, TypeError):
            continue

        if latest_time is None or pub_time > latest_time:
            latest_time = pub_time

        # Если это первая итерация, запоминаем последнюю новость и сразу отправляем
        if last_seen_time is None:
            last_seen_time = pub_time
            send_news(NewsItem(title, link, pub_time))
            return [NewsItem(title, link, pub_time)]

        # Если новость старее или равна последней сохраненной, пропускаем
        if pub_time <= last_seen_time:
            continue

        new_news.append(NewsItem(title, link, pub_time))

    # Обновляем последнюю обработанную новость, если есть новые
    if latest_time and latest_time > last_seen_time:
        last_seen_time = latest_time

    return sorted(new_news, key=lambda x: x.pub_time)  # Сортируем по времени публикации


def monitor_news(interval=180):
    """
    Функция для мониторинга сайта каждые interval секунд.
    """
    print("Запуск мониторинга новостей...")
    while True:
        try:
            fresh_news = get_news()
            if fresh_news:
                print(f"Найдены {len(fresh_news)} новые новости:")
                for news in fresh_news:
                    send_news(news)  # <-- Используем функцию из telegram_integration
            else:
                print("Новых новостей нет.")
        except Exception as e:
            print(f"Ошибка парсинга: {e}")

        time.sleep(interval)

