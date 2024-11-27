import pygame
import sys
from GameSetup import GameSetup
from GameStateManager import GameStateManager
from Button import Button
from PickDifficulty import PickDifficulty


class PickPlayer(GameSetup):
    def __init__(self, screen, clock, manager):
        super().__init__(screen, clock, manager)
        # self.background_image = pygame.image.load("images/menu/background.png")

        # self.background_audio = pygame.mixer.Sound("audio/background.wav")

        # Playing the background audio
        # self.play_background_music(volume=0.2)
    
        self.objects = [
            Button(
            image=None,
            pos=(self.screen.get_width() // 2, 300), # Position of the button
            text_input="2 PLAYER", # Text displayed on the button
            font=pygame.font.Font("images/menu/font.ttf", 75), # Font of the text
            base_color="White", # Base color of the button
            hovering_color="Yellow", # Color of the button when hovered over
            ),

            Button(
            image=None,
            pos=(self.screen.get_width() // 2, 500),
            text_input="3 PLAYER",
            font=pygame.font.Font("images/menu/font.ttf", 75),
            base_color="White",
            hovering_color="Yellow")]

    def pick_player_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #checks if mouse is pressed and gets the position of the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # If the PLAY button is clicked
                if self.objects[0].IfButtonClicked(mouse_pos): 
                    self.manager.shared_data["numberofplayers"] = 2
                    self.manager.change_state(PickDifficulty(self.screen, self.clock, self.manager))
                    self.running = False
                    
                elif self.objects[1].IfButtonClicked(mouse_pos):
                    self.manager.shared_data["numberofplayers"] = 3
                    self.manager.change_state(PickDifficulty(self.screen, self.clock, self.manager))
                    self.running = False
        
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.pick_player_events()
            self.draw()

