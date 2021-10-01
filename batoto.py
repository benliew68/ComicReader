from sys import set_coroutine_origin_tracking_depth
import cfscrape
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.options import Options

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

import undetected_chromedriver.v2 as uc

import requests

import time

from storyitem import StoryItem

captcha = "?__cf_chl_managed_tk__=pmd_IvwydZVzjt2mv3CtEACLWmj9V4HzCJ7BOcH26nuwUKs-1632713970-0-gqNtZGzNAxCjcnBszQpl"


class Batoto:
    def Search(query):
        itemNames = []
        itemLinks = []
        itemCovers = []

        url = "https://bato.to/search?word=" + query.replace(' ', '+')
        
        scraper = cfscrape.create_scraper()
        html = scraper.get(url).content
        doc = BeautifulSoup(html, 'lxml')


        #Parse data
        for storyItem in doc.find_all("div", {"class": "col item line-b no-flag"}):
            #Get story title
            itemName = storyItem.find("a", {"class": "item-title"})
            itemName = itemName.text.strip()
            itemNames.append(itemName)
            
            #Gets link to the actual comic
            #Batoto returns its links as /series/id/name so we prepend the base url
            itemLink = storyItem.find("a").get("href")
            itemLink = "https://bato.to" + itemLink
            itemLinks.append(itemLink)
            
            #Get links to title cover images
            itemCovers.append(storyItem.find("img").get("src"))

        return itemNames, itemLinks, itemCovers
        

    def GetStoryDetails(url):
        scraper = cfscrape.create_scraper()
        html = scraper.get(url).content
        doc = BeautifulSoup(html, 'lxml')

        myChapterListNames = []
        myChapterListLinks = []
        myAuthorList = []
        myGenreList = []

        story = StoryItem()


        story.url = url

        #Store the cover image
        try:
            cover = doc.find("div", {"class": "col-24 col-sm-8 col-md-6 attr-cover"})
            story.cover = cover.find("img").get("src")
        except:
            print("No authors found!")
        

        #Store the title
        try:
            title = doc.find("h3", {"class":"item-title"})
            title = title.text.strip()
            story.title = title
        except:
            print("No title found!")
        
        #Store the authors, status, genres
        for entry in doc.find_all("div", {"class": "attr-item"}):
            if "Authors:" in entry.text.strip():
                for author in entry.find_all("a"):
                    myAuthorList.append(author.text.strip())
                    

            if "Release status:" in entry.text.strip():
                story.status = entry.find("span").text.strip()
                
            if "Genres:" in entry.text.strip():
                firstEntry = entry.find("span")
                for genre in firstEntry.find_all():
                    myGenreList.append(genre.text.strip())
                    

        try:
            description = doc.find("div", {"class": "limit-html"}).text.strip()
            story.description = description
        except:
            print("No description found!")

        try:
            chapterCountStr = doc.find("div", {"class": "head"}).text.strip()
            
            #filter returns an iterable so join it to get a str back, then cast it
            chapterCount = int(''.join(filter(str.isdigit, chapterCountStr)))
            story.chapterCount = chapterCount
        except:
            print("No chapter count found!")
        
        #Get the chapter names and links
        #Reverse chapter list because it is received from most recent to least
        for chapter in doc.find_all("div", {"class":"p-2 d-flex flex-column flex-md-row item"})[::-1]:

            #Get chapter name
            chapterName = chapter.find("a").text.replace('\n','').strip()


            #Get chapter link
            chapterLink = chapter.find("a").get("href")

            #Returns as /chapter/1401113 so we prepend the base url
            chapterLink = "https://bato.to" + chapterLink

            myChapterListNames.append(chapterName)
            myChapterListLinks.append(chapterLink)

        story.genres = myGenreList
        story.authors = myAuthorList
        story.chapterListNames = myChapterListNames
        story.chapterListLinks = myChapterListLinks
        
        
        return story
                    
    def GetChapterImages(url):
        '''scraper = cfscrape.create_scraper()
        html = scraper.get(url).content
        doc = BeautifulSoup(html, 'lxml')'''

        '''driver = uc.Chrome(options=options)
        with driver:
            driver.get(url) '''


        #options.add_argument('--headless')
        #uncomment

        '''options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--window-size=1280,720")'''
        

        chapterImageLinks = []

        options = Options()

        driver = webdriver.Firefox(options=options)
        driver.get(url)
        #print(driver.get_cookie("__cf_bm"))
        #myCookies = driver.get_cookie("__cf_bm")
        

        #session = HTMLSession()
        #scraper = cfscrape.create_scraper(sess=session)
        #r = scraper.get(url, cookies=myCookies)
        #page_source = r.html.render()
        #page_source = r.html.raw_html

        #scraper = cfscrape.CloudflareScraper().get(url).content
        #scraper.html.render()
        #scraper.html.raw_html

        #print(scraper)
        page_source = driver.page_source

        

        #webURL = urllib.request.urlopen(url).read()
        doc = BeautifulSoup(page_source, 'lxml')

        #imageViewer = doc.find("div", {"id": "viewer"})
        for image in doc.find_all("img"):
            imageURL = image.get("src")
            if imageURL.startswith("https://"):
                chapterImageLinks.append(imageURL)
        
        driver.quit()

        return chapterImageLinks
            

        
        
        
        


        
                


        


#item = Batoto.GetStoryDetails("https://bato.to/series/73818/world-tatto")

#print(Batoto.GetChapterImages("https://bato.to/chapter/1438385"))
#print(Batoto.GetChapterImages("https://bato.to/chapter/1438385"))

'''x=0
for image in imageList:
    img_data = requests.get(image).content
    with open('{}.jpg'.format(x), 'wb') as handler:
        handler.write(img_data)
    x += 1

print(imageList)
'''