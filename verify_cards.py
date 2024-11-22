def verify_cards(card_collection):
    # Storing all the acceptable values in sets
    colour_values = {"red", "green", "yellow", "blue"}
    number_values = {str(x) for x in range(1, 11)} # set of 1 - 10
    card_record = {} # Initialising a dictionary to keep track of number of duplicates
    duplicates = 2 # No. of each Card(colour, number)
    
    # looping through each card in the list
    for card in card_collection:
        card_colour_number = card.split(' ') # Splitting with whitespace specified so that extra whitespaces will not be ignored. 
        if len(card_colour_number) != 2 or card_colour_number[0] not in colour_values or card_colour_number[1] not in number_values: # card_colour_number[0] is <colour> and card_colour_number[1] is <number>
            return False
        if card in card_record:
            card_record[card] += 1 # Counting each card
            if card_record[card] > duplicates: # Checking for extras
                return False
        else:
            card_record[card] = 1  # Adding new card to card_record  
        
    return True



# print(verify_cards(['blue 1', 'blue 1', 'red 3', 'yellow 5', 'green 7', 'blue 9', 'red 7', 'yellow 5', 'green 1']))

