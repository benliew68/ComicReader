class StoryItem:
    url = None
    cover = None
    
    title = "Unknown Title"
    authors = []
    status = "Unknown Status"
    genres = []

    description = "No Description Found!"
    chapterCount = "Unknown Chapter Count"
    
    chapterListNames = []
    chapterListLinks = []

'''
class user:
    name = None
    password = None
    mangaInLibrary = [["url", "chap", "page"], 
                      ["url", "chap", "page"], 
                      ["url", "chap", "page"]]
'''

def ReturnSource(url):
    SOURCEDICT = {
        "Batoto": "https://bato.to/",
        "Manganato": "https://manganato.com/",
        "Readmanganato": "https://readmanganato.com/",
        "Mangakakalot": "https://mangakakalot.com/",
        "Mangadex": "empty for now",
        "Webtoons": "https://www.webtoons.com/"
    }

    for key, value in SOURCEDICT.items():
        if url.startswith(value):
            return key

def StringToNestedList(inputString):
    try:
        prelimList = inputString.split(",")
        subList = [prelimList[n:n+3] for n in range(0, len(prelimList), 3)]
        return subList
    except:
        print("Error occurred getting library list from database")
    


def NestedListToString(list):
    returnList = []
    for innerList in list:
        for item in innerList:
            returnList.append(item)
    
    returnString = ','.join(map(str, returnList))

    return returnString



