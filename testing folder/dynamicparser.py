import storyitem

url = "https://bato.to/series/73818"

#source = storyitem.ReturnSource(url)
#module = __import__(source)
#sourceClass = getattr(module, source.capitalize())


Source2 = getattr(storyitem.ReturnSourceClass(url), 'GetStoryDetails')


print(Source2(url).url)