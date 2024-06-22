import asyncio
import logging

import requests
from bs4 import BeautifulSoup

from backend.news_parse_api.service.parse.mixin import BaseNewsParser
from backend.news_parse_api.config import logger


class RequestsNewsParser(BaseNewsParser):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.rbc.ru/short_news"
        self.session = requests.Session()

    async def fetch(self, url):
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error("Request failed: %e", e.__cause__)
            return None

    async def parse(self):
        try:
            html = await self.fetch(self.base_url)
            await asyncio.sleep(2)

            if html:
                logger.info('Started Parsing')
                soup = BeautifulSoup(html, 'html.parser')

                news_feed = {
                    news.select_one(".item__category").text[:-2]
                    : news.select_one(".item__link").get('href')
                    for news in soup.select(".js-news-feed-item")
                }

                current_categories = set()
                for category_name, link in news_feed.items():

                    # validation for main domain, no subdomains support
                    if link and link.startswith('https://www.rbc.ru/'):
                        news_html = await self.fetch(link)
                        if news_html:
                            news_soup = BeautifulSoup(news_html, 'html.parser')
                            news_content = news_soup.select_one(".l-col-main")
                            if news_content:
                                title = news_content.select_one(
                                    '.article__header__title-in'
                                ).text
                                description = '\n'.join(
                                    [
                                        p.text for p in news_content.select_one(
                                            '.article__text'
                                        ).find_all('p')
                                    ]
                                )

                                self.add_news(category_name, title, link, description)
                                current_categories.add(category_name)

                    if len(current_categories) == 5:
                        break

        except Exception as e:
            logger.error("Unexpected error: %e", e.__cause__)
        finally:
            self.session.close()


def run_requests_parser():
    parser = RequestsNewsParser()
    asyncio.run(parser.parse())
    parser.save_to_csv('news_requests.csv')
    return "Parsing completed and data saved to CSV."
