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
The user object stored in the database
class user:
    name = None
    password = None
    mangaInLibrary = [["url", "chap", "page"], 
                      ["url", "chap", "page"], 
                      ["url", "chap", "page"]]
'''

def ReturnSourceClass(url):
    SOURCEDICT = {
        "batoto": "https://bato.to/",
        "manganato": "https://manganato.com/",
        "readmanganato": "https://readmanganato.com/",
        "mangakakalot": "https://mangakakalot.com/",
        "mangadex": "https://mangadex.org/",
        "webtoons": "https://www.webtoons.com/"
    }

    for source, value in SOURCEDICT.items():
        if url.startswith(value):
            sourcename = f"sources." + source
            module = __import__(sourcename, fromlist=['sources'])
            sourceClass = getattr(module, source.capitalize())

            return sourceClass

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



