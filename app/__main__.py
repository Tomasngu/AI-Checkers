"""Module for basic game graphics"""
import sys
import pygame
# pylint: disable=maybe-no-member
from game.checkers import Checkers
from game.config import SizeConstants as const
from game.config import StoneEnum
from game.ai import AI
from game.config import Menu
from game.config import Colors


def ai_vs_ai(screen):
    """Main game loop function for AI"""
    clock = pygame.time.Clock()
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
        # checkers.update_screen()
        if checkers.check_winner():
            running = False


def play(screen, play_ai=False):
    """Main game loop function"""
    clock = pygame.time.Clock()
    checkers = Checkers(screen)
    running = True
    if play_ai:
        ai_black = AI(StoneEnum.BLACK.value)
    checkers.update_screen()
    while running:
        clock.tick(40)
        if play_ai and checkers.on_turn(ai_black.color) and not checkers.check_winner(False):
            move = ai_black.get_best_move(checkers.get_board())
            # print(move)
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


def menu_loop(screen, menu_items):
    """Menu shower"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, item in enumerate(menu_items):
                text_rect = Menu.MENU_FONT.render(item, True, Colors.WHITE)
                text_rect = text_rect.get_rect(
                    center=(const.WIDTH / 2, const.HEIGHT / 2 + i * 60))
                if text_rect.collidepoint(mouse_pos):
                    if i == 0:
                        play(screen)
                    elif i == 1:
                        play(screen, play_ai=True)
                    elif i == 2:
                        ai_vs_ai(screen)
                    elif i == 3:
                        pygame.quit()
                        sys.exit()
    screen.blit(Menu.BACKGROUND, (0, 0))

    for i, item in enumerate(menu_items):
        text = Menu.MENU_FONT.render(item, True, Colors.WHITE)
        text_rect = text.get_rect(
            center=(const.WIDTH / 2, const.HEIGHT / 2 + i * 60))
        button_rect = pygame.Rect(
            text_rect.left - 10, text_rect.top - 5, text_rect.width + 20, text_rect.height + 10)
        if item != 'Exit':
            pygame.draw.rect(screen, Colors.GRAY, button_rect)
        screen.blit(text, text_rect)

    title_text = Menu.TITLE_FONT.render("Checkers", True, Colors.WHITE)
    title_rect = title_text.get_rect(
        center=(const.WIDTH / 2, const.HEIGHT / 2 - 100))
    screen.blit(title_text, title_rect)

    pygame.display.update()


def main():
    """Main menu initialization"""
    pygame.init()
    pygame.display.set_caption('Checkers')
    screen = pygame.display.set_mode((const.WIDTH, const.WIDTH))

    menu_items = ["Player vs Player", "Player vs AI", "AI vs AI", "Exit"]

    while True:
        menu_loop(screen, menu_items)


if __name__ == "__main__":
    main()
