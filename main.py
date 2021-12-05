# This is a sample scrapping script.
# Created on Mon Sep 27 21:22:30 2021
# @author: Mateusz Murawski
# @description: web scraper extracting currency rate from NBP website

# -*- coding: utf-8 -*-


#import mysql.connector
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime


def db(query):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             port=3306,
                                             database='stage',
                                             user='mamur',
                                             password='TakieTamHaslo123')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            print("### COMMITTED ###")

    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


URL = "https://www.nbp.pl/home.aspx?f=/kursy/kursya.html"
page = requests.get(URL)

soup = BeautifulSoup(page.text, features="lxml")

date = soup.find('h3', {"class": "center"})
day_column = date.text[-10:]

table = soup.find('table', {"class": "nbptable"})

headers = []
for i in table.find_all('th'):
    title = i.text
    headers.append(title)

rows = table.find_all('tr')
data = []

for row in rows[1:]:
    row_data = row.find_all('td')
    cols = [tr.text for tr in row_data]
    data.append(cols)

result = pd.DataFrame(data, columns=headers)

print(result)
print("\n")

result['Data kursu'] = day_column

print(result.iloc[4])

unit_col = result['Kod waluty'].str.extract('(\d+)')
result['Kod waluty'] = result['Kod waluty'].str.extract('([A-Z][A-Z][A-Z])')
result['Jednostka waluty'] = unit_col
result['Kurs średni'] = result['Kurs średni'].str.replace(',', '.')

last_index = len(result.index)

print(result)
print("\n")

# for q in range(0, last_index):
#     db("""INSERT INTO rates (CURRENCY_NAME, CURRENCY_UNIT, CURRENCY_CODE, CURRENCY_RATE, RATE_DATE, UPLOAD_TIME)
#         VALUES ('%s', '%s', '%s', '%s', '%s', '%s');""" % (
#     result['Nazwa waluty'].iloc[q], result['Jednostka waluty'].iloc[q],
#     result['Kod waluty'].iloc[q], result['Kurs średni'].iloc[q],
#     result['Data kursu'].iloc[q], datetime.today().strftime('%Y-%m-%d')))










