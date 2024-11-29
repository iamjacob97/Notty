import pygame
import sys
from Button import *
from GameSetup import GameSetup
from CollectionOfCards import *


class MainGame(GameSetup):
    def __init__(self, screen, clock, manager):
        super().__init__(screen, clock, manager)

        self.deck = Deck(((self.screen.get_width()//2), (self.screen.get_height()//2)))
        if self.manager.get_shared_data()["numberofplayers"] == 2:
            self.players = [Player(), Player()]
        elif self.manager.get_shared_data()["numberofplayers"] == 3:
            self.players = [Player(), Player(), Player()]
        for i, player in enumerate(self.players):
            player.name = f"player{i + 1}"
            if i == 0:
                player.region = pygame.Rect((self.screen.get_width()//4), (self.screen.get_height()//4) * 3, 
                                            (self.screen.get_width()//4) * 2, (self.screen.get_height()//4))
            elif i == 1:
                player.region = pygame.Rect((self.screen.get_width()//4), 0, (self.screen.get_width()//4) * 2, (self.screen.get_height()//4))
            elif i == 2:
                player.region = pygame.Rect(0, (self.screen.get_height()//4), (self.screen.get_width()//4), (self.screen.get_height()//4) * 2)
        self.player_index = 0
        self.current_player = self.players[self.player_index]
        self.buttons = [Button(None, (self.screen.get_width()//2, self.screen.get_height()//3), "DEAL", pygame.font.Font("images/menu/font.ttf", 30), "white", "yellow")]
        self.labels = []
        self.objects = [self.deck] + self.buttons + self.players + self.labels

    def showLabel(self, label):
        self.labels.append(label)
        self.update()
        self.draw()
        pygame.time.wait(1000)
        self.labels.pop()
        self.update()
        self.draw()


    def deal_cards(self):
        game_buttons = [Button(None, ((self.screen.get_width()//8) * 7, (self.screen.get_height()//9) * 2), "DRAW CARD", pygame.font.Font("images/menu/font.ttf", 17), "white", "yellow"),
                        Button(None, ((self.screen.get_width()//8) * 7, (self.screen.get_height()//9) * 3), "PICK CARD", pygame.font.Font("images/menu/font.ttf", 17), "white", "yellow"),
                        Button(None, ((self.screen.get_width()//8) * 7, (self.screen.get_height()//9) * 4), "DISCARD", pygame.font.Font("images/menu/font.ttf", 17), "red", "red"),
                        Button(None, ((self.screen.get_width()//8) * 7, (self.screen.get_height()//9) * 5), "PLAY FOR ME", pygame.font.Font("images/menu/font.ttf", 17), "white", "yellow"),
                        Button(None, ((self.screen.get_width()//8) * 7, (self.screen.get_height()//9) * 6), "END TURN", pygame.font.Font("images/menu/font.ttf", 17), "white", "yellow")]
        
        player_labels = [Label((self.screen.get_width()//2, self.screen.get_height() - 17), "PLAYER 1", pygame.font.Font("images/menu/font.ttf", 17), "white"),
                         Label((self.screen.get_width()//2, 17), "PLAYER 2", pygame.font.Font("images/menu/font.ttf", 17), "white"), 
                         Label((51, self.screen.get_height()//2), "PLAYER 3", pygame.font.Font("images/menu/font.ttf", 17), "white", -90)]
        
        self.deck.deal_cards(self.players)
        self.buttons = game_buttons
        self.labels = player_labels if len(self.players) == 3 else player_labels[:2]
        self.update()
        self.draw()

    def select_player(self):
        self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "PICK PLAYER", pygame.font.Font("images/menu/font.ttf", 17), "white"))
        non_current_players = [player for player in self.players if player != self.current_player]
        for player in non_current_players:
            print(player.name)
        any_selected = False
        while not any_selected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for player in non_current_players:
                        if player.region.collidepoint(event.pos):
                                return player

    def next_player(self):
        self.player_index = (self.player_index + 1) % len(self.players)
        self.current_player = self.players[self.player_index]
        for button in self.buttons:
            if button.text_input == "DISCARD":
                button.base_colour = "red"
                button.hovering_colour = "red"
            else:
                button.base_colour = "white"
                button.hovering_colour = "yellow"

    def main_game_events(self):
        # DISCARD turns white only when discard group available
        for button in self.buttons:
            if button.text_input == "DISCARD":
                if self.current_player.hand.find_valid_group():
                    button.base_colour = "white"
                    button.hovering_colour = "yellow"
                else:
                    button.base_colour = "red"
                    button.hovering_colour = "red"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:

                    if button.text_input == "DEAL" and button.IfButtonClicked(event.pos):
                        self.deal_cards()                         

                    if button.text_input == "DRAW CARD" and button.IfButtonClicked(event.pos):
                        if self.current_player.drawn_cards < 3:
                            self.current_player.draw_card(self.deck)
                            if self.current_player.drawn_cards == 3:
                                button.base_colour = "red"
                                button.hovering_colour = "red"
                            self.draw()
                        else:
                            self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "YOU HAVE ALREADY DRAWN 3 CARDS", pygame.font.Font("images/menu/font.ttf", 17), "white"))

                    if button.text_input == "PICK CARD" and button.IfButtonClicked(event.pos):
                        if self.current_player.picked_cards < 1:
                            button.base_colour = "yellow"
                            self.current_player.pick_card(self.select_player())
                            button.base_colour = "red"
                            button.hovering_colour = "red"
                                                
                        else:
                            self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "YOU HAVE ALREADY PICKED A CARD", pygame.font.Font("images/menu/font.ttf", 17), "white"))
                            
                    if button.text_input == "DISCARD" and button.IfButtonClicked(event.pos):
                        if len(self.current_player.discard_list) >= 3:
                            if not self.current_player.discard_group(self.deck):
                                self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "NOT A VALID GROUP", pygame.font.Font("images/menu/font.ttf", 17), "white"))
                        else:
                            self.showLabel(Label((self.screen.get_width()//2, self.screen.get_height()//3), "YOU NEED AT LEAST 3 CARDS", pygame.font.Font("images/menu/font.ttf", 17), "white"))
                    
                    if button.text_input == "END TURN" and button.IfButtonClicked(event.pos):
                        self.current_player.end_turn()
                        self.next_player()
                        print(self.player_index)

                if self.current_player.hand:
                    for card in self.current_player.hand.collection:
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
        self.screen.fill("#123542")
        for obj in self.objects:
            if type(obj) == Button:
                obj.changeColour(pygame.mouse.get_pos())
            obj.update(self.screen)
        pygame.display.flip()                

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.main_game_events()
            self.draw()
            
            

 



