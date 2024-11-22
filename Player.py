import random
from CollectionOfCards import *
from Deck import *

class Player:
  def __init__(self, name):
    self.name = name
    self.hand = None
    self.draw = 0
    self.pick = 0
    self.playing = False

  def draw_card(self, deck):
    draw_card = deck.cards.pop()
    self.hand.collection.append(draw_card)
    self.draw += 1 
      

  def pick_card(self, other):
    pick_card = random.choice(other.hand.collection)
    other.hand.collection.remove(pick_card)
    self.hand.collection.append(pick_card)
    self.pick += 1

  def end_turn(self):
    self.draw = 0
    self.pick = 0
    self.playing = False

  # def find_valid_group(self):
  #   valid_group = self.collection.find_valid_group()
  #   if valid_group:
  #     for card in valid_group:
  #       self.collection.collection.remove(card)
  #     return valid_group
  #   return None

  # def discard_group(self, group, deck):
  #   for card in group:
  #     if card not in self.hand.collection:
  #       return False 

  #   for card in group:
  #     self.collection.collection.remove(card)
  #   deck.extend(group)
  #   return True

  def is_winner(self):
    return len(self.hand.collection) == 0
