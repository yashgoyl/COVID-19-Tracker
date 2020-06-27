from plyer import notification
import requests
from bs4 import BeautifulSoup
import time
from tabulate import tabulate
import numpy as np
from fpdf import FPDF
import pdfkit
import os
import matplotlib.pyplot as plt 
import csv
from reportlab.pdfgen import canvas 
from openpyxl import Workbook


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
    
    # notifyMe("Yash", "lets stop the spreaf the virus togehter")
    myHtmlData = getData("https://www.mohfw.gov.in/")
    soup = BeautifulSoup(myHtmlData, 'html.parser')
    # print(soup.prettify())

    extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
    header = extract_contents(soup.tr.find_all('th'))
    SHORT_HEADERS = ['SNo', 'State','Total-Active-Cases','Cured','Death','Total-Confirmed-Cases']  


    all_rows = soup.find_all('tr')  
    stats = []
    for row in all_rows[1:]:  
        stat = extract_contents(row.find_all('td')) 
        
        if stat:  
            if len(stat) == 5:  
                # last row  
                stat = ['', *stat]  
                stats.append(stat)  
            elif len(stat) == 6:  
                stats.append(stat)

    stats[-1][0] = len(stats)
    stats[-1][1] = "Total Cases"

    #list of all states
    objects = []
    for row in stats:
        objects.append(row[1])
    # print(objects)

    #position of each state in objects list
    y_pos = np.arange(len(objects))
    # print(y_pos)

    #list of Active Cases of all states
    performance = []
    for row in stats[:len(stats)-1]:
        performance.append(int(row[2]))

    performance.append(int(stats[-1][2][:len(stats[-1][2])-1]))

# Below 2 lines is to built table for getting all details of corona virus cases in india.
    table = tabulate(stats, headers=SHORT_HEADERS, tablefmt="pretty")
    print(table)
    # below 6 lines will convert this table to .csv file
    with open('stats.csv', 'w', newline='') as f:
        thewriter = csv.writer(f)

        thewriter.writerow(SHORT_HEADERS)
        for i in stats:
            thewriter.writerow(i)

    wb = Workbook()
    ws = wb.active
    with open('stats.csv', 'r') as f:
        for row in csv.reader(f):
            ws.append(row)
    wb.save('stats.xlsx')


    # pdfkit.from_file('stats.csv', 'stats.pdf')

    # f = open('stats.txt','w')
    # f.write(table)
    # f.close()

# # Next 7 lines is to convert text file to pdf using pdfkit
#     pdf = FPDF()
#     pdf.add_page(orientation='P')
#     pdf.set_font('Arial', size = 11)
#     f = open('new.csv','r')
#     for x in f:
#         pdf.cell(300, 15, txt = x, ln= 1, align="L") 
#     pdf.output("stats.pdf") 
# 

# Below Code is for Notification
    states = ['Rajasthan', 'Maharashtra', 'Uttar Pradesh', 'Delhi']
    
    for dataList in stats[36:37]:    
        nTitle = "Total Cases of Cornavirus in INDIA till now"
        nText = f"Total Active cases in India: {dataList[2]}\nTotal Patients Cured/ Discharged: {dataList[3]}\nTotal Deaths: {dataList[4]}\nTotal Confirmed Cases: {dataList[5]}"
        notifyMe(nTitle,nText)
        time.sleep(2)

    for dataList in stats[:35]:
        if dataList[1] in states:
            # print(dataList)
            nTitle = "Cases of COVID-19"
            nText = f"State {dataList[1]}:\nTotal Active Cases: {dataList[2]}\nCured/ Discharged: {dataList[3]}\nDeaths: {dataList[4]}\nTotal Confirmed Cases: {dataList[5]}"
            notifyMe(nTitle, nText)
            time.sleep(4)
    

    # Below 11 lines is to plot graph of Active Cases of all Cities in india using Matplotlib
    plt.barh(y_pos, performance, align='center', alpha=0.5,  
                    color=(234/256.0, 128/256.0, 252/256.0),  
                    edgecolor=(106/256.0, 27/256.0, 154/256.0))  
    plt.yticks(y_pos, objects)  
    plt.xlim(1,performance[-1]+1000) 
    plt.subplots_adjust(left=0.25) 
    plt.xlabel('Number of Cases')  
    plt.title('Corona Virus Cases in India                                      Total Confirmed Cases = ')
    plt.text(14400, 39.3, int(stats[36][5]), horizontalalignment='center', verticalalignment='center')
    # plt.savefig('stats.png') 
    plt.show()

    time.sleep(3600)
