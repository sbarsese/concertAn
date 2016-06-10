import time
from selenium import webdriver
import re
import datetime
import csv
import os
import math
def process(startPage,thDate,outputFile):
    concerts = []
    #thDate = datetime.datetime.strptime("13/05/2016", "%d/%m/%Y").date()
    #driver = webdriver.Chrome(r"C:\Users\omer\chromedriver\chromedriver.exe")  # Optional argument, if not specified will search path.
    driver = webdriver.Chrome(r"chromedriver.exe")
    #driver.get('http://www.setlist.fm/setlists/bruce-springsteen-2bd6dcce.html');
    driver.get(startPage)
    time.sleep(2) # Let the user actually see something!
    concertsLinks=[concert.get_attribute("href").encode('ascii','ignore') for concert in driver.find_elements_by_css_selector("a.summary")]
    dates = driver.find_elements_by_class_name("dateBlock")
    dates = [re.sub('[\t\n]+',"_",date.text.encode('ascii','ignore')) for date in dates]
    dates = [datetime.datetime.strptime(date, "%b_%d_%Y").date() for date in dates]
    
    isNextPage = False if [date for date in dates if date < thDate] else True
    while (isNextPage):
        nextPage = driver.find_element_by_css_selector('a[title="Go to next page"]').get_attribute("href").encode('ascii','ignore')
        driver.get(nextPage)
        time.sleep(2)
        concertsLinks = concertsLinks + [concert.get_attribute("href").encode('ascii','ignore') for concert in driver.find_elements_by_css_selector("a.summary")]
        '''dates = [re.sub('[\t\n]+',"_",date) for date in [date.text.encode('ascii','ignore') for date in driver.find_elements_by_class_name("dateBlock")]]
        dates = [datetime.datetime.strptime(date, "%b_%d_%Y").date() for date in dates]'''
        dates = driver.find_elements_by_class_name("dateBlock")
        dates = [re.sub('[\t\n]+',"_",date.text.encode('ascii','ignore')) for date in dates]
        dates = [datetime.datetime.strptime(date, "%b_%d_%Y").date() for date in dates]
        isNextPage = False if [date for date in dates if date < thDate] else True
    for concertLink in concertsLinks:
        driver.get(concertLink)
        time.sleep(1)
        date = re.sub('[\t\n]+',"_",driver.find_element_by_class_name("dateBlock").text.encode('ascii','ignore'))
        dateObject = datetime.datetime.strptime(date, "%b_%d_%Y").date()
        if dateObject < thDate:
            break
        headLine = re.sub(',',' ',driver.find_elements_by_css_selector('.setlistHeadline span span')[2].text.encode('ascii','ignore')).split(' ')
        headLine = [elem for elem in headLine if elem]
        country = headLine[-1]
        city = headLine[-2]
        arena = " ".join(headLine[:-2])
        songsElems = driver.find_elements_by_class_name('songLabel')
        songList = [songElem.text.encode('ascii','ignore').replace(',','.') for songElem in songsElems]
        
        concerts.append({"date":date,"dateObject":dateObject,"country":country,"city":city,"arena":arena,"songList":songList})
        
    driver.close()
    outputFileName = outputFile+os.sep+'concerts.csv'
    with open(outputFileName,'wb') as file:
        writer = csv.writer(file)
        writer.writerow(["date","country","city","arena","idx","song"])
        for concert in concerts:
            rows = [[concert["dateObject"],concert["country"],concert["city"],concert["arena"],idx+1,concert["songList"][idx]] for idx in range(len(concert["songList"]))]
            writer.writerows(rows)
    
    dateDistinct = set()
    dateDistinct2 = set()
    for concert in concerts:
        dateDistinct.add((concert["date"],concert["dateObject"],0))
        dateDistinct2.add((concert["date"],concert["dateObject"],0))
    dateRank = {}
    for date in dateDistinct:
        dateRank[date[0]] = math.log(1+sum([1 for d in dateDistinct2 if d[1] <= date[1]]))
    #dateRank = {date[0]:math.log(1+date[2]) for date in dateDistinct}
    songsRank = {}
    for concert in concerts:
        for song in concert["songList"]:
            if song not in songsRank:
                songsRank[song] = 0
            songsRank[song] += dateRank[concert["date"]]
    
    songsRankList = sorted(songsRank.iteritems(),key=lambda song: song[1], reverse = True)
    outputFileName1 = outputFile+os.sep+'concertsRank.csv'
    with open(outputFileName1,'wb') as file:
        writer = csv.writer(file)
        for row in songsRankList:
            writer.writerow([row[0],row[1]])

    os.system("start "+outputFileName)
    os.system("start "+ outputFileName1)
'''if __name__ == '__main__':
    concerts = []
    thDate = datetime.datetime.strptime("13/05/2016", "%d/%m/%Y").date()
    driver = webdriver.Chrome(r"C:\Users\omer\chromedriver\chromedriver.exe")  # Optional argument, if not specified will search path.
    driver.get('http://www.setlist.fm/setlists/bruce-springsteen-2bd6dcce.html');
    time.sleep(2) # Let the user actually see something!
    concertsLinks=[concert.get_attribute("href").encode('ascii','ignore') for concert in driver.find_elements_by_css_selector("a.summary")]
    dates = driver.find_elements_by_class_name("dateBlock")
    dates = [re.sub('[\t\n]+',"_",date.text.encode('ascii','ignore')) for date in dates]
    dates = [datetime.datetime.strptime(date, "%b_%d_%Y").date() for date in dates]
    
    isNextPage = False if [date for date in dates if date < thDate] else True
    while (isNextPage):
        nextPage = driver.find_element_by_css_selector('a[title="Go to next page"]').get_attribute("href").encode('ascii','ignore')
        driver.get(nextPage)
        time.sleep(2)
        concertsLinks = concertsLinks + [concert.get_attribute("href").encode('ascii','ignore') for concert in driver.find_elements_by_css_selector("a.summary")]

        dates = driver.find_elements_by_class_name("dateBlock")
        dates = [re.sub('[\t\n]+',"_",date.text.encode('ascii','ignore')) for date in dates]
        dates = [datetime.datetime.strptime(date, "%b_%d_%Y").date() for date in dates]
        isNextPage = False if [date for date in dates if date < thDate] else True
    for concertLink in concertsLinks:
        driver.get(concertLink)
        time.sleep(1)
        date = re.sub('[\t\n]+',"_",driver.find_element_by_class_name("dateBlock").text.encode('ascii','ignore'))
        dateObject = datetime.datetime.strptime(date, "%b_%d_%Y").date()
        if dateObject < thDate:
            break
        headLine = re.sub(',',' ',driver.find_elements_by_css_selector('.setlistHeadline span span')[2].text.encode('ascii','ignore')).split(' ')
        headLine = [elem for elem in headLine if elem]
        country = headLine[-1]
        city = headLine[-2]
        arena = " ".join(headLine[:-2])
        songsElems = driver.find_elements_by_class_name('songLabel')
        songList = [songElem.text.encode('ascii','ignore').replace(',','.') for songElem in songsElems]
        
        concerts.append({"date":date,"dateObject":dateObject,"country":country,"city":city,"arena":arena,"songList":songList})
        x=5
    with open('concerts.csv','wb') as file:
        writer = csv.writer(file)
        writer.writerow(["date","country","city","arena","idx","song"])
        for concert in concerts:
            rows = [[concert["dateObject"],concert["country"],concert["city"],concert["arena"],idx+1,concert["songList"][idx]] for idx in range(len(concert["songList"]))]
            writer.writerows(rows)

'''
