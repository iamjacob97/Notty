#Game starts here

import pygame
import sys
from GameStateManager import GameStateManager
from Menu import Menu # Import the Menu class to manage the main menu of the game.

pygame.init() # Initialise the pygame module.


clock = pygame.time.Clock()# Set up the clock to control the frame rate.
dimensions = WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 # Define the window dimensions and create the display.
screen = pygame.display.set_mode(dimensions)
caption = "NOTTY - a card game" # Set the window title.
pygame.display.set_caption(caption)
manager = GameStateManager() # Initialize the GameStateManager to manage game states.
manager.change_state(Menu(screen, clock, manager)) # Set the initial state to the Menu screen.

while manager.current_state: # Main game loop - runs as long as there is a current state.
    clock.tick(60) # Limit the game to 60 frames per second.
    for event in pygame.event.get(): # Handle events (e.g., quit event).
        if event.type == pygame.QUIT: # If the user closes the window.
            manager.current_state = None # Exit the game loop.
    
    manager.current_state.run() # Run the current state logic. 
    
# Cleanup after the game loop ends.
pygame.quit() # Uninitialize all pygame modules.
sys.exit() # Safely exit the program.









    
            