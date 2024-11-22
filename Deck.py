import random
from CollectionOfCards import *

class Deck:
  def __init__(self):
    self.cards = []
    colours = ["blue", "red", "yellow", "green"]
    numbers = [num for num in range(1, 11)]
    duplicates = 2
    for colour in colours:
        for number in numbers:
            self.cards += [Card(colour, number)] * duplicates # Create Deck
    

  #shuffle function
  def shuffleDeck(self):
    random.shuffle(self.cards)

  

      
 
       

