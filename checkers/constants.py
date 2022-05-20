import pygame


WIDTH, HEIGHT = 700, 700    # Taille plateau
ROWS, COLS = 10, 10         # Nombre cases lignes et colones plateau
SQUARE_SIZE = WIDTH//COLS   # Taille cases

# Couleurs cases
BEIGE = (200,173,127)
BROWN = (63,34,4)

# Couleurs pions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BLUE = (0, 0, 255)          # Couleur indicateur mouvements possibles
GREY = (128,128,128)        # Couleur contours pions

# Image représentant la dame
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (22, 13))
