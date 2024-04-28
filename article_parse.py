import requests
from bs4 import BeautifulSoup
import json
import time
# URL видимо на api с количеством цитирований
#доступ только по pii доставать из обобщенного файла и добавляь в df
def citation_count(pii: str):
    article_url = f"https://www.sciencedirect.com/sdfe/arp/citingArticles?pii={pii}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }
    # Отправляем GET-запрос на страницу статьи
    response = requests.get(article_url, headers=headers)
    #time.sleep(0.25)
    # Проверяем успешность запроса
    if response.status_code == 200:
        # Создаем объект BeautifulSoup для парсинга страницы
        soup = BeautifulSoup(response.text, 'html.parser')
        data = json.loads(soup.get_text())
        hit_count = data["hitCount"]
        return(hit_count)
    else:
        print(response)
