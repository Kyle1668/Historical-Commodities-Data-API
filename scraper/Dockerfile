FROM joyzoursky/python-chromedriver:3.6-alpine3.7-selenium

WORKDIR /usr/src/historical_commodities_web_scraper
COPY . /usr/src/historical_commodities_web_scraper

ENV PATH="${PATH};/usr/src/historical_commodities_web_scraper/drivers"

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

RUN pip3 install requests \
                 beautifulsoup4 \
                 psycopg2 \
                 selenium \
                 webdriver-manager \
                 python-dotenv

CMD ["python3", "commodities_scrapers.py"]
