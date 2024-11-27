import pygame
from random import choice, shuffle

class Card: 
    def __init__(self, colour, number): 
        assert isinstance(number, int)
        self.colour = colour 
        self.number = number
        self.x = None
        self.y = None
        self.image = None
        self.rect = None
        self.mask = None

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.colour == other.colour and self.number == other.number

    def __hash__(self):
        return hash((self.colour, self.number))  
    
    def rotate_card(self,screen):
        self.image = pygame.transform.scale(pygame.image.load(f"images\\cards\\{self.colour} {self.number}.png").convert_alpha(), (90, 125))
        self.rect = self.image.get_rect(center = (self.x, self.y))        
        rotated_image = pygame.transform.rotate(self.image, -90)
        screen.blit(rotated_image, self.rect)
    
    def draw(self, screen):
        if self.image is None:
            self.image = pygame.transform.scale(pygame.image.load(f"images\\cards\\{self.colour} {self.number}.png").convert_alpha(), (90, 125))
        self.rect = self.image.get_rect(center = (self.x, self.y))
        screen.blit(self.image, self.rect)



class CollectionOfCards:
    def __init__(self, collection):
        if not collection:
            raise ValueError("Collection is empty!") # Value error for empty list
        self.collection = collection # Should be list of card objects

    def record_builder(self):
        colour_record = {} # Maintains colour: numbers info
        num_record = {} # Maintains number: colour info
        
        for card in self.collection:
            if card.colour in colour_record:
                colour_record[card.colour].append(card.number)
            else:
                colour_record[card.colour] = [card.number] # Populating colour_record
            if card.number in num_record:
                num_record[card.number].append(card.colour)
            else:
                num_record[card.number] = [card.colour] # Populating num_record
        
        return colour_record, num_record


    def is_valid_group(self): # (consecutive numbers, same colour) or (same number, different colours)        
        colour_record, num_record = self.record_builder() # Building Records

        if len(colour_record) == 1: # if same colour
            for numbers in colour_record.values():
                sorted_numbers = sorted(numbers)
                if len(sorted_numbers) <= 2: # if less than 3 cards
                    break                 
                if all(sorted_numbers[i] + 1 == sorted_numbers[i + 1] for i in range(len(sorted_numbers) - 1)): # Checking consecutive numbers
                    return True
                            
        if len(num_record) == 1:
            for colours in num_record.values():
                if len(colours) == len(set(colours)) and len(colours) > 2: # Checking more than 2 unique colours
                    return True
                
        return False
                      
        
    def find_valid_group(self): # finds any valid group, Need to keep track of colours and numbers relations                     
        colour_record, num_record = self.record_builder() # Building Records
        valid_group = set()        
        checked_nums = set() # Keeping track of checked numbers

        for c, n in colour_record.items():
            numbers = set(n)
            for num in numbers:
                if num + 1 in numbers and num + 2 in numbers: # consecutive numbers, same colour
                    colour_set = {Card(c, num), Card(c, num + 1), Card(c, num + 2)}
                    for card in self.collection:
                        if card in colour_set:
                            valid_group.add(card)
                    return list(valid_group)
                
                if num not in checked_nums:
                    colours = set(num_record[num]) # Unique colours
                    if len(colours) > 2: # same number, different colours
                        num_set = {Card(colour, num) for colour in colours}
                        for card in self.collection:
                            if card in num_set:
                                valid_group.add(card)
                        return list(valid_group)
                    checked_nums.add(num) #To avoid rechecking same numbers

        return None
    
    def find_largest_valid_group(self): # maximum number [(same number, different colours = 4), (same colour, consecutive numbers = 10)] which means we need to record all possible valid groups      
        valid_groups = []
        max_valid = set()        
        colour_record, num_record = self.record_builder() # Building Records
        
        checked_nums = set() # Keeping track of checked numbers
        for c, n in colour_record.items():
            sorted_numbers = sorted(set(n)) # returns list of sorted numbers without duplicates
            temp_nums = [-1] # To record sequences

            for num in sorted_numbers:                  
                if temp_nums[-1] + 1 == num: 
                    temp_nums.append(num) # Growing sequence                       
                else:
                    if len(temp_nums) > 2:
                        valid_groups.append([Card(c, number) for number in temp_nums]) # Only adding if current sequence length > 2 
                    temp_nums = [num] # Reset due to break in sequence

                if num not in checked_nums:
                    colours = set(num_record[num])
                    if len(colours) > 2: # checking for same number, different colour
                        valid_groups.append([Card(colour, num) for colour in colours])
                    checked_nums.add(num)

            if len(temp_nums) > 2: # Final sequence check
                valid_groups.append([Card(c, number) for number in temp_nums])

        if valid_groups:
            max_valid_set = set(max(valid_groups, key = len)) # returns valid group of maximum length
            for card in self.collection:
                if card in max_valid_set:
                    max_valid.add(card)
            return list(max_valid)
        
        return None
    

    
