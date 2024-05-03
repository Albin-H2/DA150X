from naoqi import ALProxy
import random

CONFIDENT = True

class NAO:
    tts = ALProxy("ALTextToSpeech", "169.254.196.174", 9559) #var 169 254 76 12
    life = ALProxy("ALAutonomousLife", "169.254.196.174", 9559)

    confident = None
    previous = None
    suggestions = [3, 10, 2, 7, 1]
    confidentResponses = ["I am absolutely sure that the middle card in the top row is the correct card", "This time i am totally sure that the rightmost card in the bottom row is the correct card", "I am confident that the matching card is definitely the second card from the left in the top row", "The second card from the left in the bottom row is certainly the correct one", "I have no doubt that you should turn over the leftmost card in the top row", "That's it thank you for playing"]
    unconfidentResponses = ["I think that maybe the middle card in the top row is the correct card", "I am not sure but this time I think that rightmost card in the bottom row may be the correct card", "I believe that the matching card is probably the second card from the left in the top row", "The second card from the left in the bottom row is maybe the correct one", "I believe that you should turn over the leftmost card in the top row", "That's it thank you for playing"]
    correctResponses = ["We did it", "Great job", "We rock!", "Fantastic!", "Nice", "I knew we could do it"]
    incorrectResponses = ["Oh no that was wrong", "better luck next time", "Oops that was incorrect", "Oh no we picked the wrong card"]

    def __init__(self):
        self.confident = CONFIDENT
        self.life.setState("solitary")
        
    def introduction(self):
        self.tts.say("Hello, my name is Toad and we are going to play a game. When you press the enter key on your keyboard you will get to see 10 cards for 20 seconds. The cards will then be turned face down. After this a set of 5 new cards will be turned face up one at a time. Our task is to match each of these cards with one of the 10 face down cards. I will help you and advise where the cards are")
        self.tts.say("Press ENTER to start or press SPACEBAR if you want me to repeat the instructions")

    def correct(self, round):
        if (round == 3):
            self.tts.say("Oh, I was wrong, but you got it anyway! Good job!")
        else:
            self.tts.say(self.correctResponses[random.randint(0,5)])

    
    def incorrect(self, round):
        if (round == 3):
            self.tts.say("Oh, sorry, looks like I was wrong!")
        else:
            self.tts.say(self.incorrectResponses[random.randint(0,3)])


    def help(self, round):
        if(self.confident):
            self.tts.say(self.confidentResponses[round-1])
            print(self.confidentResponses[round-1])
        else:
            self.tts.say(self.unconfidentResponses[round-1])
            print(self.unconfidentResponses[round-1])

    def shutdown(self):
        self.life.setState("disabled")
