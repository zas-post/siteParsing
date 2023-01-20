import asyncio

import  aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from pyshorteners import Shortener

BASE_URL = "https://arbuz.kz/ru/collections/248748-chai_kofe_sladosti#/"
HEADERS = {"User-Agent": UserAgent().random}


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS) as response:
            r = await aiohttp.StreamReader.read(response.content)
            soup = BS(r, "html.parser")

            items = soup.find_all("article", {"class": "product-item product-card"})
            for item in items:
                title = item.find("a", {"class": "product-card__title"})
                link = title.get("href")
                price = item.find("b").text.strip()

                short_price = Shortener().tinyurl.short(f"https://arbuz.kz{link}")

                print(f"TITLE: {title.text.strip()} | PRICE: {price} | URL: {short_price}")
                # print(title.count())

if __name__ == '__main__':
    asyncio.run(main())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())