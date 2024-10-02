import asyncio

import aiohttp
import fake_useragent
from bs4 import BeautifulSoup

CATEGORY = [
    'https://habr.com/ru/hubs/infosecurity/articles/',
    'https://habr.com/ru/hubs/popular_science/articles/'
]

headers = {
    'user-agent': fake_useragent.UserAgent().random
}

async def send_request(url: str):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            return await resp.text(encoding='utf-8')


async def parse_category(category_url, count):
    html_response = await send_request(category_url)
    soup = BeautifulSoup(html_response, 'lxml')

    page_block = soup.find('div', class_='tm-pagination__pages')
    category_name = category_url.split('/')[-3]

    for i_page in range(1, count):
        response = await send_request(f'{category_url}page{i_page}')

        soup = BeautifulSoup(response, 'lxml')
        articles = soup.find_all('article', attrs={'data-test-id': 'articles-list-item'})

        for index, article in enumerate(articles):
            link = article.find('a', attrs={'data-test-id': 'article-snippet-title-link'})
            title = link.find('span')

            # print(f'{index + 1}. | {title.text} | https://habr.com{link.attrs["href"]}\n')
            with open(f'parse_files/{category_name}.txt', 'a') as file:
                file.write(f'{index + 1}. | {title.text} | https://habr.com{link.attrs["href"]}\n')


async def parse(list_category_url, count):
    for category_url in list_category_url:
        await parse_category(category_url, count)


# if '__main__' == __name__:
#     asyncio.run(main())
