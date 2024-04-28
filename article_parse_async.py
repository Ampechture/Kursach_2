import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json

async def citation_count_async(pii: str):
    article_url = f"https://www.sciencedirect.com/sdfe/arp/citingArticles?pii={pii}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(article_url, headers=headers) as response:
            # Проверяем успешность запроса
            if response.status == 200:
                # Получаем данные и преобразуем их из JSON
                data = await response.json()
                hit_count = data["hitCount"]
                return hit_count
            else:
                # Выводим информацию о неудачном запросе
                text = await response.text()
                print(f"Error: {response.status}, Response: {text}")
