# `TORGZAP NewsAPI [TEST]`

Веб-приложение для парсинга новостей с РБК.
___

## *Статус проекта*

***Завершен v0.0.1 &#10003;***
___
## Функциональность
#### Private API
- [GET] /api/v1/news: получить список всех новостей из определенного файла.csv.
- [POST] /api/v1/news/requests: запустить парсер новостей на requests+bs4.
- [POST] /api/v1/news/selenium: запустить парсер новостей на selenium.

## Технологии и фреймворки
- [Python 3.11.6](https://www.python.org/downloads/release/python-3116/)
- FastAPI
- Pandas
- Uvicorn
- Selenium
- Requests
- BeautifulSoup4
___

## Запуск в dev mode

1. Clone the repository to the local machine

    ```shell
    git clone https://github.com/Segfaul/torgzap_testovoe.git
    cd torgzap_testovoe/
    ```

2. Install depencies

    ```shell
    pip install -r requirements.txt
    ```

3. Run the uvicorn server

    ```shell
    uvicorn backend.news_parse_api.main:app --reload --port 5000
    ```

4. Checkout following address

    ```shell
    http://127.0.0.1:5000/api/swagger
    ```
___