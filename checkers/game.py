import pygame
from .constants import BLACK, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    # Met à jour l'affichage dans la fenetre
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()


    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}
        self.max_skipped = self.get_max_skipped()


    # Appelle la fonction determinant le gagnant et retourne ce dernier
    def winner(self):
        return self.board.winner()


    # Relance une partie
    def reset(self):
        self._init()


    def get_max_skipped(self):
        maxi = 0
        for piece in self.board.get_all_pieces(self.turn):
            moves = self.board.get_valid_moves(piece)
            for move, skip in moves.items():
                if len(skip)>maxi:
                    maxi = len(skip)
        return maxi

    
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            keys = []
            for move, skip in self.valid_moves.items():
                if len(skip) != self.max_skipped :
                    keys.append(move)
            for m in keys:
                self.valid_moves.pop(m)

            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    #permet d'afficher les coups qu'une piece peut jouer
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    #permet de passer le tour d'un joueur a un autre
    def change_turn(self):
        self.valid_moves = {}

        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

        self.max_skipped = self.get_max_skipped()

    def get_board(self):
        return self.board
    

    def ai_move(self,board):
        self.board = board
        self.change_turn()