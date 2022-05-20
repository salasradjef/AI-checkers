from .constants import BLACK, WHITE, SQUARE_SIZE, GREY, CROWN
import pygame

class Piece:
    PADDING = 15
    OUTLINE = 2

    # Initialise la piece dont les caractéristiques sont passées en paramètres
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()


    # Calcule les vraies coordonnées de la piece dans la fenetre
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2


    # Transforme la piece en dame
    def make_king(self):
        self.king = True
    

    # Dessine la piece aux coordonnées correspondantes
    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

        # Si la piece est une dame, ajoute l'image correcpondante au dessin
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))


    # Enregistre les nouvelles coordonnées de la piece
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()     # Appelle la fonction qui calcule les vraies coordonnées dans la fenetre


    #
    def __repr__(self):
        return str(self.color)