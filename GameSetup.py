import pygame

class GameSetup:
    def __init__(self, screen, clock, manager):
        self.screen = screen
        self.clock = clock
        self.manager = manager

        # Setting the running variable to True
        self.running = True

        # Loading background image
        self.background_image = None
        # self.icon = 

        #Loadin audio files for the menu
        self.background_audio = None

        # # Playing the background audio
        # self.play_background_music(volume=0.2)

        # Creating buttons using the Button class and storing them in a list
        self.objects = []

    # Function to create the setup screen
    def draw(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))  # Draw the background image
        else:
            self.screen.fill("black")
        for obj in self.objects: # Draw each button
            obj.changeColour(pygame.mouse.get_pos()) # Change the colour of each button in loop if hovered over
            obj.update(self.screen) # Update the button visuals
        pygame.display.flip() # Update the display showing new frame


    # Function to play the background music
    def play_background_music(self, volume=0.5):
        self.background_audio.set_volume(volume)
        self.background_audio.play(loops=-1)

    # Function to stop the background music
    def stop_background_music(self):
        self.background_audio.stop()

