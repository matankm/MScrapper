# This is a sample scrapping script.
# Created on Mon Sep 27 21:22:30 2021
# @author: Mateusz Murawski
# @description: web scraper extracting currency rate from NBP website

# -*- coding: utf-8 -*-


from DBConnect import db
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime


def NBPSiteScraper():
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

    for q in range(0, last_index):
        db("""INSERT INTO rates (CURRENCY_NAME, CURRENCY_UNIT, CURRENCY_CODE, CURRENCY_RATE, RATE_DATE, UPLOAD_TIME)
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s');""" % (
        result['Nazwa waluty'].iloc[q], result['Jednostka waluty'].iloc[q],
        result['Kod waluty'].iloc[q], result['Kurs średni'].iloc[q],
        result['Data kursu'].iloc[q], datetime.today().strftime('%Y-%m-%d')))










