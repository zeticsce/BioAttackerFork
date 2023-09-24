import os
import sys 
import requests
import traceback
import time

import pymysql
from pymysql.cursors import DictCursor

if os.path.abspath(os.curdir) in sys.path: sys.path.append(os.path.abspath(os.curdir))

from config import MYSQL_HOST, MYSQL_DB, MYSQL_PASSWORD, MYSQL_USER



my_ip = requests.get('https://ip.beget.ru/').text.replace(' ', '').replace('\n', '')
host = '127.0.0.1' if my_ip == MYSQL_HOST else MYSQL_HOST
conn = pymysql.connect(
    host=host,
    port=3306,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database="",
    charset='utf8mb4',
    cursorclass=DictCursor
)
def query(query):
    start_time = time.time()
    with conn.cursor() as cursor:
        cursor.execute(query)
        conn.commit()
        print("query", time.time() - start_time)
        return cursor.fetchall()