class Deck:
  def __init__(self, ):
    self.cards = []
    colours = ["blue", "red", "yellow", "green"]
    numbers = [num for num in range(1, 11)]
    for colour in colours:
        for number in numbers:
            self.cards += [Card(colour, number)] * 2 # Create Deck
    self.image = pygame.Surface((90, 125))
    self.image.fill("blue")
    self.rect = self.image.get_rect(center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))

  #shuffle function
  def shuffleDeck(self):
    shuffle(self.cards)

  def deal_cards(self, player_list):
      self.shuffleDeck()
      for i in range(len(player_list)):    
          collection = []
          for _ in range(5):
              collection.append(self.cards.pop())
          player_list[i].hand = CollectionOfCards(collection)  

  def draw(self, screen):
     screen.blit(self.image, self.rect)
    


class Player:
  def __init__(self):
    self.hand = None
    self.drawn_cards = 0
    self.pick = 0
    self.playing = False
    self.index = None
    self.region = None

  def draw_card(self, deck):
    draw_card = deck.cards.pop()
    self.hand.collection.append(draw_card)
    self.drawn_cards += 1      

  def pick_card(self, other):
    pick_card = choice(other.hand.collection)
    other.hand.collection.remove(pick_card)
    self.hand.collection.append(pick_card)
    self.pick += 1

  def end_turn(self):
    self.draw = 0
    self.pick = 0
    self.playing = False

  def is_winner(self):
    return len(self.hand.collection) == 0
  
  def discard_group(self):
        lst = []
        card_is_enough = False
        while not card_is_enough:
            card_found = False
            print("Which card would you like to select to discard?")
            print("Input 'none' if you don't need anymore:")
            selected_card = input("Card: ")

            if selected_card == "none":
                if self.discard <= 2:
                    print("You need to have selected at least 3 cards to discard")
                    print("\n")
                else:
                    card_is_enough = True
            else:
                for card in self.hand.collection:
                    string = card.colour + " " + str(card.number)
                    if selected_card == string:
                        card_found = True
                        lst.append(card)
                        self.discard += 1
                if not card_found:
                    print("That is not a valid card that you have")
                    print("\n")

        new_collection = CollectionOfCards(lst)
        if new_collection.is_valid_group():
            for c in lst:
                self.hand.collection.remove(c)
            print("\n")
            print("Your cards have been discarded")
            print("\n")
        else:
            print("\n")
            print("Your cards do not make up a valid group")
            print("\n")
  
  
  def draw(self, screen):
    if self.hand is not None:
      if self.index == 0:
        x = (self.WINDOW_WIDTH // 2) - (70 * len(self.hand.collection) / 2)
        y = 600
      elif self.index == 1:
        x = (self.WINDOW_WIDTH // 2) - (70 * len(self.hand.collection) / 2)
        y = 150
      else:
        x = 150
        y = (self.WINDOW_HEIGHT // 2) - (70 * len(self.hand.collection) / 2)    
        
      for card in self.hand.collection:
        if self.index < 2:
          card.x = x
          card.y = y
          card.draw(screen)
          x += card.image.get_width()
        else:
          card.x = x
          card.y = y
          card.rotate_card(screen)
          y += card.image.get_width()



def probability_of_valid_group(card_collection_list):
    hand = card_collection_list[0] # Player 1 hand
    if hand.find_valid_group():
        return 1
    
    colours = ["blue", "red", "yellow", "green"] # List of valid colours
    numbers = [num for num in range(1, 11)] # List of valid numbers
    valid_draws = 0
    deck = []
    player_cards = []
    duplicates = 2

    for colour in colours:
        for number in numbers:
            deck += [Card(colour, number)] * duplicates

    for card_collection in card_collection_list:
        player_cards += [card for card in card_collection.collection]

    removed_cards = []
    for player_card in player_cards:
        for card in deck:
            if card == player_card:
                removed_cards.append(card)
                break
        
    for card in removed_cards:
        deck.remove(card)

    deck_len = len(deck)

    while deck:
        hand.collection.append(deck.pop()) # removing from real deck and adding to player 1 hand 
        if hand.find_valid_group():
            valid_draws += 1 # Counting successful draws
        hand.collection.pop() # Resetting player 1 hand
    
    probability = valid_draws / deck_len # Checking with deck since real_deck became empty
    
    return probability

