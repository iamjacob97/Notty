import pygame
import sys
from Button import *
from GameSetup import *
from GameStateManager import *
from CollectionOfCards import *


class MainGame(GameSetup):
    def __init__(self, screen, clock, manager):
        super().__init__(screen, clock, manager)
        self.background_image = pygame.image.load(join("images", "backgrounds", "gamescreen.png"))
        self.font = pygame.font.Font(join("images", "backgrounds", "font.ttf"), 17)
        self.deck = Deck(((self.screen.get_width()//2), (self.screen.get_height()//2)))
        # self.players = [HumanPlayer()]
        # for _ in range(self.manager.get_shared_data()["numberofplayers"] - 1):
        #     self.players.append(ComputerPlayer())
        if self.manager.get_shared_data()["numberofplayers"] == 2:
            self.players = [HumanPlayer(), ComputerPlayer()]
        elif self.manager.get_shared_data()["numberofplayers"] == 3:
            self.players = [HumanPlayer(), HumanPlayer(), HumanPlayer()]
        for i, player in enumerate(self.players):
            player.name = f"player{i + 1}"
            if i == 0:
                player.region = pygame.Rect((self.screen.get_width()//16) * 3, (self.screen.get_height()//16) * 12, 
                                            (self.screen.get_width()//16) * 9, (self.screen.get_height()//16) * 4)
            elif i == 1:
                player.region = pygame.Rect((self.screen.get_width()//16) * 3, 0, 
                                            (self.screen.get_width()//16) * 9, (self.screen.get_height()//16) * 4)
            elif i == 2:
                player.region = pygame.Rect(0, (self.screen.get_height()//16) * 2, 
                                            (self.screen.get_width()//16) * 3, (self.screen.get_height()//16) * 12)
                player.max_cards = 5
        self.player_index = 0
        self.current_player = self.players[self.player_index]
        self.current_player.active = True
        self.buttons = [Button("deal", (self.screen.get_width()//2, self.screen.get_height()//3), "DEAL", self.font, "white", "green")]
        self.labels = []
        self.objects = [self.deck] + self.buttons + self.players + self.labels

    def showLabel(self, label):
        self.labels.append(label)
        self.update()
        self.draw()
        pygame.time.wait(1000)
        self.labels.clear()
        self.update()
        self.draw()


    def deal_cards(self):
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
        
        self.deck.deal_cards(self.players)
        if len(self.players) == 3:
            self.buttons = player_buttons + game_buttons
        else:
            self.buttons = player_buttons[:2] + game_buttons[:-2]
        self.update()
        self.draw()

    def select_player(self):
        self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "PICK PLAYER", self.font, "green"))
        non_current_players = [player for player in self.players if player != self.current_player]
        any_selected = False
        while not any_selected:
            for button in self.buttons[:len(self.players)]:
                if button.name == self.current_player.name:
                    button.base_colour = "red"
                    button.hovering_colour = "red"
                else:
                    button.hovering_colour = "yellow"
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.changeColour
                self.draw()        

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for player in non_current_players:
                        if player.region.collidepoint(event.pos):
                                for button in self.buttons[:len(self.players)]:
                                    button.base_colour = "white"
                                    button.hovering_colour = "white"
                                return player

    def next_player(self):
        self.player_index = (self.player_index + 1) % len(self.players)
        self.current_player = self.players[self.player_index]
        self.current_player.active = True
        for button in self.buttons[len(self.players):]:
                button.base_colour = "white"
                button.hovering_colour = "green"

    def computer_move(self):
        non_current_players = [player for player in self.players if player != self.current_player]
        self.current_player.make_move(self.manager.get_shared_data()["difficulty"], self.deck, non_current_players)
        self.next_player()

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
                    if player.first_card_index <= 0:
                        button.base_colour = "red"
                        button.hovering_colour = "red"
                    else:
                        button.base_colour = "white"
                        button.hovering_colour = "yellow"
                elif button.name == f"{player.name}-next":
                    if len(player.hand.collection) - player.first_card_index <= player.max_cards:
                        button.base_colour = "red"
                        button.hovering_colour = "red"
                    else:
                        button.base_colour = "white"
                        button.hovering_colour = "yellow"


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:

                    if button.name == "deal" and button.IfButtonClicked(event.pos):
                        self.deal_cards()                         

                    if button.name == "draw" and button.IfButtonClicked(event.pos):
                        if self.current_player.drawn_cards < 3:
                            self.current_player.draw_card(self.deck)
                            if self.current_player.drawn_cards == 3:
                                button.base_colour = "red"
                                button.hovering_colour = "red"
                            self.draw()
                        else:
                            self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "YOU HAVE ALREADY DRAWN 3 CARDS", self.font, "yellow"))

                    if button.name == "pick" and button.IfButtonClicked(event.pos):
                        if self.current_player.picked_cards < 1:
                            button.base_colour = "yellow"
                            selected_player = self.select_player()
                            self.current_player.pick_card(selected_player)
                            if selected_player.is_winner():
                                self.manager.shared_data["winner"] = selected_player.name
                                print(self.manager.get_shared_data())
                                print(f"{selected_player.name} is the winner")
                            button.base_colour = "red"
                            button.hovering_colour = "red"                                                
                        else:
                            self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "YOU HAVE ALREADY PICKED A CARD", self.font, "yellow"))
                            
                    if button.name == "discard" and button.IfButtonClicked(event.pos):
                        if len(self.current_player.discard_list) >= 3:
                            if self.current_player.discard_group(self.deck):
                                if self.current_player.is_winner():
                                    self.manager.shared_data["winner"] = self.current_player.name
                                    print(self.manager.get_shared_data())
                                    print(f"{self.current_player.name} is the winner")
                            else:
                                self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "NOT A VALID GROUP", self.font, "yellow"))
                        else:
                            self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "YOU NEED AT LEAST 3 CARDS", self.font, "yellow"))
                    
                    if button.name == "end" and button.IfButtonClicked(event.pos):
                        self.current_player.end_turn()
                        self.next_player()

                    if button.name == "player1-prev" and button.IfButtonClicked(event.pos):
                        self.players[0].first_card_index -= self.players[0].max_cards
                        if self.players[0].first_card_index < 0:
                            self.players[0].first_card_index = 0
                        self.draw()
                    
                    if button.name == "player1-next" and button.IfButtonClicked(event.pos):
                        self.players[0].first_card_index += self.players[0].max_cards
                        self.draw()
                    
                    if button.name == "player2-prev" and button.IfButtonClicked(event.pos):
                        self.players[1].first_card_index -= self.players[0].max_cards
                        if self.players[1].first_card_index < 0:
                            self.players[1].first_card_index = 0
                        self.draw()
                    
                    if button.name == "player2-next" and button.IfButtonClicked(event.pos):
                        self.players[1].first_card_index += self.players[0].max_cards
                        self.draw()

                    if button.name == "player3-prev" and button.IfButtonClicked(event.pos):
                        self.players[2].first_card_index -= self.players[0].max_cards
                        if self.players[2].first_card_index < 0:
                            self.players[2].first_card_index = 0
                        self.draw()
                    
                    if button.name == "player3-next" and button.IfButtonClicked(event.pos):
                        self.players[2].first_card_index += self.players[0].max_cards
                        self.draw()

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


    def update(self):
        self.objects = [self.deck] + self.buttons + self.players + self.labels
    
    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        for obj in self.objects:
            if type(obj) == Button:
                obj.changeColour(pygame.mouse.get_pos())
            obj.update(self.screen)
        pygame.display.flip()                

    def run(self):
        while self.running:
            self.clock.tick(60)
            if type(self.current_player) == HumanPlayer:
                self.main_game_events()
            else:
                self.computer_move()
            self.draw()
            
            

 



