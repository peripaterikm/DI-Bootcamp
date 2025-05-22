#Ex.1
# A class is a blueprint for creating objects, defining their attributes and behaviors. 

# An instance is a specific object created from a class with actual values. 

# Encapsulation means hiding internal data and providing controlled access through methods, which protects the integrity of the data. Abstraction focuses on exposing only the essential features of an object while hiding complex details.

# Inheritance allows one class to receive the properties and methods of another, promoting code reuse.

# Multiple inheritance means a class can inherit from more than one parent class. 

# Polymorphism enables methods with the same name to behave differently depending on the object calling them. 

# Method Resolution Order (MRO) is the sequence Python uses to determine which method to execute when multiple inherited classes define the same method.


#Ex.2
import random

# Card class with suit and value
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

# Deck class that manages a list of Card objects
class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """Builds a full deck of 52 cards"""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = [Card(suit, value) for suit in suits for value in values]

    def shuffle(self):
        """Shuffles the deck"""
        self.build()
        random.shuffle(self.cards)

    def deal(self):
        """Deals one card from the deck"""
        if self.cards:
            return self.cards.pop()
        else:
            return "No more cards in the deck."

deck = Deck()
deck.shuffle()

print("Dealing 5 cards:")
for _ in range(5):
    print(deck.deal())

print(f"\nCards left in deck: {len(deck.cards)}")
