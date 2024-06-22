from abc import ABC, abstractmethod

import pandas as pd


class BaseNewsParser(ABC):

    def __init__(self):
        self.news_data = []

    @abstractmethod
    async def parse(self):
        pass

    def save_to_csv(self, filename):
        df = pd.DataFrame(self.news_data)
        df.to_csv(filename, index=False)

    def add_news(self, category, title, link, description):
        self.news_data.append({
            "category": category,
            "title": title,
            "link": link,
            "description": description
        })
