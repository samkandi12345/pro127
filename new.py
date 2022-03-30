from tkinter import BROWSE
from unicodedata import name
from wsgiref import headers
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests
star_data = []
starturl = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("C:\Users\samra\Downloads\chromedriver_win32")
browser.get(starturl)
time.sleep(10) 

def scrap():
    headers = ["Name","Distance","Mass","Radius"]
    star_data = []
    for i in range(0,428):
        soup = BeautifulSoup(browser.page_source,"html.parser")
        for ul_tag in soup.find_all("ul",attrs={"class","exoplanets"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index,li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            star_data.append(temp_list)
        browser.find_element_by_xpath("/html/body/div[3]/div[3]/div[5]/div[1]")
    with open("file.csv","w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(star_data)

new_star_data = []

def scrap_more_data(hyperlink):
    page = requests.get(hyperlink)
    soup = BeautifulSoup(page.content,"html.parsar")
    for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
        td_tags = tr_tag.find_all("td")
        temp_list = []
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
            except:
                temp_list.append("")
            new_star_data.append(temp_list)

    pass

for data in star_data:
    scrap_more_data(data[5])

for index,data in enumerate(star_data):
    new_star_data.append(data+new_star_data[index])

with open("csv2.csv","w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(new_star_data)
