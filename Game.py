from CollectionOfCards import *
from Deck import *
from Player import *

class Game:
    def __init__(self, names):
        self.players = [Player(name) for name in names]
        self.player_index = 0
        self.current_player = self.players[self.player_index]
        self.deck = Deck()

    def deal_cards(self):
        self.deck.shuffleDeck()
        for i in range(len(self.players)):    
            collection = []
            for _ in range(5):
                collection.append(self.deck.cards.pop())
            self.players[i].hand = CollectionOfCards(collection)
    
    def view_cards(self):
        for player in self.players:
            print(f"{player.name}'s cards are")
            for card in player.hand.collection:
                print(card)

    def next_player(self):
        self.player_index = (self.player_index + 1) % len(self.players)
        self.current_player = self.players[self.player_index]


        
    
