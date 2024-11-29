import pygame
from os.path import join
from random import choice, shuffle

class Card: 
    def __init__(self, colour, number): 
        assert isinstance(number, int)
        self.colour = colour 
        self.number = number
        self.x = None
        self.y = None
        self.image = {}
        self.rect = None
        self.mask = None
        self.highlighted = False

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.colour == other.colour and self.number == other.number

    def __hash__(self):
        return hash((self.colour, self.number))    
    
    def update(self, screen, pos, player):
        if not self.image:
            image = pygame.image.load(join("images", "notty_cards", f"{self.colour} {self.number}.png")).convert()
            self.image["player1"] = image
            self.image["player2"] = image
            self.image["player3"] = pygame.transform.rotate(image, -90)
        # Assigning center positions
        self.x = pos[0]
        self.y = pos[1]
        self.rect = self.image[player].get_rect(center = (self.x, self.y))
        # updating screen
        if self.highlighted == True:
            pygame.draw.rect(screen, "darkblue", self.rect.inflate(9, 9))
        screen.blit(self.image[player], self.rect)

    def IfCardClicked(self, position):
        # Check if the mouse position is within the button's rectangle area
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    


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

        return []
    
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
        
        return []
    

class Deck:
    def __init__(self, pos):
        self.cards = []
        colours = ["blue", "red", "yellow", "green"]
        numbers = [num for num in range(1, 11)]
        for colour in colours:
            for number in numbers:
                self.cards += [Card(colour, number), Card(colour, number)] # Create Deck
        self.image = pygame.image.load(join("images", "notty_cards", "deck.png")).convert()
        self.rect = self.image.get_rect(center = pos)

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

    def update(self, screen):
        screen.blit(self.image, self.rect)
    


class Player:
    def __init__(self):
        self.name = None
        self.hand = None
        self.drawn_cards = 0
        self.picked_cards = 0
        self.discard_list = []
        self.region = None
        self.active = False
        self.selected = False
    
    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def draw_card(self, deck):
        draw_card = deck.cards.pop()
        self.hand.collection.append(draw_card)
        self.drawn_cards += 1      

    def pick_card(self, other):
        picked_card = choice(other.hand.collection)
        other.hand.collection.remove(picked_card)
        self.hand.collection.append(picked_card)
        self.picked_cards += 1


    def discard_group(self, deck):
        if CollectionOfCards(self.discard_list).is_valid_group():
            for card in self.discard_list:
                card.highlighted = False
                self.hand.collection.remove(card)
                deck.cards.append(card)
            self.discard_list.clear()
            deck.shuffleDeck()
            return True
        else:
            return False
    
    def play_for_me(self, deck, player_list):
        pass

    def end_turn(self):
        self.drawn_cards = 0
        self.picked_cards = 0
        for card in self.discard_list:
            card.highlighted = False
        self.discard_list = [] 
        self.active = False   

    def is_winner(self):
        return len(self.hand.collection) == 0


    def update(self, screen):
        if self.hand is not None:
            if self.name == "player1":
                x_pos = self.region.center[0] - (70 * len(self.hand.collection) / 2)
                y_pos = self.region.center[1]
                for card in self.hand.collection:
                    card.update(screen, (x_pos, y_pos), self.name)
                    x_pos += card.image[self.name].get_width()
            elif self.name == "player2":
                x_pos = self.region.center[0] - (70 * len(self.hand.collection) / 2)
                y_pos = self.region.center[1]
                for card in self.hand.collection:
                    card.update(screen, (x_pos, y_pos), self.name)
                    x_pos += card.image[self.name].get_width()

            elif self.name == "player3":
                x_pos = self.region.center[0]
                y_pos = self.region.center[1] - (90 * len(self.hand.collection) / 2)
                for card in self.hand.collection:
                    card.update(screen, (x_pos, y_pos), self.name)
                    y_pos += card.image[self.name].get_height()

class HumanPlayer(Player):
    pass

class ComputerPlayer(Player):
    def __init__(self):
        super().__init__()

    def make_move(self, difficulty, deck, non_current_players):
        if difficulty == "easy":
            move_list = ["draw", "pick", "discard", "end"]
            while self.active:
                random_choice = choice(move_list)
                if random_choice == "draw":
                    if self.drawn_cards <3:
                        self.draw_card(deck)
                    else:
                        move_list.remove("draw")
                elif random_choice == "pick":
                    if self.picked_cards < 1:
                        self.pick_card(choice(non_current_players))
                        move_list.remove("pick")
                elif random_choice == "discard":
                    for card in self.hand.find_largest_valid_group():
                        self.hand.collection.remove(card)
                        deck.append(card)
                    deck.shuffleDeck()
                elif random_choice == "end":
                    self.end_turn()       


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

