import pygame
import sys
from os.path import join
from Button import *
from GameSetup import GameSetup


class GameOver(GameSetup):
    def __init__(self, screen, clock, manager):
        super().__init__(screen, clock, manager)
        self.winner_name = self.manager.get_shared_data()["winner"]

        # Load background image
        self.background = pygame.image.load(join("images", "backgrounds", "gameover.png"))


        self.background_audio = pygame.mixer.Sound(join("audio", "background.wav"))
        self.congrats_audio = pygame.mixer.Sound(join("audio", "congrats.mp3"))

        #title for the font
        font_style = pygame.font.Font(join("images", "backgrounds", "font.ttf"), 35)
        button_font = pygame.font.Font(join("images", "backgrounds", "font.ttf"), 30)

        self.play_background_music(volume=0.05)

        # Label for winner
        self.congrats_audio.play()
        self.label_text = f"Congratulations {self.winner_name.upper()} Wins!"
        self.label = Label((self.screen.get_width() // 2, self.screen.get_height() // 3), 
                           self.label_text, font_style, "green")
        
   
        self.GameOverButtons = [
            Button(
            name ="New Game",
            pos=(self.screen.get_width() // 2, 350),  # Position of "New Game" button
            text_input="New Game",  # Text displayed on the button
            font=button_font,  # Font of the text
            base_colour="White",  # Base color of the button
            hovering_colour="Yellow",  # Color of the button when hovered over
            ),

            Button(
            name ="Quit", 
            pos=(self.screen.get_width() // 2, 500),  # Position of "Quit" button
            text_input="Quit",  # Text displayed on the button
            font=button_font,  # Font of the text
            base_colour="White",  # Base color of the button
            hovering_colour="Yellow",  # Color of the button when hovered over
            ),
        ]

    def draw(self): #puts everything on the screen
        self.screen.blit(self.background, (0, 0))  
        self.label.update(self.screen)  
        for button in self.GameOverButtons: 
            button.changeColour(pygame.mouse.get_pos())
            button.update(self.screen)
        pygame.display.flip() 

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                for button in self.GameOverButtons:
                    button.changeColour(pygame.mouse.get_pos())
                    if button.IfButtonClicked(event.pos):
                        if button.name == "New Game": #starts new game
                            self.stop_background_music() # Stop the background music
                            from PickPlayer import PickPlayer
                            self.manager.change_state(PickPlayer(self.screen, self.clock, self.manager))
                            self.running = False 
                        elif button.name == "Quit": # quits the game
                            pygame.quit()
                            sys.exit()

    def run(self):
        while self.running:
            self.clock.tick(60)  
            self.handle_events()  
            self.draw()  
