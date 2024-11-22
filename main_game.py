# import pygame
# from pygame.locals import *
from CollectionOfCards import *
from Deck import *
from Player import *
from Game import *

# pygame.init()
# size = width, height = 1280, 720
# pygame.display.set_caption('Notty')
# running = True

# screen = pygame.display.set_mode(size)

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

# pygame.quit()

def play():
    num_players = 0
    while not num_players in {2,3}:
        try:
            num_players = int(input("Number of players?(2 or 3): "))
        except ValueError:
            print("Should be either 2 or 3")

    names = []
    for i in range(num_players):
        names.append(input(f"player{i + 1} name: "))

    game = Game(names)
    game.deal_cards()

    while True:
        game.view_cards()
        game.current_player.playing = True
        print(f"{game.current_player.name}'s turn")
        while game.current_player.playing:
            action = input("What do you want to do: ")
            if action == "d":
                if game.current_player.draw >= 3:
                    print("Already drawn three cards")
                else:
                    game.current_player.draw_card(game.deck)
                    game.view_cards()
            elif action == "p":
                if game.current_player.pick >= 1:
                    print("Already picked a card")
                else:
                    game.current_player.pick_card(game.players[int(input("Who do you want to pick from?: ")) - 1])
                    game.view_cards()
            else:
                game.current_player.end_turn()
                if game.current_player.is_winner():
                    print(f"{game.current_player.name} is the winner!")
                    return None
                game.next_player()
                break
        

play()