import pygame
from os.path import join
from random import choice, shuffle

class Card: 
    def __init__(self, colour, number): # card attributes
        assert isinstance(number, int)
        self.colour = colour 
        self.number = number
        self.x = None
        self.y = None
        self.image = {}
        self.rect = None
        self.mask = None
        self.highlighted = False

    def __repr__(self):
        return f"{self.colour} {self.number}"

    def __eq__(self, other): # compares other cards by colour and number
        if not isinstance(other, Card):
            return False
        return self.colour == other.colour and self.number == other.number

    def __hash__(self):
        return hash((self.colour, self.number))    
    
    def update(self, screen, pos, player): # updating card visuals
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
            pygame.draw.rect(screen, "yellow", self.rect.inflate(9, 9))
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
    
    def find_probability(self, card_list): # finding probability of valid group in a given list
        valid_group = 0
        temp_list = []

        for card in  card_list:
            temp_list.append(Card(card.colour, card.number))

        while temp_list:
            self.collection.append(temp_list.pop())
            if self.find_valid_group():
                valid_group += 1
            self.collection.pop()
        
        probability = valid_group/len(card_list)

        return probability

    

class Deck: # Deck class
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

    def deal_cards(self, player_list): # dealing cards at the beginning of the game
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
        self.max_cards = 7 # maximum cards on screen at a time
        self.first_card_index = 0 #index of fist card on screen
        self.drawn_cards = 0
        self.picked_cards = 0
        self.discard_list = [] #keeps track of selected cards to discard
        self.region = None
        self.selected = False
        self.active = False
        self.no_play = 0

    def __repr__(self):
        return f"{self.name}"
    
    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def draw_card(self, deck): #draw card logic
        draw_card = deck.cards.pop()
        self.hand.collection.append(draw_card)
        self.first_card_index = (len(self.hand.collection) // self.max_cards) * self.max_cards
        self.drawn_cards += 1   
        self.no_play = 0   

    def pick_card(self, other): # pick card logic
        picked_card = choice(other.hand.collection)
        other.hand.collection.remove(picked_card)
        self.hand.collection.append(picked_card)
        self.first_card_index = (len(self.hand.collection) // self.max_cards) * self.max_cards
        self.picked_cards += 1
        self.no_play = 0

    def discard_group(self, deck): # discard groups in discard list
        if CollectionOfCards(self.discard_list).is_valid_group():
            for card in self.discard_list:
                card.highlighted = False
                self.hand.collection.remove(card)
                deck.cards.append(card)
            self.discard_list.clear()
            deck.shuffleDeck()
            self.no_play = 0
            return True        
        else:
            return False
        
    def build_playable_groups(self): # makes sequences of playable groups
        sequences = []
        num_set = []
        colour_record, num_record = self.hand.record_builder()            

        checked_nums = set() # Keeping track of checked numbers
        for c, n in colour_record.items():
            sorted_numbers = sorted(set(n)) # returns list of sorted numbers without duplicates
            temp_nums = [-2] # To record sequences            

            for num in sorted_numbers:                 
                if temp_nums[-1] + 1 == num or temp_nums[-1] + 2 == num: 
                    temp_nums.append(num) # Growing sequence                       
                else:
                    if len(temp_nums) > 1:                        
                        sequences.append([Card(c, number) for number in temp_nums]) # Only adding if current sequence length > 1
                    temp_nums = [num] # Reset due to break in sequence

                if num not in checked_nums:
                    colours = set(num_record[num])
                    if len(colours) > 1: # checking for same number, different colour
                        num_set.append([Card(colour, num) for colour in colours])
                    checked_nums.add(num)

            if len(temp_nums) > 1: # Final sequence check                
                sequences.append([Card(c, number) for number in temp_nums])

        return sequences + num_set
    
    def attempt_to_discard(self, deck, num_priority_index, hand_priority_average, checklist): # Uses number priority to make play
            if hand_priority_average < 3: # for low priority hand, discard any group
                if self.hand.find_valid_group():
                    for card in self.hand.find_largest_valid_group():
                        self.hand.collection.remove(card)
                        deck.cards.append(card)
                    deck.shuffleDeck()
                    self.no_play = 0
                    return True

            for card_set in checklist: # for high priority hand trying to discard high priority cards
                set_collection = CollectionOfCards(card_set)
                largest_valid = set_collection.find_largest_valid_group() #largest valid group in card set
                if not largest_valid:
                    continue

                set_collection_average = sum(num_priority_index[card.number] for card in largest_valid) / len(largest_valid)  # priority average of the set

                if set_collection_average >= hand_priority_average: #Only discard the sets that have priority more than hand_average
                    remove_cards = []
                    for card in largest_valid:
                        for my_card in self.hand.collection:
                            if card == my_card:
                                remove_cards.append(my_card)
                                break
                    for card in remove_cards:                        
                        self.hand.collection.remove(card)
                        deck.cards.append(card)
                    deck.shuffleDeck()
                    self.no_play = 0
                    return True

    def attempt_to_pick(self, non_current_players, num_priority_index, hand_priority_average, checklist):
        if hand_priority_average < 3: # picks player with maximum probability            
            max_pick = (None, 0)

            for player in non_current_players:
                pick_probability = self.hand.find_probability(player.hand.collection)
                if pick_probability > max_pick[1]:
                    max_pick = (player, pick_probability) # player with the maximum probability of getting valid group from

            if max_pick[1] > 0:
                if max_pick[1] > (len(self.hand.collection)/3) / len(self.hand.collection):
                    if len(max_pick[0].hand.collection) > 1:
                        self.pick_card(max_pick[0])
                        self.no_play = 0
                        return True
            else:
                if len(self.hand.collection) < 3: # if less than 3 cards and no pick probability
                    self.pick_card(choice(non_current_players))
                    self.no_play = 0
                    return True

        max_pick_priority = {} # picks player that gives max priority valid group

        for card_set in checklist:                    
            set_collection = CollectionOfCards(card_set)
            valid_length = 0
            if set_collection.find_valid_group():
                valid_length = len(set_collection.find_largest_valid_group())

            for player in non_current_players:
                temp_set = [Card(card.colour, card.number) for card in player.hand.collection]

                while temp_set:
                    set_collection.collection.append(temp_set.pop())
                    priority_check_collection = set_collection.find_largest_valid_group()
                    if priority_check_collection: 
                        if len(priority_check_collection) > valid_length:
                            max_priority_average = sum(num_priority_index[card.number] for card in priority_check_collection) / len(priority_check_collection)
                            if max_priority_average > max_pick_priority.get(player, 0):
                                max_pick_priority[player] = max_priority_average                               
                
                    set_collection.collection.pop()                    
        sorted_players = sorted(max_pick_priority, key=lambda player: max_pick_priority[player])
        for player in sorted_players:
            player_hand_priority_average = sum(num_priority_index[card.number] for card in player.hand.collection) / len(player.hand.collection)
            if max_pick_priority[player] >= hand_priority_average and hand_priority_average >= player_hand_priority_average:
                self.pick_card(player)
                self.no_play = 0
                return True
                            

    def attempt_to_draw(self, deck, num_priority_index, hand_priority_average, checklist):
        draw_probability = self.hand.find_probability(deck.cards)
        if draw_probability > 0:
            if draw_probability > (len(self.hand.collection)/3) / len(deck.cards):
                self.draw_card(deck)
                self.no_play = 0
                return True
            else:
                if len(self.hand.collection) < 3:
                    self.draw_card(deck)
                    self.no_play = 0
                    return True           
                
    
    def play_for_me(self, deck, non_current_players):
        while self.active:
            num_priority_index = {1 : 5, 2 : 4, 3 : 3, 4 : 2, 5 : 1, 6 : 1, 7 : 2, 8 : 3, 9 : 4, 10 : 5} #priority index based on availabioity of possible valid groups
            hand_priority_average = sum(num_priority_index[card.number] for card in self.hand.collection) / len(self.hand.collection) #average priority of cards in hand       
            checklist = self.build_playable_groups()  # builds playable groups     

            if checklist:
                if self.attempt_to_discard(deck, num_priority_index, hand_priority_average, checklist): 
                    continue # continue loop from start
                
                if self.picked_cards < 1 and self.attempt_to_pick(non_current_players, num_priority_index, hand_priority_average, checklist):
                    continue # continue loop from start
                
                if self.drawn_cards < 3 and self.attempt_to_draw(deck, num_priority_index, hand_priority_average, checklist):
                    continue # continue loop from start                            
            # plays like medium computer when there is no checklist to work with
            else: 
                if self.picked_cards < 1:
                    max_pick = (None, 0)

                    for player in non_current_players:
                        pick_probability = self.hand.find_probability(player.hand.collection)
                        if pick_probability > max_pick[1]:
                            max_pick = (player, pick_probability)

                    if max_pick[1] > 0:
                        if max_pick[1] > (len(self.hand.collection)/3) / len(self.hand.collection):
                            if len(max_pick[0].hand.collection) > 1:
                                self.pick_card(max_pick[0])
                                self.no_play = 0
                                continue
                    else:
                        if len(self.hand.collection) < 3:
                            self.pick_card(choice(non_current_players))
                            self.no_play = 0
                            continue
                        
                if self.drawn_cards < 3:
                    draw_probability = self.hand.find_probability(deck.cards)
                    if draw_probability > 0:
                        if draw_probability > (len(self.hand.collection)/3) / len(deck.cards):
                            self.draw_card(deck)
                            self.no_play = 0
                            continue
                    else:
                        if len(self.hand.collection) < 3:
                            self.draw_card(deck)
                            self.no_play = 0
                            continue
                
                self.no_play += 1
                if self.no_play >= 3 and self.drawn_cards < 3:
                    self.draw_card(deck)
                    continue

            self.end_turn()        

    def end_turn(self): # end turn logic - resets everything
        self.drawn_cards = 0
        self.picked_cards = 0
        for card in self.discard_list:
            card.highlighted = False
        self.discard_list = [] 
        self.active = False   

    def is_winner(self):
        return len(self.hand.collection) == 0

    def update(self, screen): # updates all player cards on screen
        if self.hand:
            scroll_buffer = None # calculates the last card of the list slice on screen

            if len(self.hand.collection) <= self.max_cards: # reset to 0
                self.first_card_index = 0
                scroll_buffer = len(self.hand.collection) 

            elif len(self.hand.collection) == self.first_card_index: # if equal to first card index starts from first card - max_cards
                scroll_buffer = self.first_card_index
                self.first_card_index -= self.max_cards

            elif len(self.hand.collection) < self.first_card_index: # when less than first card index, starts from last scroll
                self.first_card_index = (len(self.hand.collection) // self.max_cards) * self.max_cards
                scroll_buffer = self.first_card_index + len(self.hand.collection) % self.max_cards
                
            elif len(self.hand.collection) > self.first_card_index: 
                if self.first_card_index + self.max_cards > len(self.hand.collection): # checks for last scroll or not
                    scroll_buffer = self.first_card_index + len(self.hand.collection) % self.max_cards
                else:
                    scroll_buffer = self.first_card_index + self.max_cards 

            gap_between_cards = 5   
            cards_on_screen = scroll_buffer - self.first_card_index
            
            if self.name == "player1":
                x_pos = (self.region.center[0] - ((90 + gap_between_cards) * (cards_on_screen / 2))) + 75
                y_pos = self.region.center[1]
                for card in self.hand.collection[self.first_card_index : scroll_buffer]:
                    card.update(screen, (x_pos, y_pos), self.name)
                    x_pos += card.image[self.name].get_width() + gap_between_cards

            elif self.name == "player2":
                x_pos = (self.region.center[0] - ((90 + gap_between_cards) * (cards_on_screen / 2))) + 75
                y_pos = self.region.center[1]
                for card in self.hand.collection[self.first_card_index : scroll_buffer]:
                    card.update(screen, (x_pos, y_pos), self.name)
                    x_pos += card.image[self.name].get_width() + gap_between_cards

            elif self.name == "player3":
                x_pos = self.region.center[0]
                y_pos = (self.region.center[1] - ((90 + gap_between_cards) * (cards_on_screen / 2))) + 75
                for card in self.hand.collection[self.first_card_index : scroll_buffer]:
                    card.update(screen, (x_pos, y_pos), self.name)
                    y_pos += card.image[self.name].get_height() + gap_between_cards

class HumanPlayer(Player):
    pass

class ComputerPlayer(Player): 
    def __init__(self):
        super().__init__()
        

    def make_move(self, difficulty, deck, non_current_players): #moves for different difficulties
        if difficulty == "easy": #random moves
            move_list = ["draw", "pick", "discard", "end"]
            while self.active:
                random_choice = choice(move_list)
                if random_choice == "draw":
                    if self.drawn_cards < 3:
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
                        deck.cards.append(card)
                    deck.shuffleDeck()

                elif random_choice == "end":
                    self.end_turn()

        elif difficulty == "medium": # more organized
            while self.active:              
                if self.hand.find_valid_group():
                    for card in self.hand.find_largest_valid_group():
                        self.hand.collection.remove(card)
                        deck.cards.append(card)
                    deck.shuffleDeck()
                    self.no_play = 0                
                
                if self.picked_cards < 1:
                    max_pick = (None, 0)

                    for player in non_current_players:
                        pick_probability = self.hand.find_probability(player.hand.collection)
                        if pick_probability > max_pick[1]:
                            max_pick = (player, pick_probability)

                    if max_pick[1] > 0: #some probability of getting a valid group
                        if max_pick[1] > (len(self.hand.collection)/3) / len(self.hand.collection): # max number of groups that can be discarded from hand / number of cards in hand
                            if len(max_pick[0].hand.collection) > 1:
                                self.pick_card(max_pick[0])
                                self.no_play = 0
                                continue
                    else:
                        if len(self.hand.collection) < 3:
                            self.pick_card(choice(non_current_players))
                            self.no_play = 0
                            continue
                        
                if self.drawn_cards < 3:
                    draw_probability = self.hand.find_probability(deck.cards)
                    if draw_probability > 0:
                        if draw_probability > (len(self.hand.collection)/3) / len(deck.cards):
                            self.draw_card(deck)
                            self.no_play = 0
                            continue
                    else:
                        if len(self.hand.collection) < 3:
                            self.draw_card(deck)
                            self.no_play = 0
                            continue
                
                self.no_play += 1
                if self.no_play >= 3 and self.drawn_cards < 3:
                    self.draw_card(deck)
                    continue
                self.end_turn()               

        elif difficulty == "hard": #use priority indexes for numbers and tries to discard high priority cards first
            self.play_for_me(deck, non_current_players)

