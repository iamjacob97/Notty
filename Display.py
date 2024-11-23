import pygame
import sys

class Display:
    def __init__(self):
        # self.background = pygame.image.load("images\\")
        self.clock = pygame.time.Clock()
        self.running = True

        pygame.init()

        self.dimensions = width, height = 1280, 720
        self.screen = pygame.display.set_mode(self.dimensions)
        self.caption = "NOTTY - a card game"

        pygame.display.set_caption(self.caption)

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()

    
