from pprint import pprint
from selenium import webdriver
from bs4 import BeautifulSoup


def get_commodity_data(raw_table, commodity):
    """
    Parses the HTML table's rows for commodity data
    :param raw_table: List of HTML strings for the child elements of #curr_table
    :param commodity: The type of commodity being derived.
    :return: List of dictionaries each corresponding to a day
    """
    total_derived_daily_commodity_data = []

    for table_row in raw_table.find_all("tr"):
        derived_day_data = {}
        for raw_data in table_row.find_all("td"):
            if "date" not in derived_day_data:
                derived_day_data["date"] = raw_data.get_text()
            elif "price" not in derived_day_data:
                derived_day_data["price"] = raw_data.get_text()
            elif "open" not in derived_day_data:
                derived_day_data["open"] = raw_data.get_text()
            elif "high" not in derived_day_data:
                derived_day_data["high"] = raw_data.get_text()
            elif "low" not in derived_day_data:
                derived_day_data["low"] = raw_data.get_text()
            elif "volume" not in derived_day_data:
                derived_day_data["volume"] = raw_data.get_text()
            elif "change" not in derived_day_data:
                derived_day_data["change"] = raw_data.get_text()

        if bool(derived_day_data):
            derived_day_data["commodity"] = commodity
            total_derived_daily_commodity_data.append(derived_day_data)
        else:
            print("WARNING: No commodity data found in this row (td).")

    return total_derived_daily_commodity_data


def upload_data_to_postgres(derived_commodity_data):
    pass


if __name__ == "__main__":
    urls = [("https://www.investing.com/commodities/gold-historical-data", "gold"),
            ("https://www.investing.com/commodities/silver-historical-data", "silver")]

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=options)

    for link in urls:
        # soup = BeautifulSoup(link[0], 'html.parser')
        driver.get(link[0])
        elem = driver.find_element_by_xpath("//*")
        source_code = elem.get_attribute("innerHTML")
        soup = BeautifulSoup(source_code, 'html.parser')
        table = soup.find("table", {"id": "curr_table"})
        pprint(get_commodity_data(table, link[1]))
