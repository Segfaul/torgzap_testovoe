import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException

from backend.news_parse_api.service.parse.mixin import BaseNewsParser
from backend.news_parse_api.config import logger

class SeleniumNewsParser(BaseNewsParser):
    def __init__(self):
        super().__init__()
        self.driver = self._init_driver()

    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(log_output='errors.log')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    async def parse(self):
        try:
            self.driver.get("https://www.rbc.ru/short_news")
            await asyncio.sleep(2)
            logger.info('Started Parsing')

            # activate JS script to upload more news
            for _ in range(2):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                await asyncio.sleep(2)

            news_feed = {
                news.find_element(By.CSS_SELECTOR, ".item__category").text[:-2]
                :news.find_element(By.CSS_SELECTOR, ".item__link").get_attribute('href')
                for news in self.driver.find_elements(By.CSS_SELECTOR, ".js-news-feed-item")
            }
            current_categories = set()
            for category_name, link in news_feed.items():

                # validation for main domain, no subdomains support
                if link.startswith('https://www.rbc.ru/'):
                    self.driver.get(link)
                    news_content = self.driver.find_element(By.CSS_SELECTOR, ".l-col-main")
                    title = news_content.find_element(
                        By.CSS_SELECTOR, '.article__header__title-in'
                    ).text
                    description = '\n'.join([p.text for p in news_content.find_element(
                        By.CSS_SELECTOR, '.article__text'
                    ).find_elements(By.TAG_NAME, 'p')])

                    self.add_news(category_name, title, link, description)

                    current_categories.add(category_name)

                if len(current_categories) == 5:
                    break

        except (WebDriverException, TimeoutException) as e:
            logger.error(
                'Webdriver error: %s', {e.__cause__}
            )
        except Exception as e:
            logger.error(
                'Unexpected error: %s', {e.__cause__}
            )
        finally:
            self.driver.quit()


def run_selenium_parser():
    parser = SeleniumNewsParser()
    asyncio.run(parser.parse())
    parser.save_to_csv('news_selenium.csv')
    return "Parsing completed and data saved to CSV."
