import cfscrape
from bs4 import BeautifulSoup

from storyitem import StoryItem

class Mangakakalot:
    def Search(query):
        itemNames = []
        itemLinks = []
        itemCovers = []

        url = "https://mangakakalot.com/search/story/" + query.replace(' ', '_')
        

        scraper = cfscrape.create_scraper()
        html = scraper.get(url).content
        doc = BeautifulSoup(html, 'lxml')

        
        
        for storyItem in doc.find_all("div", {"class": "story_item"}):
            #Get the story name
            itemNames.append(storyItem.find("img").get("alt"))

            #Get the link to the actual comic
            itemLinks.append(storyItem.find("a").get("href"))

            #Get the link to the comic's cover
            itemCovers.append(storyItem.find("img").get("src"))
        
        #Returns the values as lists
        return itemNames, itemLinks, itemCovers

    def GetStoryDetails(url):
        scraper = cfscrape.create_scraper()
        html = scraper.get(url).content
        doc = BeautifulSoup(html, 'lxml')
        
        story = StoryItem()

        #Get title of story
        story.title = doc.find("h1").text.strip()
        

        #Info is stored in a table so parse for data
        table = doc.find("table", {"class": "variations-tableInfo"})
        #print(table)
        table_body = table.find("tbody")
        rows = table_body.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            info = row.text.strip()

            if "Author(s) :" in info:
                info = info.replace("Author(s) :", '')
                info = info.strip()
                authors = info.split(' - ')
                
                for author in authors:
                    story.authors.append(author)
            
            if "Status :" in info:
                info = info.replace("Status :", '')
                info = info.strip()
                story.status = info
            
            if "Genres :" in info:
                info = info.replace("Genres :", '')
                info = info.strip()
                genres = info.split(' - ')

                for genre in genres:
                    story.genres.append(genre)

        #Get the description
        description = doc.find("div", {"class": "panel-story-info-description"})
        description = description.text.strip()
        description = description.replace('Description :', '')
        description = description.strip()
        
        story.description = description

        chapterList = doc.find("ul", {"class": "row-content-chapter"})
        numChapters = 0
        for chapters in chapterList.find_all("li"):
            numChapters += 1
        #print(numChapters)

        '''print(story.title)
        print(story.authors)
        print(story.status)
        print(story.genres)
        print(story.description)'''

        return story
