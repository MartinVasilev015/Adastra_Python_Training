'''
-define a BlackJackCard class and a Deck class 
so that the following code (which draws 3 cards) will work: 
    d = Deck() 
    h = Hand_Lazy(d.pop(), d.pop(), d.pop()) 
    print(h.total) 
'''
from enum import Enum
import random

class Suit(str, Enum): 
    Club = "♣" 
    Diamond = "♦" 
    Heart = "♥"
    Spade = "♠" 


class Card:
    def __init__(self, suit: Suit, power: str, soft: int, hard: int) -> None:
        self.suit = suit
        self.power = power
        self.soft = soft
        self.hard = hard


class Deck:
    
    cards = []
    
    def __init__(self) -> None:
        self.set_deck()
        self.suffle_deck()

    def set_deck(self):
        for i in Suit:
            for j in range(2, 11):
                card = Card(i, str(j), j, j)
                self.cards.append(card)
            
            for e in ['J', 'Q', 'K', 'A']:
                card = Card(i, str(e), 10, 10)
                if e == 'A':
                    card.hard = 1
                    card.soft = 11
                self.cards.append(card)

    def suffle_deck(self):
        random.shuffle(self.cards)

    def pop(self):
        return self.cards.pop(0)


class Hand:
    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.cards= list(cards)
    
    def __str__(self) -> str:
        return ", ".join(map(str, self.card))

    def __repr__(self) -> str:
        return(
            f"{self.__class__.__name__}"
            f"({self.dealer_card!r},"
            f"{', '.join(map(repr, self.card))}"
        )


class Hand_Lazy(Hand): 
    @property 
    def total(self) -> int: 
        delta_soft = max(c.soft - c.hard for c in self.cards)
        hard_total = sum(c.hard for c in self.cards) 
        if hard_total + delta_soft <= 21: 
            return hard_total + delta_soft 
        return hard_total 
    
    @property 
    def card(self) -> list[Card]: 
        return self._cards 
    
    @card.setter 
    def card(self, aCard: Card) -> None: 
        self._cards.append(aCard) 

    @card.deleter 
    def card(self) -> None: 
        self._cards.pop(-1) 


d = Deck()

h = Hand_Lazy(d.pop(), d.pop(), d.pop())

print(h.total)

#for debugging/testing:
for c in h.cards:
    print(c.suit + c.power)
