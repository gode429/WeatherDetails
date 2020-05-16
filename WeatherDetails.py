from bs4 import BeautifulSoup
import csv
import requests
import time
import pandas as pd
import urllib
import re
import math

columns = ['Date (yyyy-mm-dd)', 'Average temperature (°F)', 'Average humidity (%)', 'Average dewpoint (°F)',
           'Average barometer (in)', 'Average windspeed (mph)', 'Average gustspeed (mph)',
           'Average direction (°deg)', 'Rainfall for month (in)', 'Rainfall for year (in)', 'Maximum rain per minute',
           'Maximum temperature (°F)', 'Minimum temperature (°F)', 'Maximum humidity (%)', 'Minimum humidity (%)',
           'Maximum pressure', 'Minimum pressure', 'Maximum windspeed (mph)', 'Maximum gust speed (mph)',
           'Maximum heat index (°F)']
print("Please enter the start date in the format - dd/mm/yyyy")
StartDay, StartMonth, StartYear = input().split('/')
print("Please enter the end date in the format - dd/mm/yyyy")
EndDay, EndMonth , EndYear  = input().split('/')

templist = []
for year in range(int(StartYear), int(EndYear)+1):
    for month in range(1, 13):
        if month == 1 and year == int(StartYear):
            month = int(StartMonth)
            count = int(StartDay) - 1
        else:
            count = 0
        if month < 10:
            date = str(year) + "0" + str(month)
        else:
            date = str(year) + str(month)
        if month == int(EndMonth) + 1 and year == int(EndYear):
            break
        url = "http://www.estesparkweather.net/archive_reports.php?date=" + date
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'lxml')
        tables = soup.find_all("table", {"cellpadding": "3"})
        length = len(tables)
        for table in tables:
            count = count + 1
            first = table.find("td", {"colspan": "2"}).text[4:5]
            second = table.find("td", {"colspan": "2"}).text[5:6]
            if first.isnumeric() and second.isnumeric():
                tableday = int(table.find("td", {"colspan": "2"}).text[4:6])
            elif first.isnumeric():
                tableday = int(table.find("td", {"colspan": "2"}).text[4:5])
            else:
                break
            if month == int(StartMonth) and year == int(StartYear) and tableday < int(StartDay) :
                count = int(StartDay) - 1
                continue
            if month == int(EndMonth) and year == int(EndYear) and count == int(EndDay) + 1:
                break
            rowdata = [row.text for row in table.find_all('td')]
            l = len(rowdata)
            if tableday < 10:
                fulltime = date + "0" + str(tableday)
            else:
                fulltime = date + str(tableday)
            if l > 38:
                temp = []
                temp.append(fulltime)
                for j in range(2, 40, 2):
                    new = ""
                    for a in rowdata[j]:
                        if a == " ":
                            continue
                        elif (a.isnumeric()) == True or a == "." or a == '-':
                            new = new + a
                        else:
                            break
                    temp.append(float(new))
                templist.append(temp)
        if count >= 31 and month == 12:
            break
df = pd.DataFrame(templist, columns=columns)
df[['Average temperature (°F)', 'Average humidity (%)', 'Average dewpoint (°F)',
    'Average barometer (in)', 'Average windspeed (mph)', 'Average gustspeed (mph)',
    'Average direction (°deg)', 'Rainfall for month (in)', 'Rainfall for year (in)', 'Maximum rain per minute',
    'Maximum temperature (°F)', 'Minimum temperature (°F)', 'Maximum humidity (%)', 'Minimum humidity (%)',
    'Maximum pressure', 'Minimum pressure', 'Maximum windspeed (mph)', 'Maximum gust speed (mph)',
    'Maximum heat index (°F)']] = df[['Average temperature (°F)', 'Average humidity (%)', 'Average dewpoint (°F)',
                                      'Average barometer (in)', 'Average windspeed (mph)', 'Average gustspeed (mph)',
                                      'Average direction (°deg)', 'Rainfall for month (in)', 'Rainfall for year (in)',
                                      'Maximum rain per minute',
                                      'Maximum temperature (°F)', 'Minimum temperature (°F)', 'Maximum humidity (%)',
                                      'Minimum humidity (%)',
                                      'Maximum pressure', 'Minimum pressure', 'Maximum windspeed (mph)',
                                      'Maximum gust speed (mph)',
                                      'Maximum heat index (°F)']].apply(pd.to_numeric)

df['Date (yyyy-mm-dd)'] = pd.to_datetime(df['Date (yyyy-mm-dd)'])
df.set_index("Date (yyyy-mm-dd)", inplace=True)
df.to_csv('output.csv')
