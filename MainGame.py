import pygame #Imports pygame modules.
import sys #Imports the sys module.
from GameSetup import * #Imports everything from GameSetup.
from Button import * #Imports everything from Button.
from CollectionOfCards import * #Imports everything from CollectionOfCards.
from GameOver import GameOver #Imports GameOver class.

class MainGame(GameSetup):
    def __init__(self, screen, clock, manager):
        super().__init__(screen, clock, manager)
        self.background_image = pygame.image.load(join("images", "backgrounds", "gamescreen.png")) #This is the background image that will be loaded in, as this class inherits the function that puts the background image onto the screen.
        self.font = pygame.font.Font(join("images", "backgrounds", "font.ttf"), 17) #Font for words.
        self.deck = Deck(((self.screen.get_width()//2), (self.screen.get_height()//2))) #Where the deck image will be loaded in and deck object is created.

        self.deckaudio = pygame.mixer.Sound(join("audio", "dealcards.mp3"))
        self.deckaudio1 = pygame.mixer.Sound(join("audio", "cardsound.mp3"))
        self.deckaudio2 = pygame.mixer.Sound(join("audio", "mouseclick.mp3"))
        self.deckaudio3 = pygame.mixer.Sound(join("audio", "correct.mp3"))
        self.deckaudio4 = pygame.mixer.Sound(join("audio", "wrong.mp3"))
        self.players = [HumanPlayer()]
        for _ in range(self.manager.get_shared_data()["numberofplayers"] - 1): #Sets everyone else a computer player
            self.players.append(ComputerPlayer())
        #Creates a region for each player based on the index created using the enumerate function.
        for i, player in enumerate(self.players):
            player.name = f"player{i + 1}"
            if i == 0:
                player.region = pygame.Rect((self.screen.get_width()//16) * 3, (self.screen.get_height()//16) * 12, 
                                            (self.screen.get_width()//16) * 9, (self.screen.get_height()//16) * 4)
            elif i == 1:
                player.region = pygame.Rect((self.screen.get_width()//16) * 3, 0, 
                                            (self.screen.get_width()//16) * 9, (self.screen.get_height()//16) * 4)
            elif i == 2:
                player.region = pygame.Rect(0, (self.screen.get_height()//16), 
                                            (self.screen.get_width()//16) * 3, (self.screen.get_height()//16) * 12)
                #Player 3 has a maximum of 5 cards it shows, due to the aesthetic choice of our game.
                player.max_cards = 5
        self.player_index = 0 #This is updated everytime a player goes.
        self.current_player = self.players[self.player_index] #This is used later to determine current player.
        self.current_player.active = True
        self.buttons = [Button("deal", (self.screen.get_width()//2, self.screen.get_height()//3), "DEAL", self.font, "white", "green")] #The deal button needs to start the game.
        self.labels = []
        self.objects = [self.deck] + self.buttons + self.players + self.labels #This is the objects list, which is updated with a list of buttons in the game and draws them onto the screen using the draw function.

    def showLabel(self, label):
        self.labels.append(label)
        self.update()
        self.draw()
        pygame.time.wait(1000)
        self.labels.clear()
        self.update()
        self.draw()


    def deal_cards(self): #This function creates all the buttons in the games once the deal button is pressed. Game buttons are general game buttons, and player_buttons are those which denote a certain player.
        game_buttons = [Button("draw", ((self.screen.get_width()//8) * 7, (self.screen.get_height()//9) * 2), "DRAW CARD", self.font, "white", "green"),
                        Button("pick", ((self.screen.get_width()//8) * 7, (self.screen.get_height()//9) * 3), "PICK CARD", self.font, "white", "green"),
                        Button("discard", ((self.screen.get_width()//8) * 7, (self.screen.get_height()//9) * 4), "DISCARD", self.font, "red", "red"),
                        Button("play", ((self.screen.get_width()//8) * 7, (self.screen.get_height()//9) * 5), "PLAY FOR ME", self.font, "white", "green"),
                        Button("end", ((self.screen.get_width()//8) * 7, (self.screen.get_height()//9) * 6), "END TURN", self.font, "white", "green"),
                        Button("player1-prev", ((self.screen.get_width()//16) * 5, self.screen.get_height() - 17), "prev", self.font, "red", "red"),
                        Button("player1-next", ((self.screen.get_width()//16) * 11, self.screen.get_height() - 17), "next", self.font, "red", "red"),
                        Button("player2-prev", ((self.screen.get_width()//16) * 5, 17), "prev", self.font, "red", "red"),
                        Button("player2-next", ((self.screen.get_width()//16) * 11, 17), "next", self.font, "red", "red"),
                        Button("player3-prev", (17, (self.screen.get_height()//16) * 5), "prev", self.font, "red", "red", -90),
                        Button("player3-next", (17, (self.screen.get_height()//16) * 11), "next", self.font, "red", "red", -90)]
        
        player_buttons = [Button("player1", (self.screen.get_width()//2, self.screen.get_height() - 17), "player1", self.font, "white", "white"),
                          Button("player2", (self.screen.get_width()//2, 17), "player2", self.font, "white", "white"), 
                          Button("player3", (17, self.screen.get_height()//2), "player3", self.font, "white", "white", -90)]
        #this uses the deal_cards function from the deck class, taking in self.players as a parameter to distribute the cards to. If there are 3 players, self.buttons is set to all the buttons above. However, if the length of the players is 2, we do not include 'player3-prev', 'player3-next', and 'player3' as this is not needed.
        self.deck.deal_cards(self.players)
        if len(self.players) == 3:
            self.buttons = player_buttons + game_buttons
        else:
            self.buttons = player_buttons[:2] + game_buttons[:-2]
        self.update() #This updates the positions of all the objects in the list of objects.
        self.draw() #This displays the objects on the screen.

    def select_player(self): #This function is run when you click the pick button when it's your turn and you have not already picked a card.
        self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "PICK PLAYER", self.font, "green")) #Pick player label is shown to tell you to pick a player.
        non_current_players = [player for player in self.players if player != self.current_player] #List of players that are non-current players.
        any_selected = False
        while not any_selected: #This will run as no player has been selected to pick from.
            for button in self.buttons[:len(self.players)]: #This for loop looks through the player buttons and turns the current player's button red, indicating that they cannot be picked from.
                if button.name == self.current_player.name:
                    button.base_colour = "red"
                    button.hovering_colour = "red"
                else: #Otherwise, if the player button is yellow you can pick from that player.
                    button.hovering_colour = "yellow"
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.changeColour
                self.draw() #This for loop logic is drawn onto the screen.

            for event in pygame.event.get():
                if event.type == pygame.QUIT: #If we press quit in the pygame window,
                    pygame.quit()
                    sys.exit() #exits the program.
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #If we lefthand click on any of the other players, that player is returned. This logic is continued in the pick button from lines 168-176.
                    for player in non_current_players:
                        if player.region.collidepoint(event.pos):
                                for button in self.buttons[:len(self.players)]:
                                    button.base_colour = "white"
                                    button.hovering_colour = "white"
                                return player

    def next_player(self): #This function sets the current player index.
        self.player_index = (self.player_index + 1) % len(self.players) #In a 2 player game, if the previous player index was 0, it will be 1 and 1 % 2 is 1. However, if the previous player index was 1, it would be 0 as 2 % 2 is 0. If there are 3 players, 1 % 3 is 1, 2%3 is 2 and 0%3 is 0.
        self.current_player = self.players[self.player_index] #Current player set to player in list of players based on player_index.
        self.current_player.active = True
        for button in self.buttons[len(self.players):]:
                button.base_colour = "white"
                button.hovering_colour = "green"
        

    def computer_move(self):#When the type of current player is not a human player, this method is called, which calls the make_move method from computer player class, and depending on the difficulty has different logic.
        non_current_players = [player for player in self.players if player != self.current_player]
        self.current_player.make_move(self.manager.get_shared_data()["difficulty"], self.deck, non_current_players)
        self.next_player() #After the make_move logic has been made, the next_player method is called.

    def main_game_events(self):
        # DISCARD turns white only when discard group available
        for button in self.buttons[len(self.players):]:
            if button.name == "discard":
                if self.current_player.hand.find_valid_group():
                    button.base_colour = "white"
                    button.hovering_colour = "green"
                else:
                    button.base_colour = "red"
                    button.hovering_colour = "red"
            
            for player in self.players: 
                if button.name == f"{player.name}-prev": 
                    if player.first_card_index <= 0: #if starting card is first card
                        button.base_colour = "red"
                        button.hovering_colour = "red"
                    else:
                        button.base_colour = "white"
                        button.hovering_colour = "yellow"
                elif button.name == f"{player.name}-next": 
                    if len(player.hand.collection) - player.first_card_index <= player.max_cards: #if on the last card
                        button.base_colour = "red"
                        button.hovering_colour = "red"
                    else:
                        button.base_colour = "white"
                        button.hovering_colour = "yellow"


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() #Exits the program.

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:

                    if button.name == "deal" and button.IfButtonClicked(event.pos): #If the deal button is clicked, deal_cards() is called.
                        self.deal_cards()
                        self.deckaudio.play()                         

                    if button.name == "draw" and button.IfButtonClicked(event.pos): #If draw is clicked...
                        if self.current_player.drawn_cards < 3: #If player has drawn less than 3 cards this round...
                            self.current_player.draw_card(self.deck) #Draw a card from the deck.
                            if self.current_player.drawn_cards == 3: #If 3 cards drawn, draw button turns red to indicate you cannot draw.
                                button.base_colour = "red"
                                button.hovering_colour = "red"
                            self.draw()
                            self.deckaudio1.play()   
                        else:
                            self.deckaudio4.play()
                            self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "YOU HAVE ALREADY DRAWN 3 CARDS", self.font, "yellow")) #If try and click draw button and drawn 3 cards, this label temporarily appears.

                    if button.name == "pick" and button.IfButtonClicked(event.pos): #If pick button is clicked...
                        if self.current_player.picked_cards < 1: #And you have picked less than 1 card...
                            button.base_colour = "yellow"
                            selected_player = self.select_player() #When you click on a player button, that returns the associated player (method also described on line 79-104).
                            self.current_player.pick_card(selected_player) #Pick card from that selected player.
                            self.deckaudio1.play()   
                            if selected_player.is_winner(): #If you pick a card from that player and they have no more cards left, the winner becomes that player in the shared_data. Game_state is changed to GameOver.
                                self.manager.shared_data["winner"] = selected_player.name
                                self.manager.change_state(GameOver(self.screen, self.clock, self.manager))
                                self.running = False

                            button.base_colour = "red" #Goes to red when picked.
                            button.hovering_colour = "red"                                                
                        else:
                            self.deckaudio4.play()
                            self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "YOU HAVE ALREADY PICKED A CARD", self.font, "yellow")) #Label to remind you that you have already picked a card if click on pick card and have already picked a card this turn.
                            
                    if button.name == "discard" and button.IfButtonClicked(event.pos): #If the discard button is clicked...
                        if len(self.current_player.discard_list) >= 3: #If the amount of cards highlighted is 3 or more...
                            if self.current_player.discard_group(self.deck): #If the group is a valid group it is discarded.
                                self.deckaudio3.play()   
                                if self.current_player.is_winner(): #Checks if current player's a winner.
                                    self.manager.shared_data["winner"] = self.current_player.name #if so, changes winner to current player.
                                    self.manager.change_state(GameOver(self.screen, self.clock, self.manager)) #changes state to 'GameOver'.
                                    self.running = False
                            else:
                                self.deckaudio4.play()
                                self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "NOT A VALID GROUP", self.font, "yellow")) #If the cards you've selected don't make a valid group and you click discard, this comes up.
                        else:
                            self.deckaudio4.play()
                            self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "SELECT AT LEAST 3 CARDS", self.font, "yellow")) #If you select less than 3 cards and try to discard, this label appears.

                    if button.name == "play" and button.IfButtonClicked(event.pos): #If the play button is pressed.
                        non_current_players = [player for player in self.players if player != self.current_player]
                        self.current_player.play_for_me(self.deck, non_current_players) #The computer plays for the current player.
                        self.deckaudio2.play()
                        for player in self.players:
                            if player.is_winner():
                                self.manager.shared_data["winner"] = player.name
                                self.manager.change_state(GameOver(self.screen, self.clock, self.manager))
                                self.running = False
                        self.next_player() #After the play_for_me logic, it moves onto the next player.

                    if button.name == "end" and button.IfButtonClicked(event.pos): #If the end button is pressed, the current player's turn is ended and it moves onto the next player.
                        self.current_player.end_turn()
                        self.deckaudio2.play()
                        self.next_player()

                    if button.name == "player1-prev" and button.IfButtonClicked(event.pos):#Allows scrolling backwards through the player's hand
                        self.players[0].first_card_index -= self.players[0].max_cards #Decreases the player's hand by the number of cards that can be shown at once then scrolls backwards to the previous screen
                        if self.players[0].first_card_index < 0: #checks if the decrement is negative if so sets it to 0 to maintain the display within the desired limits
                            self.players[0].first_card_index = 0
                        self.draw()
                        self.deckaudio2.play()
                    
                    if button.name == "player1-next" and button.IfButtonClicked(event.pos):#Allows scrolling forward through the player's hand
                        self.players[0].first_card_index += self.players[0].max_cards#increases the index by the maximum number of cards that can be displayed on the screen at once(max_cards)
                        self.draw() #redraws the screen with the updated player's hand new index after scrolling forward
                        self.deckaudio2.play()
                    
                    if button.name == "player2-prev" and button.IfButtonClicked(event.pos):
                        self.players[1].first_card_index -= self.players[1].max_cards
                        if self.players[1].first_card_index < 0:
                            self.players[1].first_card_index = 0
                        self.draw()
                        self.deckaudio2.play()
                    
                    if button.name == "player2-next" and button.IfButtonClicked(event.pos):
                        self.players[1].first_card_index += self.players[1].max_cards
                        self.draw()
                        self.deckaudio2.play()

                    if button.name == "player3-prev" and button.IfButtonClicked(event.pos):
                        self.players[2].first_card_index -= self.players[2].max_cards
                        if self.players[2].first_card_index < 0:
                            self.players[2].first_card_index = 0
                        self.draw()
                        self.deckaudio2.play()
                    
                    if button.name == "player3-next" and button.IfButtonClicked(event.pos):
                        self.players[2].first_card_index += self.players[2].max_cards
                        self.draw()
                        self.deckaudio2.play()

                if self.current_player.hand:
                    last_card_index = None
                    if len(self.current_player.hand.collection) - self.current_player.first_card_index  >= self.current_player.max_cards:
                        last_card_index = self.current_player.first_card_index + self.current_player.max_cards
                    else:
                        last_card_index = self.current_player.first_card_index + len(self.current_player.hand.collection) % self.current_player.max_cards
                    for card in self.current_player.hand.collection[self.current_player.first_card_index : last_card_index]:
                        if card.IfCardClicked(event.pos):
                            if not card.highlighted:
                                card.highlighted = True
                                self.current_player.discard_list.append(card)
                            else:
                                card.highlighted = False
                                self.current_player.discard_list.remove(card)


    def update(self): #Adds all of the buttons into a list called objects.
        self.objects = [self.deck] + self.buttons + self.players + self.labels
    
    def draw(self): #This is where the screen is constantly reloaded.
        self.screen.blit(self.background_image, (0, 0)) #Puts the background image onto the screen.
        for obj in self.objects: #Changes colour of buttons if they've been highlighted.
            if type(obj) == Button:
                obj.changeColour(pygame.mouse.get_pos())
            obj.update(self.screen)
        pygame.display.flip()   #Refreshes the screen.             

    def run(self):
        while self.running:
            self.clock.tick(60)

            if type(self.current_player) == HumanPlayer:
                self.main_game_events() #Clicking buttons.

            else:
                self.computer_move() #Computer player makes a move.
                for player in self.players:
                    if player.is_winner(): #If a player runs out of cards, they become the winner and the state is changed to 'GameOver'.
                        self.manager.shared_data["winner"] = player.name
                        self.manager.change_state(GameOver(self.screen, self.clock, self.manager))
                        self.running = False
                        
            self.draw()
            
            

 



