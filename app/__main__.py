"""Module for basic game graphics"""
import pygame
from game.checkers import Checkers
from game.config import SizeConstants as const
from game.config import StoneEnum
from game.ai import AI

def main_ai():
    """Main game loop function"""
    pygame.init()
    pygame.display.set_caption('Checkers')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((const.WIDTH, const.WIDTH))
    checkers = Checkers(screen)
    running = True
    ai_black = AI(StoneEnum.BLACK.value)
    ai_white = AI(StoneEnum.WHITE.value)
    checkers.update_screen()
    while running:
        clock.tick(40)
        if checkers.on_turn(ai_white.color):
            move = ai_white.get_best_move(checkers.get_board())
            print(move)
            # print('WHITE')
            checkers.ai_move(move)
            checkers.update_screen()
        if checkers.on_turn(ai_black.color) and not checkers.check_winner(False):
            move = ai_black.get_random_move(checkers.get_board())
            print(move)
            # print('BLACK')
            checkers.ai_move(move)
            checkers.update_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                checkers.process_input(pos)
                checkers.update_screen()
        # checkers.update_screen()
        if checkers.check_winner():
            running = False


def main():
    """Main game loop function"""
    pygame.init()
    pygame.display.set_caption('Checkers')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((const.WIDTH, const.WIDTH))
    checkers = Checkers(screen)
    running = True
    ai_black = AI(StoneEnum.BLACK.value)
    ai_white = AI(StoneEnum.WHITE.value)
    checkers.update_screen()
    while running:
        clock.tick(40)
        # if checkers.on_turn(ai_white.color):
        #     move = ai_white.get_best_move(checkers.get_board())
        #     print(move)
        #     # print('WHITE')
        #     checkers.ai_move(move)
        #     checkers.update_screen()
        if checkers.on_turn(ai_black.color) and not checkers.check_winner(False):
            move = ai_black.get_best_move(checkers.get_board())
            print(move)
            # print('BLACK')
            checkers.ai_move(move)
            checkers.update_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                checkers.process_input(pos)
                checkers.update_screen()
        # checkers.update_screen()
        if checkers.check_winner():
            running = False

if __name__ == "__main__":
    main_ai()
