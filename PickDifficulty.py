import pygame
import sys
from GameSetup import GameSetup
from Button import Button
from MainGame import MainGame

class PickDifficulty(GameSetup):
    def __init__(self, screen, clock, manager):
        super().__init__(screen, clock, manager)
        # self.background_image = pygame.image.load("images/menu/background.png")

        # self.background_audio = pygame.mixer.Sound("audio/background.wav")

        # Playing the background audio
        # self.play_background_music(volume=0.2)
    
        self.objects = [
            Button(
            image=None,
            pos=(self.screen.get_width() // 2, 200), # Position of the button
            text_input="EASY", # Text displayed on the button
            font=pygame.font.Font("images/menu/font.ttf", 75), # Font of the text
            base_colour="White", # Base colour of the button
            hovering_colour="Yellow", # colour of the button when hovered over
            ),

            Button(
            image=None,
            pos=(self.screen.get_width() // 2, 400),
            text_input="MEDIUM",
            font=pygame.font.Font("images/menu/font.ttf", 75),
            base_colour="White",
            hovering_colour="Yellow"),

            Button(
            image=None,
            pos=(self.screen.get_width() // 2, 600),
            text_input="HARD",
            font=pygame.font.Font("images/menu/font.ttf", 75),
            base_colour="White",
            hovering_colour="Yellow")]
        

    def pick_difficulty_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #checks if mouse is pressed and gets the position of the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the PLAY button is clicked
                if self.objects[0].IfButtonClicked(event.pos):
                    self.manager.shared_data["difficulty"] = "easy"
                    self.manager.change_state(MainGame(self.screen, self.clock, self.manager))
                    self.running = False

                elif self.objects[1].IfButtonClicked(event.pos):
                    self.manager.shared_data["difficulty"] = "medium"
                    self.manager.change_state(MainGame(self.screen, self.clock, self.manager))
                    self.running = False

                elif self.objects[2].IfButtonClicked(event.pos):
                    self.manager.shared_data["difficulty"] = "hard"
                    self.manager.change_state(MainGame(self.screen, self.clock, self.manager))
                    self.running = False
        
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.pick_difficulty_events()
            self.draw()

