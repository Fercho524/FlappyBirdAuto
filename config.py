import pygame

# Dimensiones de la pantalla
SCREEN_SIZE = [SCREEN_WIDTH,SCREEN_HEIGHT] = [500,700]

# Colores
WHITE = (255, 255, 255)

# Game Constants
GRAVITY = 1
SPEED_INC = 1

# Fonts
FONT = pygame.font.SysFont("Press_Start_2P", 10)

# Screen and Window Config
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

CLOCK = pygame.time.Clock()

BIRD_WIDTH = 50
BIRD_HEIGHT = 30