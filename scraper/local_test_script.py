from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime
import psycopg2
import os
from pprint import pprint

html = """
<table class="genTbl closedTbl historicalTbl" id="curr_table" tablesorter="">
                    <thead>
                    <tr>
                        <th data-col-name="date" class="first left noWrap pointer">Date<span sort_default=""
                                                                                             class="headerSortDefault"></span>
                        </th>
                        <th data-col-name="price" class="noWrap pointer">Price<span sort_default=""
                                                                                    class="headerSortDefault"></span>
                        </th>
                        <th data-col-name="open" class="noWrap pointer">Open<span sort_default=""
                                                                                  class="headerSortDefault"></span></th>
                        <th data-col-name="high" class="noWrap pointer">High<span sort_default=""
                                                                                  class="headerSortDefault"></span></th>
                        <th data-col-name="low" class="noWrap pointer">Low<span sort_default=""
                                                                                class="headerSortDefault"></span></th>
                        <th data-col-name="vol" class="noWrap pointer">Vol.<span sort_default=""
                                                                                 class="headerSortDefault"></span></th>
                        <th data-col-name="change" class="noWrap pointer">Change %<span sort_default=""
                                                                                        class="headerSortDefault"></span>
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td data-real-value="1559865600" class="first left bold noWrap">Jun 07, 2019</td>
                        <td data-real-value="1,341.20" class="greenFont">1,341.20</td>
                        <td data-real-value="1,333.10">1,333.10</td>
                        <td data-real-value="1,347.70">1,347.70</td>
                        <td data-real-value="1,329.80">1,329.80</td>
                        <td data-real-value="0">-</td>
                        <td class="bold greenFont">0.27%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1559779200" class="first left bold noWrap">Jun 06, 2019</td>
                        <td data-real-value="1,337.60" class="greenFont">1,337.60</td>
                        <td data-real-value="1,330.80">1,330.80</td>
                        <td data-real-value="1,338.70">1,338.70</td>
                        <td data-real-value="1,326.20">1,326.20</td>
                        <td data-real-value="161">0.16K</td>
                        <td class="bold greenFont">0.70%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1559692800" class="first left bold noWrap">Jun 05, 2019</td>
                        <td data-real-value="1,328.30" class="greenFont">1,328.30</td>
                        <td data-real-value="1,328.90">1,328.90</td>
                        <td data-real-value="1,343.30">1,343.30</td>
                        <td data-real-value="1,326.30">1,326.30</td>
                        <td data-real-value="622">0.62K</td>
                        <td class="bold greenFont">0.37%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1559606400" class="first left bold noWrap">Jun 04, 2019</td>
                        <td data-real-value="1,323.40" class="greenFont">1,323.40</td>
                        <td data-real-value="1,324.30">1,324.30</td>
                        <td data-real-value="1,328.60">1,328.60</td>
                        <td data-real-value="1,320.80">1,320.80</td>
                        <td data-real-value="302">0.30K</td>
                        <td class="bold greenFont">0.05%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1559520000" class="first left bold noWrap">Jun 03, 2019</td>
                        <td data-real-value="1,322.70" class="greenFont">1,322.70</td>
                        <td data-real-value="1,307.00">1,307.00</td>
                        <td data-real-value="1,327.80">1,327.80</td>
                        <td data-real-value="1,307.00">1,307.00</td>
                        <td data-real-value="812">0.81K</td>
                        <td class="bold greenFont">1.29%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1559260800" class="first left bold noWrap">May 31, 2019</td>
                        <td data-real-value="1,305.80" class="greenFont">1,305.80</td>
                        <td data-real-value="1,287.70">1,287.70</td>
                        <td data-real-value="1,306.40">1,306.40</td>
                        <td data-real-value="1,287.50">1,287.50</td>
                        <td data-real-value="2814">2.81K</td>
                        <td class="bold greenFont">1.45%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1559174400" class="first left bold noWrap">May 30, 2019</td>
                        <td data-real-value="1,287.10" class="greenFont">1,287.10</td>
                        <td data-real-value="1,279.40">1,279.40</td>
                        <td data-real-value="1,288.30">1,288.30</td>
                        <td data-real-value="1,273.90">1,273.90</td>
                        <td data-real-value="55573">55.57K</td>
                        <td class="bold greenFont">0.48%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1559088000" class="first left bold noWrap">May 29, 2019</td>
                        <td data-real-value="1,281.00" class="greenFont">1,281.00</td>
                        <td data-real-value="1,278.90">1,278.90</td>
                        <td data-real-value="1,285.20">1,285.20</td>
                        <td data-real-value="1,278.40">1,278.40</td>
                        <td data-real-value="189694">189.69K</td>
                        <td class="bold greenFont">0.31%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1559001600" class="first left bold noWrap">May 28, 2019</td>
                        <td data-real-value="1,277.10" class="redFont">1,277.10</td>
                        <td data-real-value="1,283.50">1,283.50</td>
                        <td data-real-value="1,286.90">1,286.90</td>
                        <td data-real-value="1,275.10">1,275.10</td>
                        <td data-real-value="362163">362.16K</td>
                        <td class="bold redFont">-0.61%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1558915200" class="first left bold noWrap">May 27, 2019</td>
                        <td data-real-value="1,284.95" class="greenFont">1,284.95</td>
                        <td data-real-value="1,284.25">1,284.25</td>
                        <td data-real-value="1,286.85">1,286.85</td>
                        <td data-real-value="1,283.25">1,283.25</td>
                        <td data-real-value="0">-</td>
                        <td class="bold greenFont">0.06%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1558828800" class="first left bold noWrap">May 26, 2019</td>
                        <td data-real-value="1,284.15" class="greenFont">1,284.15</td>
                        <td data-real-value="1,284.20">1,284.20</td>
                        <td data-real-value="1,285.15">1,285.15</td>
                        <td data-real-value="1,283.65">1,283.65</td>
                        <td data-real-value="0">-</td>
                        <td class="bold greenFont">0.04%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1558656000" class="first left bold noWrap">May 24, 2019</td>
                        <td data-real-value="1,283.60" class="redFont">1,283.60</td>
                        <td data-real-value="1,283.20">1,283.20</td>
                        <td data-real-value="1,284.70">1,284.70</td>
                        <td data-real-value="1,280.10">1,280.10</td>
                        <td data-real-value="218714">218.71K</td>
                        <td class="bold redFont">-0.14%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1558569600" class="first left bold noWrap">May 23, 2019</td>
                        <td data-real-value="1,285.40" class="greenFont">1,285.40</td>
                        <td data-real-value="1,273.30">1,273.30</td>
                        <td data-real-value="1,287.10">1,287.10</td>
                        <td data-real-value="1,272.10">1,272.10</td>
                        <td data-real-value="330160">330.16K</td>
                        <td class="bold greenFont">0.88%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1558483200" class="first left bold noWrap">May 22, 2019</td>
                        <td data-real-value="1,274.20" class="greenFont">1,274.20</td>
                        <td data-real-value="1,274.40">1,274.40</td>
                        <td data-real-value="1,277.10">1,277.10</td>
                        <td data-real-value="1,272.00">1,272.00</td>
                        <td data-real-value="191366">191.37K</td>
                        <td class="bold greenFont">0.08%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1558396800" class="first left bold noWrap">May 21, 2019</td>
                        <td data-real-value="1,273.20" class="redFont">1,273.20</td>
                        <td data-real-value="1,277.70">1,277.70</td>
                        <td data-real-value="1,277.70">1,277.70</td>
                        <td data-real-value="1,269.00">1,269.00</td>
                        <td data-real-value="213168">213.17K</td>
                        <td class="bold redFont">-0.32%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1558310400" class="first left bold noWrap">May 20, 2019</td>
                        <td data-real-value="1,277.30" class="greenFont">1,277.30</td>
                        <td data-real-value="1,277.60">1,277.60</td>
                        <td data-real-value="1,278.80">1,278.80</td>
                        <td data-real-value="1,273.30">1,273.30</td>
                        <td data-real-value="212182">212.18K</td>
                        <td class="bold greenFont">0.13%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1558051200" class="first left bold noWrap">May 17, 2019</td>
                        <td data-real-value="1,275.70" class="redFont">1,275.70</td>
                        <td data-real-value="1,287.20">1,287.20</td>
                        <td data-real-value="1,289.00">1,289.00</td>
                        <td data-real-value="1,274.60">1,274.60</td>
                        <td data-real-value="264569">264.57K</td>
                        <td class="bold redFont">-0.82%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1557964800" class="first left bold noWrap">May 16, 2019</td>
                        <td data-real-value="1,286.20" class="redFont">1,286.20</td>
                        <td data-real-value="1,297.70">1,297.70</td>
                        <td data-real-value="1,299.30">1,299.30</td>
                        <td data-real-value="1,284.20">1,284.20</td>
                        <td data-real-value="282065">282.07K</td>
                        <td class="bold redFont">-0.89%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1557878400" class="first left bold noWrap">May 15, 2019</td>
                        <td data-real-value="1,297.80" class="greenFont">1,297.80</td>
                        <td data-real-value="1,298.00">1,298.00</td>
                        <td data-real-value="1,301.70">1,301.70</td>
                        <td data-real-value="1,293.60">1,293.60</td>
                        <td data-real-value="247522">247.52K</td>
                        <td class="bold greenFont">0.12%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1557792000" class="first left bold noWrap">May 14, 2019</td>
                        <td data-real-value="1,296.30" class="redFont">1,296.30</td>
                        <td data-real-value="1,300.80">1,300.80</td>
                        <td data-real-value="1,304.20">1,304.20</td>
                        <td data-real-value="1,294.30">1,294.30</td>
                        <td data-real-value="222050">222.05K</td>
                        <td class="bold redFont">-0.42%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1557705600" class="first left bold noWrap">May 13, 2019</td>
                        <td data-real-value="1,301.80" class="greenFont">1,301.80</td>
                        <td data-real-value="1,288.30">1,288.30</td>
                        <td data-real-value="1,302.20">1,302.20</td>
                        <td data-real-value="1,282.40">1,282.40</td>
                        <td data-real-value="379440">379.44K</td>
                        <td class="bold greenFont">1.12%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1557446400" class="first left bold noWrap">May 10, 2019</td>
                        <td data-real-value="1,287.40" class="greenFont">1,287.40</td>
                        <td data-real-value="1,285.00">1,285.00</td>
                        <td data-real-value="1,290.30">1,290.30</td>
                        <td data-real-value="1,283.90">1,283.90</td>
                        <td data-real-value="238643">238.64K</td>
                        <td class="bold greenFont">0.17%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1557360000" class="first left bold noWrap">May 09, 2019</td>
                        <td data-real-value="1,285.20" class="greenFont">1,285.20</td>
                        <td data-real-value="1,281.90">1,281.90</td>
                        <td data-real-value="1,289.20">1,289.20</td>
                        <td data-real-value="1,280.40">1,280.40</td>
                        <td data-real-value="306546">306.55K</td>
                        <td class="bold greenFont">0.30%</td>
                    </tr>
                    <tr>
                        <td data-real-value="1557273600" class="first left bold noWrap">May 08, 2019</td>
                        <td data-real-value="1,281.40" class="redFont">1,281.40</td>
                        <td data-real-value="1,285.60">1,285.60</td>
                        <td data-real-value="1,292.80">1,292.80</td>
                        <td data-real-value="1,280.20">1,280.20</td>
                        <td data-real-value="302694">302.69K</td>
                        <td class="bold redFont">-0.33%</td>
                    </tr>
                    </tbody>
                </table>
"""


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


