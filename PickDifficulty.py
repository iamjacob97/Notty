import pygame
import sys
from os.path import join
from GameSetup import GameSetup
from Button import Button
from MainGame import MainGame

class PickDifficulty(GameSetup):
    def __init__(self, screen, clock, manager):
        super().__init__(screen, clock, manager)
        self.background_image = pygame.image.load(join("images", "backgrounds", "difficulty.png"))
        font_style = pygame.font.Font(join("images", "backgrounds", "font.ttf"), 57)
        self.objects = [
            Button("easy",
            pos=(self.screen.get_width() // 2, 200), # Position of the button
            text_input="EASY", # Text displayed on the button
            font=font_style, # Font of the text
            base_colour="White", # Base colour of the button
            hovering_colour="Yellow", # colour of the button when hovered over
            ),

            Button("medium",
            pos=(self.screen.get_width() // 2, 400),
            text_input="MEDIUM",
            font=font_style,
            base_colour="White",
            hovering_colour="Yellow"),

            Button("hard",
            pos=(self.screen.get_width() // 2, 600),
            text_input="HARD",
            font=font_style,
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

