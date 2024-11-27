import pygame
import sys
from Button import *


class MainGame:
    def __init__(self, screen, clock, manager):
        self.screen = screen
        self.clock = clock
        self.manager = manager
        self.running = True
        # self.background_image = pygame.image.load("images/menu/background.png")

        # if self.manager.get_shared_data()["numberofplayers"] == 2:
        #     self.players = [Player(), Player()]
        # elif 

    def main_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        print(self.manager.get_shared_data())

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.main_game_events()
            
            

 



