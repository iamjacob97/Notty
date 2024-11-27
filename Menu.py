import pygame
import sys
from GameSetup import GameSetup
from GameStateManager import GameStateManager
from Button import Button
from PickPlayer import PickPlayer


class Menu(GameSetup):
    def __init__(self, screen, clock, manager):
        super().__init__(screen, clock, manager)
        self.background_image = pygame.image.load("images/menu/background.png")

        #Loadin audio files for the menu
        self.background_audio = pygame.mixer.Sound("audio/background.wav")

        # # Playing the background audio
        self.play_background_music(volume=0.2)

        # Creating buttons using the Button class and storing them in a list
        self.objects = [
            Button(
            image=None,
            pos=(self.screen.get_width() // 2, 200), # Position of the button
            text_input="PLAY", # Text displayed on the button
            font=pygame.font.Font("images/menu/font.ttf", 75), # Font of the text
            base_color="White", # Base color of the button
            hovering_color="Yellow", # Color of the button when hovered over
            ),

            Button(
            image=None,
            pos=(self.screen.get_width() // 2, 350),
            text_input="OPTIONS",
            font=pygame.font.Font("images/menu/font.ttf", 75),
            base_color="White",
            hovering_color="Yellow"),

            Button(
            image=None,
            pos=(self.screen.get_width() // 2, 500),
            text_input="INSTUCTIONS",
            font=pygame.font.Font("images/menu/font.ttf", 75),
            base_color="White",
            hovering_color="Yellow"),

            Button(
            image=None,
            pos=(self.screen.get_width() // 2, 650),
            text_input="QUIT",
            font=pygame.font.Font("images/menu/font.ttf", 75),
            base_color="White",
            hovering_color="Yellow")
        ]

    def show_options(self):
        # Display the options screen
        show_options_screen = True
        while show_options_screen:
            self.screen.fill("black")
            font = pygame.font.Font("images/menu/font.ttf", 25)
            options_text = font.render("This is the OPTIONS screen.", True, "White")
            self.screen.blit(options_text,
(self.screen.get_width() // 2 - options_text.get_width() // 2, 300),
            )

            back_button = Button(
                image=None,
                pos=(self.screen.get_width() // 2, 500),
                text_input="BACK",
                font=pygame.font.Font("images/menu/font.ttf", 75),
                base_color="White",
                hovering_color="Yellow",
            )
            back_button.changeColor(pygame.mouse.get_pos())
            back_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.IfButtonClicked(pygame.mouse.get_pos()):
                        show_options_screen = False

            pygame.display.flip() # Update the display



    def show_instructions(self):
        # Read instructions from file
        with open("instructions.txt", 'r') as file:
            instructions = file.readlines()

        # Display black screen and load font
        show_instructions_screen = True
        while show_instructions_screen:
            self.screen.fill("black")
            font = pygame.font.Font("images/menu/font.ttf", 25)

            # Loop through each line in the instructions list with an index
            for i, line in enumerate(instructions):
                # Render the text using the specified font removing any leading/trailing whitespace and setting the color to white
                instructions_text = font.render(line.strip(), True, "White")

                # Display the text using the blit method
                self.screen.blit(
                    instructions_text,
                    (self.screen.get_width() // 2 - instructions_text.get_width() // 2, 100 + i * 50))
            

            # Creating a back button
            back_button = Button(
                image=None,
                pos=(self.screen.get_width() // 2, self.screen.get_height() - 100),
                text_input="BACK",
                font=pygame.font.Font("images/menu/font.ttf", 50),
                base_color="White",
                hovering_color="Yellow",
            )

            # Update button visuals
            back_button.changeColor(pygame.mouse.get_pos())
            back_button.update(self.screen)

            # menu events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.IfButtonClicked(pygame.mouse.get_pos()):
                        show_instructions_screen = False

            pygame.display.flip() # Update the display


    # adding logic to buttons in the menu
    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #checks if mouse is pressed and gets the position of the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # If the PLAY button is clicked
                if self.objects[0].IfButtonClicked(mouse_pos): # PLAY Button which is at index 0
                    self.stop_background_music() # Stop the background music
                    self.manager.change_state(PickPlayer(self.screen, self.clock, self.manager))
                    self.running = False # Exit the menu loop

                # If the OPTIONS button is clicked
                elif self.objects[1].IfButtonClicked(mouse_pos): # OPTIONS Button
                    #play audio
                    self.show_options()

                # If the INSTRUCTIONS button is clicked
                elif self.objects[2].IfButtonClicked(mouse_pos): # INSTRUCTIONS Button
                    self.show_instructions()

                # If the QUIT button is clicked
                elif self.objects[3].IfButtonClicked(mouse_pos):  # QUIT Button
                    pygame.quit()
                    sys.exit()


    def run(self):
        while self.running:
            self.clock.tick(60)
            self.menu_events()
            self.draw()
