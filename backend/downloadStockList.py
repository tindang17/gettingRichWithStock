import requests
import json
import csv


def DownloadStockList():
    stockList = []
    count = 0
    for i in range(1, 21):
        url = "https://www.nasdaq.com/api/v1/screener?page=" + \
            str(i) + "&pageSize=300"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        data = json.loads(response.text)

        for stock in data['data']:
            count += 1
            temp = []
            temp.append(stock['ticker'])
            stockList.append(temp)
            print(count)

    with open('stockList.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(stockList)
    print()


DownloadStockList()
