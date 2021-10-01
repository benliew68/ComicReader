import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebChannel import QWebChannel
import bs4 as bs
import urllib.request

class Client(QWebChannel):

    def __init__(self, url):
        self.app = QGuiApplication(sys.argv)
        QWebChannel.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()
        
    def on_page_load(self):
        self.app.quit()
        
url = 'https://bato.to/chapter/1418860'
client_response = Client(url)
source = client_response.mainFrame().toHtml()
soup = bs.BeautifulSoup(source, 'lxml')
js_test = soup.find('div', {"id": "viewer"})
print(js_test.text)