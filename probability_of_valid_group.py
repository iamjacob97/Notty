from CollectionOfCards import Card, CollectionOfCards

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
            if player_card.colour == card.colour and player_card.number == card.number:
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

    # colours = ["blue", "red", "yellow", "green"] # List of valid colours
    # numbers = [num for num in range(1, 11)] # List of valid numbers
    # valid_draws = 0 # Successful draws
    # deck = [] # Deck tuples
    # player_cards = [] # Player cards tuples
    # duplicates = 2 # No. of each Card(colour, number)

    # for colour in colours:
    #     for number in numbers:
    #         deck += [(colour, number)] * duplicates # Full deck tuples
    
    # for card_collection in card_collection_list:
    #     player_cards += [(card.colour, card.number) for card in card_collection.collection] # Player card tuples
    

    # for card in player_cards:
    #     deck.remove(card) # Real deck tuples

    # real_deck = [Card(card[0], card[1]) for card in deck] # Building real deck with cards
    
    # while real_deck:
    #     hand.collection.append(real_deck.pop()) # removing from real deck and adding to player 1 hand 
    #     if hand.find_valid_group():
    #         valid_draws += 1 # Counting successful draws
    #     hand.collection.pop() # Resetting player 1 hand
       
    # probability = valid_draws / len(deck) # Checking with deck since real_deck became empty
   
    # return probability

    # colours = {"blue", "red", "yellow", "green"}
    # numbers = [n for n in range(1, 11)]
    # valid_draws = set()
    # player_cards = []
    # duplicates = 2
    # total_cards = len(colours) * len(numbers) * duplicates

    # for card_collection in card_collection_list:
    #     player_cards += [(card.colour, card.number) for card in card_collection.collection] 

    # deck_len = total_cards - len(player_cards)

    # card_record, num_record = hand.record_builder()

    # checked_nums = set()
    # for colour, number_list in card_record.items():        
    #     sorted_numbers = sorted(set(number_list)) # returns list of sorted numbers without duplicates
    #     temp_nums = [-1] # To record sequences

    #     for num in sorted_numbers:                  
    #         if temp_nums[-1] + 1 == num: 
    #             temp_nums.append(num) # Growing sequence     
                                 
    #         else:
    #             if len(temp_nums) > 1:
    #                 if temp_nums[0] == numbers[0]:
    #                     valid_draws.add((colour, temp_nums[1] + 1))                    
    #                 else:
    #                     valid_draws.update([(colour, temp_nums[0] - 1), (colour, temp_nums[1] + 1)])
    #             temp_nums = [num]
                
    #         if num not in checked_nums:                
    #             if len(num_record[num]) > 1:
    #                 for c in (colours - set(num_record[num])):
    #                     valid_draws.add((c, num))
            
    #     if len(temp_nums) > 1:            
    #         if temp_nums[0] == numbers[0]:                
    #             valid_draws.add((colour, temp_nums[1] + 1))
    #         elif temp_nums[1] == numbers[-1]:
    #             valid_draws.add((colour, temp_nums[0] - 1))                    
    #         else:
    #             valid_draws.update([(colour, temp_nums[0] - 1), (colour, temp_nums[1] + 1)])
    
    
    # vdraw_no = len(valid_draws) * duplicates
    # for draw in valid_draws:
    #     if duplicates - player_cards.count(draw) == 0:
    #         vdraw_no -= duplicates
    #     else:
    #         vdraw_no -= player_cards.count(draw)

    # probability = vdraw_no / deck_len

    # return probability

    
            

print(probability_of_valid_group([CollectionOfCards(['blue 1', 'blue 2', 'blue 4'])]))