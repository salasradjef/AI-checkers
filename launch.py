import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from checkers.IA import alphabeta, minimax
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE,WHITE,BLACK
from checkers.game import Game
FPS = 60


def choose_difficulty():
    accepted = False
    while(accepted != True):
        print("1)- Facile")
        print("2)- Moyen")
        print("3)- Difficile")
        rslt = input("")
        if(int(rslt) == 1):
            accepted = True
            print("Vous avez choisi le niveau Facile !")
            return 1
        elif(int(rslt) == 2):
            accepted = True
            print("Vous avez choisi le niveau Moyen !")
            return 2
        elif(int(rslt) == 3):
            accepted = True
            print("Vous avez choisi le niveau Difficile !")
            return 3
        else:
            print("Choisir l'option 1 , 2 ou 3 \n")



def human_vs_human():
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers Human')
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        if game.winner() != None:
            print(game.winner())
            run = False
            print("Felitication aux" + str(game.turn))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    pygame.quit()

def human_vs_IA(difficulty):
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers IA')
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == BLACK:
            INFINI_MINUS = float('-inf')
            INFINI = float('inf')
            if difficulty == 1:
                value, new_board =minimax(game.get_board(),1,BLACK, game)
                game.ai_move(new_board)
            elif difficulty == 2 :
                value,new_board = alphabeta(game.get_board(),3,BLACK,game,alpha=INFINI_MINUS,beta=INFINI,level=1)
                game.ai_move(new_board)
            elif difficulty == 3 :
                value,new_board = alphabeta(game.get_board(),5,BLACK,game,alpha=INFINI_MINUS,beta=INFINI,level=2)
                game.ai_move(new_board)
           

        if game.winner() != None:
            
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    pygame.quit()

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def menu():
    accepted = False


    print("-----Bonjour-----")
    print("Souhaitez-vous jouer :")

    while(accepted != True):
        
        print("1)- Humain vs IA")
        print("2)- Humain vs Humain")

        reponse = input("")

        if(int(reponse) == 1):
            accepted = True
            rslt = choose_difficulty()
            human_vs_IA(rslt)
            
        elif (int(reponse) == 2):
            accepted = True
            human_vs_human()

        else:

            print("Choisir l'option 1 ou 2 \n")

menu()