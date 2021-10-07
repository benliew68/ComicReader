import cfscrape
from bs4 import BeautifulSoup
from pygame.constants import RESIZABLE, VIDEORESIZE

from storyitem import StoryItem
from mangakakalot import Mangakakalot
from batoto import Batoto

import pygame
import timeit

searchURL = "https://mangakakalot.com/search/story/world"
url = "https://readmanganato.com/manga-qm951521"

displayMode = "single"
#-single
#-double
#-longstrip
#-webtoon

windowResized = False

pygame.init()
WIDTH, HEIGHT = 1366, 768
WIN = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
WHITE = (255, 255, 255)

pygame.display.set_caption("Comic Reader")

def MainMenu():
    while True:
        WIN.fill(WHITE)


def comic(page, x, y):
    WIN.blit(page,(x,y))
    


def main():
    run = True
    windowResized = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.VIDEORESIZE:
                windowResized = True
                
                #pygame.display.update()

        if windowResized:
            
            screenWidth, screenHeight = pygame.display.get_surface().get_size()

            page = pygame.image.load('0.jpg')
            pageHeight = page.get_height()
            pageWidth = page.get_width()

            pageRatio = pageWidth/pageHeight


            adjustedPageHeight = (screenHeight-20)
            adjustedPageWidth = adjustedPageHeight * pageRatio

            if adjustedPageWidth > screenWidth:
                adjustedPageWidth = screenWidth
                adjustedPageHeight = adjustedPageWidth/pageRatio

            page = pygame.transform.scale(page, (int(adjustedPageWidth), int(adjustedPageHeight)))

            pageDisplayX = (screenWidth - adjustedPageWidth)/2
            pageDisplayY = (screenHeight - adjustedPageHeight)/2

            windowResized = False

        WIN.fill(WHITE)
        comic(page, pageDisplayX, pageDisplayY)
        pygame.display.update()



    pygame.quit()

main()


    


    
    

