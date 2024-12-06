
import pygame
import sys
from os.path import join
from Button import Button
from GameSetup import GameSetup
from PickPlayer import PickPlayer

class Menu(GameSetup):
    def __init__(self, screen, clock, manager):
        super().__init__(screen, clock, manager)
        #Loading background image for menu
        self.background_image = pygame.image.load(join("images", "backgrounds", "startmenu.png"))

        #Loading audio files for the menu
        self.background_audio = pygame.mixer.Sound(join("audio", "background.wav"))

        # # Playing the background audio
        self.play_background_music(volume=0.05)
        # Loading font
        font_style = pygame.font.Font(join("images", "backgrounds", "font.ttf"), 57)
        # Creating buttons using the Button class and storing them in a list
        self.objects = [
            Button("play",
            pos=(self.screen.get_width() // 2, 200), # Position of the button
            text_input="PLAY", # Text displayed on the button
            font=font_style, # Font of the text
            base_colour="White", # Base colour of the button
            hovering_colour="Yellow", # colour of the button when hovered over
            ),

            Button("instructions",
            pos=(self.screen.get_width() // 2, 350),
            text_input="INSTUCTIONS",
            font=font_style,
            base_colour="White",
            hovering_colour="Yellow"),

            Button("quit",
            pos=(self.screen.get_width() // 2, 500),
            text_input="QUIT",
            font=font_style,
            base_colour="White",
            hovering_colour="Yellow")
        ]


    #Displays the instructions on the screen, ensuring text fits within the screen width.
    def show_instructions(self):
        # Read instructions from file
        instructions = self.load_instructions("instructions.txt")

        # Load background
        background = pygame.image.load(join("images", "backgrounds", "instructions.png"))
        font = pygame.font.Font(join("images", "backgrounds", "font.ttf"), 17)

        # Display instructions
        show_instructions_screen = True
        while show_instructions_screen:
            self.screen.blit(background, (0, 0))  # Draw background

            # # Render the instructions text on the screen, breaking lines that exceed the screen width.
            self.render_breaked_text(instructions, font, max_width=self.screen.get_width() - 40, start_y=100)

            # Create the back button
            back_button = Button(
                name="back",
                pos=(self.screen.get_width() // 2, self.screen.get_height() - 30),
                text_input="BACK",
                font=pygame.font.Font(join("images", "backgrounds", "font.ttf"), 21),
                base_colour="White",
                hovering_colour="Yellow",
            )

            # Update button visuals
            back_button.changeColour(pygame.mouse.get_pos())
            back_button.update(self.screen)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.IfButtonClicked(pygame.mouse.get_pos()):
                        show_instructions_screen = False
            pygame.display.flip() 

    def load_instructions(self, file_path):
    # Opens the specific file in read mode
        with open(file_path, 'r') as file:
    # Reads all the lines from the file and store them in the instructions variable
            instructions = file.readlines()
    # Return the list of lines (instructions) from the file
        return instructions


    def render_breaked_text(self, instructions, font, max_width, start_y):
        #vertical position for text rendering.
        y_offset = start_y
        # Define the vertical space between lines.
        line_height = 25  

        #looping through each line of instructions.
        for line in instructions:
        # Split the line into individual words.
            words = line.strip().split(' ')
        # Initialising the current line as an empty string.
            current_line = ""
        # loop through each word in the line.
            for word in words:
        # Add the word to the current line with a space.
                test_line = f"{current_line}{word} "
        # Check if the line width is within the max width.
                if font.size(test_line)[0] < max_width:
        # Update the current line if it fits.
                    current_line = test_line
                else:
        # Render the current line to the screen.
                    self.render_line(current_line, font, y_offset)
        # Move to the next line's vertical position.
                    y_offset += line_height
                    current_line = f"{word} "

            # places or renders the current line of text onto the screen.
            self.render_line(current_line, font, y_offset)
            # adjusts the vertical position down by the height of one line to prepare for the next line.
            y_offset += line_height

    # Create a surface for the line of text.
    def render_line(self, line, font, y_offset): 
        rendered_text = font.render(line.strip(), True, "White")
        # Draw the rendered text onto the screen.
        self.screen.blit(rendered_text, (20, y_offset))


    # adding logic to buttons in the menu
    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #checks if mouse is pressed and gets the position of the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the PLAY button is clicked
                if self.objects[0].IfButtonClicked(event.pos): # PLAY Button which is at index 0
                    self.stop_background_music() # Stop the background music
                    self.manager.change_state(PickPlayer(self.screen, self.clock, self.manager)) #respoonsible for changing game states
                    self.running = False # Exit the menu loop

                # If the INSTRUCTIONS button is clicked
                elif self.objects[1].IfButtonClicked(event.pos): # INSTRUCTIONS Button
                    self.show_instructions()

                # If the QUIT button is clicked
                elif self.objects[2].IfButtonClicked(event.pos):  # QUIT Button
                    pygame.quit()
                    sys.exit()


    def run(self):
        while self.running:
            self.clock.tick(60)
            self.menu_events()
            self.draw()