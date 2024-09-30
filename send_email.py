import os
import pymysql
import gmail_script
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv('.env')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
EMAILS = os.getenv('EMAIL').split(';')
SUBJECT = os.getenv('SUBJECT')

connection = pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, database='HouseMarket', connect_timeout=5)

sql_houses = """
SELECT price, address, bedrooms, bathrooms, sq_ft, image, url, createdAt, updatedAt FROM HouseMarket
WHERE (
    LCASE(address) LIKE '%ancaster%' OR
    LCASE(address) LIKE '%dundas%' OR
    LCASE(address) LIKE '%burlington%'
    ) AND createdAt BETWEEN NOW() - INTERVAL 2 DAY AND NOW()
    ORDER BY price
    LIMIT 100
"""

def render_email_template(template_name, context):
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    return template.render(context)


def send_email():
    context = {
        "houses": []
    }

    print("[INFO] Collecting good houses.")
    with connection.cursor() as cursor:
        cursor.execute(sql_houses)
        houses = cursor.fetchall()

    for house in houses:
        context['houses'].append({
            "price": house[0],
            "address": house[1],
            "bedrooms": house[2],
            "bathrooms": house[3],
            "sq_ft": house[4],
            "image": house[5],
            "url": house[6],
            "createdAt": house[7],
            "updatedAt": house[8],
        })

    if len(houses) == 0:
        print("[INFO] No houses found")
        return


    print("[INFO] Sending email.")
    email_content = render_email_template("email_template.html", context)
    for email in EMAILS:
        gmail_script.send_email(email, email_content, SUBJECT)
    print("[INFO] Email sent")


if __name__ == '__main__':
    send_email()
