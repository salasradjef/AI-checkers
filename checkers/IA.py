from copy import deepcopy
from .constants import *


#Implementation de alphabeta

def alphabeta(position,depth,max_player,game,alpha,beta,level):
   #Condition d'arrêt de la récursivité (si on trouve un etat ou l'IA gagne il ne sert a rien de continuer de parcourir l'arbre
    if level == 1 :
        if depth == 0 or position.winner() != None:
            return position.evaluate(),position
    elif level == 2 :
        if depth == 0 or position.winner() != None:
            return position.evaluate_v2(),position
    

    #max_player permet de savoir si il doit maximiser le score(pour l'IA) ou minimiser le score (pour l'adversaire)
    if max_player:
        #noeud de type Max
        maxEval = float('-inf')
        best_move = None 
        #Pour chaque coup possible des Noires (IA) lancer un minimax
        for move in get_all_moves(position,BLACK,game): 
            evaluation = alphabeta(position,depth-1,False,game,alpha,beta,level)[0]
            maxEval = max(evaluation,maxEval)
            if maxEval == evaluation:
                best_move = move

            #coupure beta
            if beta >= maxEval:
                return maxEval,best_move

            alpha = max(alpha,evaluation)
            
            #alpha est toujours inférieure à Beta
            if beta <= alpha:
                break
            
        
        return maxEval , best_move 

    else:

        #noeud de type Min
        minEval = float('inf')
        best_move = None
        #Pour chaque coup possible des Blancs (Humain) lancer un minimax
        for move in get_all_moves(position,WHITE,game):
            evaluation = alphabeta(move,depth-1,True,game,alpha,beta,level)[0]
            minEval = min(evaluation,minEval)
            if minEval == evaluation:
                best_move = move


            #coupure alpha
            if alpha >= minEval:
                return minEval,best_move
                
            beta = min(beta,evaluation)



            #alpha est toujours inférieure à Beta
            if beta <= alpha:
                break

        return minEval,best_move





#Implementation de l'algorithme minimax
def minimax(position, depth, max_player, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    

    #max_player permet de savoir si il doit maximiser le score(pour l'IA) ou minimiser le score (pour l'adversaire)
    if max_player:
        maxEval = float('-inf')
        best_move = None
        #Pour chaque coup possible des Noires  lancer un minimax
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        #Pour chaque coup possible des Blancs lancer un minimax
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move



#Simuler un déplacement 
def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board




#Récuperer la liste de tous les mouvement possibles sur le damier pour un joueur 
def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)

        keys = []
        for move, skip in valid_moves.items():
            if len(skip) != game.max_skipped :
                keys.append(move)
        for m in keys:
            valid_moves.pop(m)

        for move, skip in valid_moves.items():
            
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves




