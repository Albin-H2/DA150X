from enum import Enum
import pygame
from models import *

class GameState(Enum):
    WAITING = 0
    PLAYING = 1
    ENDED = 2

class Memory:
    pile = None
    deck = None
    state = None
    results = None
    currentRound = None
    # contains cardIDs of pile cards
    pileCards = [1, 7, 5, 10, 3]

    def __init__(self):
        self.deck = Deck()
        self.pile = Pile(self.deck.getDeck(), self.pileCards)
        self.state = GameState.WAITING
        self.currentRound = 0
        self.results = []

    def play(self, cardID):
        # player picks a matching card
        if cardID == self.pile.showTop:
            self.currentRound = self.currentRound + 1
        # add chosen cardID to results array
        self.results.append(cardID)