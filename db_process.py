import re
import os
import json
import pymysql
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv('.env')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')

connection = pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, database='HouseMarket', connect_timeout=5)

sql_insert_query_cw = """
INSERT INTO HouseMarket (price, address, bedrooms, bathrooms, sq_ft, image, url) 
VALUES (%s, %s, %s, %s, %s, %s, %s) 
ON DUPLICATE KEY UPDATE 
price = VALUES(price)
"""


def __extract_number(text: str, integer: bool = True):
    clean = re.sub(r'[^0-9.]', '', text)
    if integer:
        return int(clean)
    return Decimal(clean)


def load_json_file_into_db():
    with open('output/data.json', 'r') as file:
        houses_data = json.load(file)
    rows = []

    for areas in houses_data:
        for house in houses_data[areas]:
            price = __extract_number(house['price'])
            address = house['address']
            bedroom = house['bedroom']
            bathroom = house['bathroom']
            sq_ft = __extract_number(house['sq_ft'] if '-' not in house['sq_ft'] else "0")
            image_value = house['image']
            url = house['url']
            rows.append((price, address, bedroom, bathroom, sq_ft, image_value, url))

    try:
        with connection.cursor() as cursor:
            cursor.executemany(sql_insert_query_cw, rows)

        connection.commit()
        # os.remove('output/data.json')
    except Exception as e:
        print(f"[ERROR] Error in insert car data: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    print("[INFO] Storing data into MySQL DB")
    load_json_file_into_db()
    print("[INFO] All data is stored in MySQL DB.")
