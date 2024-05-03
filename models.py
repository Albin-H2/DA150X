import pygame
SIZE = 0.4
class Card:
    image = None
    cardID = None
    flipUp = None

    # cardID is the number used to refer to this specific type of card, this number ranges from 1-10.  
    def __init__(self, cardID):
        image = pygame.image.load('imgs/' + str(cardID) + '.png')
        self.image = pygame.transform.scale(image, (int(500*SIZE), int(726*SIZE)))

        backImage = pygame.image.load('imgs/back.png')
        self.backImage = pygame.transform.scale(backImage, (int(500*SIZE), int(726*SIZE)))

        self.cardID = cardID
        self.flipUp = False

    def collidepoint(self, x, y, corner):
        if ((x > corner[0]) & (y > corner[1]) & (x < (corner[0] + 500*SIZE)) & (y < (corner[1] + 726*SIZE))):
            return True
        
        return False

class Deck:
    deck = None

    def __init__(self):
        deck = []
        iter = 1
        while iter <= 10:
            card = Card(iter)
            deck.append(card)
            iter += 1
        self.deck = deck

    def getDeck(self):
        return self.deck


class Pile:
    cards = None

    # initialise pile with array of 5 cards
    def __init__(self, deck, pileCards):
        cards = []
        iter = 1
        while iter <= 5:
            cards.append(deck[pileCards[iter-1]-1])
            iter += 1
        self.cards = cards

    # remove last/top card from pile, ie after each round to progress to next card
    def nextCard(self):
        del self.cards[-1]
    
    def showTop(self):
        if (len(self.cards)>0):
            # cards[-1] returns the 1st indexed card from the right (so last card)
            return self.cards[-1]
        else:
            return None
        

