import requests
from bs4 import BeautifulSoup

try:
    gold_url = "https://www.investing.com/commodities/gold-historical-data"
    session = requests.Session()
    page = session.get(gold_url, headers={'User-Agent': 'Mozilla/5.0'})

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        print(soup.prettify())
    else:
        print("Unable to connect")

except requests.exceptions.MissingSchema:
    print("Request didn't return HTML")
