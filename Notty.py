import pygame
import sys
from GameStateManager import GameStateManager
from Menu import Menu
from PickPlayer import PickPlayer
from MainGame import *



pygame.init()

clock = pygame.time.Clock()
dimensions = WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode(dimensions)
caption = "NOTTY - a card game"
pygame.display.set_caption(caption)
manager = GameStateManager()
manager.change_state(Menu(screen, clock, manager))
pickplayer = PickPlayer(screen, clock, manager)


while manager.current_state:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    manager.current_state.run()   
    

pygame.quit()
sys.exit()











    
            