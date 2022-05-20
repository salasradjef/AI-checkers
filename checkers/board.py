from numpy import False_
import pygame
from .constants import BLACK, ROWS, BEIGE, BROWN, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []     # Initialise la liste qui va simuler le plateau
        self.black_left = self.white_left = 20      # Initialise le nombre de pions de départ
        self.black_kings = self.white_kings = 0     # Initialise le nombre de dames de départ
        self.create_board()     # Appelle la fonction qui crée le plateau


    # Crée le plateau et y ajoute les pieces de départ
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])   # Ajoute les lignes à la liste du plateau

            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):     # Permet de n'ajouter des pieces qu'aux cases marrons

                    if row < 4:
                        self.board[row].append(Piece(row, col, BLACK))  # Ajoute les pieces noires du coté haut

                    elif row > 5:
                        self.board[row].append(Piece(row, col, WHITE))  # Ajoute les pieces blanches du coté bas

                # N'ajoute rien dans le reste des cas
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)


    # Dessine les cases du plateau
    def draw_squares(self, win):
        win.fill(BROWN)     # Couleur arrière plan

        # Crée des carrés beiges espacés régulièrement pour donner l'impression d'un damier
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BEIGE, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    # Déplace la piece passée en paramètres vers les nouvelles coordonnées
    def move(self, piece, row, col):
        # Deplace la piece vers ses nouvelles coordonnées dans le tableau simulant le plateau 
        # en echangeant les elements aux coordonnées de la pieces et aux nouvelles coordonnées
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        # Enregistre les nouvelles coordonnées de la piece
        piece.move(row, col)

        # Transforme la piece en dame si elle arrive a la derniere ligne à l'opposée de son coté de départ
        if piece.color == WHITE and row == 0:
            piece.make_king()
            self.white_kings += 1
        elif piece.color == BLACK and row == ROWS - 1:
            piece.make_king()
            self.black_kings += 1 


    # Retourne la piece se trouvant aux coordonnées passées en paramètres
    def get_piece(self, row, col):
        return self.board[row][col]

        
    # Appelle les fonctions nécessaires pour dessiner le plateau et les pieces
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)


    # Supprime du plateau la piece passée en paramètres si elle existe
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1
    

    # Retourne le vainqueur si il existe
    # Le vainqueur est l'adversaire du joueur n'ayant plus de pieces
    def winner(self):
        if self.black_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK
        return None 
    

    # Retourne les mouvements possibles pour la piece passées en paramètres
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
            moves.update(self._traverse_left_back(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right_back(row +1, min(row+3, ROWS), 1, piece.color, right))
        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
            moves.update(self._traverse_left_back(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right_back(row -1, max(row-3, -1), -1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[], king = False):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    
                    row = max(r-3, 0)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))

                
                    row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                    

                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[], king = False):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    
                    row = max(r-3, 0)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                    
                    row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                        
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves


    def _traverse_left_back(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif r == start:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                        moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                        moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                        moves.update(self._traverse_left_back(r-step, row, -step, color, left-1,skipped=last))
                        moves.update(self._traverse_right_back(r-step, row, -step, color, left+1,skipped=last))
                    else:
                        row = min(r+3, ROWS)
                        moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                        moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                        moves.update(self._traverse_left_back(r-step, row, -step, color, left-1,skipped=last))
                        moves.update(self._traverse_right_back(r-step, row, -step, color, left+1,skipped=last))
                    

                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right_back(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif r == start:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                        moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                        moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                        moves.update(self._traverse_left_back(r-step, row, -step, color, right-1,skipped=last))
                        moves.update(self._traverse_right_back(r-step, row, -step, color, right+1,skipped=last))
                    else:
                        row = min(r+3, ROWS)
                        moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                        moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                        moves.update(self._traverse_left_back(r-step, row, -step, color, right-1,skipped=last))
                        moves.update(self._traverse_right_back(r-step, row, -step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves



    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces



    #Heuristique 01
    def evaluate(self):
        return self.black_left - self.white_left + (self.black_kings * 0.5 - self.white_left * 0.5)
        #return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    #Heuristique 02
    def evaluate_v2(self):
        score_black = 0
        score_white = 0
        for row in self.board:
            for piece in row:
                if piece != 0:
                    tmp = piece.row + self.board.index(row)
                    if piece.king == True:
                        tmp = tmp * 2
                    if piece.color == BLACK:
                        score_black = score_black + tmp
                    elif piece.color == WHITE:
                        score_white = score_white + tmp
                    
                


        return score_black - score_white 
        

    