def init_db_connection():
    pg_user = os.environ["POSTGRES_USER"]
    pg_pass = os.environ["POSTGRES_PASSWORD"]
    pg_port = os.environ["POSTGRES_PORT"]
    return psycopg2.connect(
        dbname="postgres",
        host="localhost",
        port=pg_port,
        user=pg_user,
        password=pg_pass
    )


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
    except psycopg2.Error:
        print("Unable To Create Table: Likely already exists.")

    pg_db_connection.commit()
    cursor.close()

def upload_data_to_postgres(pg_db_connection, derived_commodity_data):
    # if len(derived_commodity_data) > 0:
    #     raise Exception("def upload_data_to_postgres: derived_commodity_data is empty")

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
    if True:
        load_dotenv()

    db_connection = init_db_connection()
    urls = [("https://www.investing.com/commodities/gold-historical-data", "gold"),
            ("https://www.investing.com/commodities/silver-historical-data", "silver")]

    for link in urls:
        # soup = BeautifulSoup(link[0], 'html.parser')
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find("table", {"id": "curr_table"})
        pprint(get_commodity_data(table, link[1]))

        create_commodity_table(db_connection, link[1])

        for commodity_list in get_commodity_data(table, link[1]):
            upload_data_to_postgres(db_connection, commodity_list)

    db_connection.close()
