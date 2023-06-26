"""Width and height of displayed screen"""
from enum import Enum
import pygame

class SizeConstants:
    """Namespace class for constants containing sizes for scalability"""
    # pylint: disable=too-few-public-methods
    WIDTH, HEIGHT = 640, 640
    ROWS, COLS = 8, 8
    CELL_SIZE = WIDTH//ROWS
    STONE_SIZE = int(CELL_SIZE * 0.8)
    STONE_OFFSET = (CELL_SIZE-STONE_SIZE)//2
    CIRCLE_RADIUS = int(CELL_SIZE * 0.2)

pygame.font.init()
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

class Menu:
    "Namespace class for Menu assets"
    # pylint: disable=too-few-public-methods
    TITLE_FONT = pygame.font.Font("app/assets/PressStart2P-Regular.ttf", 65)
    MENU_FONT = pygame.font.Font(None, 50)
    BACKGROUND = pygame.transform.scale(
        pygame.image.load('app/assets/Background.png'), (SizeConstants.WIDTH, SizeConstants.HEIGHT))

class Colors:
    "Namespace class for colors"
    # pylint: disable=too-few-public-methods
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BROWN = (78, 53, 36)
    BLUE = (100, 149, 237)
    YELLOW = (187,203,43)
    GRAY = (128, 128, 128)

class StoneEnum(Enum):
    "Enum class to indicate pieces"
    WHITE = 1
    BLACK = 2
    WHITE_KING = 3
    BLACK_KING = 4

class StoneImages:
    "Namespace class for stone images"
    # pylint: disable=too-few-public-methods
    size = SizeConstants.STONE_SIZE
    WHITE_STONE = pygame.transform.scale(
        pygame.image.load('app/assets/Stone_White.png'), (size, size))
    WHITE_KING = pygame.transform.scale(
        pygame.image.load('app/assets/Stone_White_2.png'), (size, size))

    BLACK_STONE = pygame.transform.scale(
        pygame.image.load('app/assets/Stone_Black.png'), (size, size))
    BLACK_KING = pygame.transform.scale(
        pygame.image.load('app/assets/Stone_Black_2.png'), (size, size))

class AIConstants:
    # pylint: disable=too-few-public-methods
    "Namespace class for AI constants"
    DEPTH = 6
    SEED = 25
    