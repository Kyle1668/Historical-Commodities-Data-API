import os
import psycopg2
from pprint import pprint
from datetime import datetime
from selenium import webdriver
from dotenv import load_dotenv
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
            print("Row Parsed: %s" % derived_day_data)
        else:
            print("WARNING: No commodity data found in this row (td). Likely table head.")

    return total_derived_daily_commodity_data


def init_db_connection():
    pg_user = os.environ["POSTGRES_USER"]
    pg_pass = os.environ["POSTGRES_PASSWORD"]
    pg_host = os.environ["POSTGRES_HOST"]
    pg_port = os.environ["POSTGRES_PORT"]
    connection = None

    try:
        connection = psycopg2.connect(
            dbname="postgres",
            host=pg_host,
            port=pg_port,
            user=pg_user,
            password=pg_pass
        )
    except psycopg2.Error:
        print("Error: Unable to connection to database")
        print("ENV: %s" % os.environ)
        exit(1)

    return connection


def create_commodity_table(pg_db_connection, commodity_name):
    cursor = pg_db_connection.cursor()
    try:
        query = """
                CREATE TABLE %s (
                    date DATE,
                    price FLOAT,
                    open FLOAT,
                    high FLOAT,
                    low FLOAT,
                    volume FLOAT,
                    change FLOAT,
                    PRIMARY KEY (date)
                );
            """ % commodity_name
        cursor.execute(query)
        print("Table Created: %s" % commodity_name)
    except psycopg2.Error:
        print("Unable To Create Table: Likely already exists.")

    pg_db_connection.commit()
    cursor.close()


def upload_data_to_postgres(pg_db_connection, derived_commodity_data):
    commodity = derived_commodity_data["commodity"]
    cursor = pg_db_connection.cursor()

    try:
        date_object = datetime.strptime(derived_commodity_data["date"], "%b %d, %Y")
        formatted_volume = 0

        if derived_commodity_data["volume"] != "-":
            formatted_volume = float(derived_commodity_data["volume"].strip('K')) * 1000

        formatted_change = float(derived_commodity_data["change"].strip('%')) / 100

        query = """
            INSERT INTO %s (date, price, open, high, low, volume, change)
            VALUES ('%s', %s, %s, %s, %s, %s, %s);
        """ % (
            commodity,
            date_object.date().isoformat(),
            float(derived_commodity_data["price"].replace(",", "")),
            float(derived_commodity_data["open"].replace(",", "")),
            float(derived_commodity_data["high"].replace(",", "")),
            float(derived_commodity_data["low"].replace(",", "")),
            formatted_volume,
            formatted_change,
        )
        cursor.execute(query)
    except psycopg2.Error:
        pass

    pg_db_connection.commit()
    cursor.close()


if __name__ == "__main__":
    if os.environ["ENV"] == "production":
        load_dotenv()

    db_connection = init_db_connection()
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

        create_commodity_table(db_connection, link[1])

        for commodity_list in get_commodity_data(table, link[1]):
            upload_data_to_postgres(db_connection, commodity_list)
