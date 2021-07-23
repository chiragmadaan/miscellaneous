# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
status = "Hit or Stand?"
dealer_pos = (80,235)
player_pos = (80,435)

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
    def draw_invert(self, canvas, pos):
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_BACK_SIZE)
        
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.acecount = 0

    def __str__(self):
        val = "Hand contains "
        for i in self.cards:
            val = val + str(i) + " "
        return val

    def add_card(self, card):
        self.cards.append(card)
        if card.get_rank() == 'A':
            self.acecount += 1

    def get_value(self):
        val = self.acecount * 10
        for i in self.cards:
            val += VALUES[i.get_rank()]
        if val > 21:
            temp = self.acecount
            while temp > 0 and val > 21:
                val -= 10
                temp -=1
        return val
   
    def draw(self, canvas, pos):
        posx = pos[0]
        posy = pos[1]
        for c in self.cards:
            c.draw(canvas,[posx,posy])
            posx += CARD_SIZE[0] + 20
            
    def draw_invert(self, canvas, pos):
        self.cards[0].draw_invert(canvas,pos)
        self.cards[1].draw(canvas,[pos[0] + CARD_SIZE[0] + 20, pos[1]])
    
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for i in SUITS:
            for j in RANKS:
                self.cards.append(Card(i,j))
        random.shuffle(self.cards)
        
    def shuffle(self):
        self.cards = []
        for i in SUITS:
            for j in RANKS:
                self.cards.append(Card(i,j))
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(len(self.cards) - 1)
    
    def __str__(self):
        val = "Deck contains "
        for i in self.cards:
            val += str(i) + " "
        return val


#define event handlers for buttons
def deal():
    global outcome, in_play, test_deck, player, dealer, score, status
    if in_play:
        outcome = "You lose."
        score -= 1
    else:
        outcome = ""
    player = Hand()
    dealer = Hand()
    test_deck.shuffle()
    player.add_card(test_deck.deal_card())
    dealer.add_card(test_deck.deal_card())
    player.add_card(test_deck.deal_card())
    dealer.add_card(test_deck.deal_card())
    status = "Hit or Stand?"
    in_play = True
    

def hit():
    global player, in_play, status, score, outcome
    if not in_play:
        return
    player.add_card(test_deck.deal_card())
    if player.get_value() > 21:
        outcome = "You have busted."
        score -= 1
        status = "New Deal?"
        in_play = False
    
def stand():
    global in_play, dealer, test_deck, score, outcome, status
    if not in_play:
        return
    in_play = False
    sum = dealer.get_value()
    while sum < 17:
        dealer.add_card(test_deck.deal_card())
        sum = dealer.get_value()
    if sum > 21:
        outcome = "Dealer went bust, you win."
        score += 1
        status = "New Deal?"
        return
    if sum >= player.get_value():
        outcome = "You lose."
        score -= 1
        status = "New Deal?"
    else:
        outcome = "You win."
        score += 1
        status = "New Deal?"

# draw handler    
def draw(canvas):
    canvas.draw_text("BlackJack", (100, 100), 50, "Cyan")
    canvas.draw_text("Score: " + str(score), (400, 100), 35, "Black")
    canvas.draw_text("Dealer", (80, 200), 35, "Black")
    canvas.draw_text(str(outcome), (250, 200), 35, "Black")
    canvas.draw_text("Player", (80, 400), 35, "Black")
    canvas.draw_text(str(status), (250, 400), 35, "Black")
    if in_play:
        dealer.draw_invert(canvas,dealer_pos)
    else:
        dealer.draw(canvas,dealer_pos)
    player.draw(canvas,player_pos)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
frame.start()

test_deck = Deck()
deal()

# remember to review the gradic rubric
