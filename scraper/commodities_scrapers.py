import requests
from selenium import webdriver
from bs4 import BeautifulSoup

gold_url = "https://www.investing.com/commodities/gold-historical-data"
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(gold_url, chrome_options=options)
driver = webdriver.Chrome(chrome_options=options)
driver.get(gold_url)

elem = driver.find_element_by_xpath("//*")
source_code = elem.get_attribute("innerHTML")

soup = BeautifulSoup(source_code, 'html.parser')
table = soup.find("table", {"id": "curr_table"})

# print(soup.prettify())
# print(table)
# print(table.find_all("tr"))

derived_daily_commodity_data = []

for table_row in table.find_all("tr"):
    for raw_data in table_row.find_all("td"):
        print(raw_data.get_attribute("innerHTML"))
