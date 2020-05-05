from plyer import notification
import requests
from bs4 import BeautifulSoup
import time

def notifyMe(title, message):
    notification.notify(
        title = title,
        message = message,
        app_name = 'Corona Stats',
        app_icon = '/home/devilyash/Documents/Python/Coronavirus Cases Notifier/icon14.png',
        timeout = 20
    )

def getData(url):
    r = requests.get(url)
    return r.text

if __name__ == "__main__":
    while True:
        # notifyMe("Yash", "lets stop the spreaf the virus togehter")
        myHtmlData = getData("https://www.mohfw.gov.in/")
        soup = BeautifulSoup(myHtmlData, 'html.parser')
        # print(soup.prettify())

        myDataStr = ""
        for tr in soup.find_all('tbody')[0].find_all('tr'):
            myDataStr += tr.get_text()
        myDataStr = myDataStr[1:]
        # print(myDataStr)
        itemList = myDataStr.split("\n\n")

        states = ['Rajasthan', 'Maharashtra', 'Uttar Pradesh']
        total = ['Total number of confirmed cases in India']
        for i in itemList[32:35]:
            dataList = i.split('\n')
            if dataList[0] in total:
                nTitle = "Total Cases of Cornavirus in INDIA"
                nText = f"Total number of confirmed cases in India: {dataList[1]}\nTotal Patients Cured/ Discharged: {itemList[33]}\nTotal Deaths: {itemList[34][1:5]}"
                notifyMe(nTitle,nText)
                time.sleep(2)

        for item in itemList[:32]:
            dataList = item.split('\n')
            # print(dataList)
            if dataList[1] in states:
                # print(dataList)
                nTitle = "Cases of COVID-19"
                nText = f"State {dataList[1]}:\nTotal Cases: {dataList[2]}\nCured/ Discharged: {dataList[3]}\nDeaths: {dataList[4]}"
                notifyMe(nTitle, nText)
                time.sleep(4)
        time.sleep(3600)
