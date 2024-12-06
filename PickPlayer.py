import pygame
import sys
from os.path import join
from Button import Button
from GameSetup import GameSetup
from PickDifficulty import PickDifficulty

class PickPlayer(GameSetup):
    def __init__(self, screen, clock, manager):
        super().__init__(screen, clock, manager)
        self.background_image = pygame.image.load(join("images","backgrounds", "chooseplayer.png"))
        # self.background_audio = pygame.mixer.Sound("audio/background.wav")
        # Playing the background audio
        # self.play_background_music(volume=0.2)
        font_style = pygame.font.Font(join("images", "backgrounds", "font.ttf"), 75)
        self.objects = [
            Button("2player",
            pos=(self.screen.get_width() // 2, 300), # Position of the button
            text_input="2 PLAYER", # Text displayed on the button
            font=font_style, # Font of the text
            base_colour="White", # Base colour of the button
            hovering_colour="Yellow", # colour of the button when hovered over
            ),

            Button("3player",
            pos=(self.screen.get_width() // 2, 500),
            text_input="3 PLAYER",
            font=font_style,
            base_colour="White",
            hovering_colour="Yellow")]

    def pick_player_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #checks if mouse is pressed and gets the position of the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
               # If the PLAY button is clicked
                if self.objects[0].IfButtonClicked(event.pos): 
                    self.manager.shared_data["numberofplayers"] = 2
                    self.manager.change_state(PickDifficulty(self.screen, self.clock, self.manager))
                    self.running = False
                    
                elif self.objects[1].IfButtonClicked(event.pos):
                    self.manager.shared_data["numberofplayers"] = 3
                    self.manager.change_state(PickDifficulty(self.screen, self.clock, self.manager))
                    self.running = False
        
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.pick_player_events()
            self.draw()

