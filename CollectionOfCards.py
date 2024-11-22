class Card: 
    def __init__(self, colour, number): 
        assert isinstance(number, int)
        self.colour = colour 
        self.number = number 

    def __str__(self): 
        return f'{self.colour} {self.number}'
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.colour == other.colour and self.number == other.number

    def __hash__(self):
        return hash((self.colour, self.number))


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
