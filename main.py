import pygame
import time
import sys
from models import *
from engine import *
from nao import *

pygame.init()
file = open(sys.argv[1]+".txt","w")
gameEngine = Memory()
startGame = False 
playerCanClick = False

BACKGROUND_COLOUR = [13, 91, 1]

#These values control the position of the facedown cards 
MARGIN = 50 #Distance from left edge to first card left edge
HEADER = 240 #Distance from top edge to first card top edge
VSPACING = 225 #Distance between the left edge of one card and the left edge of the next
HSPACING = 300 #Distance between the top edge of one card and the top edge of the card under it

#number of seconds to show the deck cards for
DELAY = 20

#number of rounds to play
ROUNDS = 5
CURRENT_ROUND = 1

#array of success for each round
roundSuccess = []
compliance = []

firstTime = True

# list with all face-down card coordinates
coordList = [[MARGIN, HEADER], [MARGIN + VSPACING, HEADER], [MARGIN + 2*VSPACING, HEADER], [MARGIN + 3*VSPACING, HEADER], [MARGIN + 4*VSPACING, HEADER], [MARGIN, HEADER + HSPACING], [MARGIN + VSPACING, HEADER + HSPACING], [MARGIN + 2*VSPACING, HEADER + HSPACING], [MARGIN + 3*VSPACING, HEADER + HSPACING], [MARGIN + 4*VSPACING, HEADER + HSPACING]]
# list with all the cards (index +1 = cardID)
cardList = gameEngine.deck.getDeck()

#create the display surface
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#colour window
DISPLAYSURF.fill(BACKGROUND_COLOUR)
#create window caption
pygame.display.set_caption('Memory')

mainLoop = True
allowShowDeck = False
naoHelp = False
intro = True


def renderGame():
    DISPLAYSURF.fill(BACKGROUND_COLOUR)

    for card in cardList:
        cardID = card.cardID
        coords = coordList[cardID-1]
        global playerCanClick
        if(card.flipUp):
            DISPLAYSURF.blit(card.image, coords)
            playerCanClick = False
        else:
            DISPLAYSURF.blit(card.backImage, coords)


    if gameEngine.state == GameState.PLAYING:
        playerCanClick = True
        topCard = gameEngine.pile.showTop()
        if (topCard != None):
            DISPLAYSURF.blit(topCard.image, (1300, 50))
    else:
        DISPLAYSURF.blit(cardList[0].backImage, (1300, 50))

#show deck to player for DELAY seconds (change variable above)
def showDeck():
    DISPLAYSURF.fill(BACKGROUND_COLOUR)
    global gameEngine

    for card in cardList:
        cardID = card.cardID
        coords = coordList[cardID-1]
        DISPLAYSURF.blit(card.image, coords)

    DISPLAYSURF.blit(cardList[0].backImage, (1300, 50))
    
    pygame.display.update()
    pygame.time.delay(DELAY*1000)
    gameEngine.state = GameState.PLAYING
    pygame.event.clear()


def flipCard(card):
    card.flipUp = not card.flipUp
    renderGame()
    pygame.display.update()
    time.sleep(1.5)
    card.flipUp = not card.flipUp
    renderGame()
    pygame.event.clear()


while mainLoop:
    nao = NAO()
    #nao.eventCheck()

    if (naoHelp):
        time.sleep(1.5)
        nao.help(CURRENT_ROUND)
        naoHelp = False

    key = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #quit pygame
            mainLoop = False
        
        #initial keydowns
        if event.type == pygame.KEYDOWN:
            #quit pygame
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] and keys[pygame.K_DELETE]:
                mainLoop = False
            elif gameEngine.state == GameState.WAITING:
                #show deck and start game
                if (event.key == pygame.K_SPACE):
                    nao.introduction()
                elif (event.key == pygame.K_RETURN):
                    showDeck()
                    startGame = True
                elif (event.key == pygame.K_s):
                    renderGame()
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (playerCanClick):
            x, y = event.pos
            for cardID, card in enumerate(cardList):
                if (card.collidepoint(x, y, coordList[cardID])):
                    if CURRENT_ROUND <= ROUNDS and playerCanClick:
                        flipCard(card)
                        gameEngine.results.append(cardID)
                        topCard = gameEngine.pile.showTop()
                        playerCanClick = False
                        if (cardID+1) == topCard.cardID:
                            roundSuccess.append(1)
                            nao.correct(CURRENT_ROUND)
                        else:
                            roundSuccess.append(0)
                            nao.incorrect(CURRENT_ROUND)
                        if(cardID+1) == nao.suggestions[CURRENT_ROUND-1]:
                            compliance.append(1)
                        else:
                            compliance.append(0)

                        CURRENT_ROUND += 1
                        gameEngine.pile.nextCard()
                        naoHelp = True
                    break

    if gameEngine.state == GameState.PLAYING:
        renderGame()

    #if NAO.clickStart, set GameState to PICKING_CARD (player game has actually started)
    pygame.display.update()

    if startGame == True:
        startGame = False
        time.sleep(1)
        nao.help(1)

#print clicked cards
file.write(','.join([str(x) for x in gameEngine.results]))
file.write("\n")
file.write(','.join([str(x) for x in roundSuccess]))
file.write("\n")
file.write(','.join([str(x) for x in compliance]))

nao.shutdown()

pygame.quit()
sys.exit()

