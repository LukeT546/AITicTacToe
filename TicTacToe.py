import sys
import pygame
import numpy as np
from Constants import *
import random
import copy


#setup
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption("Tic Tac Toe")
screen.fill(background_colour)


class Board:

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLUMNS) )
        self.empty_squares = self.squares 
        self.marked_squares = 0
    
    def final_state(self):
        #check rows
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
        
        #check columns
        for column in range(COLUMNS):
            if self.squares[0][column] == self.squares[1][column] == self.squares[2][column] != 0:
                return self.squares[0][column]

        #check diagonals
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]

        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            return self.squares[1][1]

        return 0
        
    def mark(self, row, column, player):
        self.squares[row][column] = player
        self.marked_squares += 1

    def empty_square(self, row, column):
        return self.squares[row][column] == 0
    
    def is_full(self):
        return self.marked_squares == ROWS * COLUMNS
    
    def isempty(self):
        return self.marked_squares == 0
    
    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.empty_square(row, column):
                    empty_squares.append( (row, column) )

        return empty_squares

class AI:

    def __init__(self, level = 1, player=2):
        self.level = level
        self.player = player

    def random_choice(self, board):
        empty_squares = board.get_empty_squares()
        index = random.randrange(0,len(empty_squares))

        return empty_squares[index]


    def minimax(self, board, maximising):

        case = board.get_final_state()

        if case == 1:
            return 1, None
    
        if case == 2:
            return -1, None
    
        elif board.is_full():
             return 0, None
    
        if maximising:
            max_eval = -1000
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row,col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark(row, col, self.player)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximising:
            min_eval = 1000
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row,col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            #random choice
            eval = "random"
            move = self.random_choice(main_board)
        else:
            #minimax
            eval, move = self.minimax(main_board, False)
        
        print(f"AI has chosen to mark the square {move} with evaluation {eval}")

        return move


class  Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  #player 1 is cross, player 2 is circle
        self.gamemode = "AI" #pvp or AI
        self.running = True
        self.show_lines()

    def show_lines(self):
        pygame.draw.line(screen, line_colour, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, line_colour, (WIDTH- SQUARE_SIZE, 0), (WIDTH-SQUARE_SIZE, HEIGHT), LINE_WIDTH)

        pygame.draw.line(screen, line_colour, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, line_colour, (0, HEIGHT - SQUARE_SIZE), (WIDTH, HEIGHT - SQUARE_SIZE), LINE_WIDTH)

    def next_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def draw_fig(self, row, col):
        if self.player == 1:
            #draw cross
            pygame.draw.line(screen, line_colour, (col * SQUARE_SIZE + radius, row * SQUARE_SIZE + SQUARE_SIZE - radius), (col * SQUARE_SIZE + SQUARE_SIZE - radius, row * SQUARE_SIZE + radius), circle_width)
            pygame.draw.line(screen, line_colour, (col * SQUARE_SIZE + radius, row * SQUARE_SIZE + radius), (col * SQUARE_SIZE + SQUARE_SIZE - radius, row * SQUARE_SIZE + SQUARE_SIZE - radius), circle_width)
        elif self.player == 2:
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, circle_colour, center, radius, circle_width)
            

def main():
    
    game = Game()
    board = game.board
    AI = game.ai

    #mainloop
    # while True:

    #     for event in pygame.event.get():

    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()

    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             pos = event.pos
    #             row = pos[1] // SQUARE_SIZE
    #             col = pos[0] // SQUARE_SIZE

    #             if board.empty_square(row,col): 
    #                 board.mark(row, col, game.player)
    #                 game.draw_fig(row, col)
    #                 game.next_player()

    #     if game.gamemode == "AI" and game.player == AI.player:
    #         #update the board
    #         pygame.display.update()

    #         #ai method
    #         row, col = AI.eval(board)

    #         board.mark(row, col, game.player)
    #         game.draw_fig(row, col)
    #         game.next_player()      
                
    #     pygame.display.update() 
        # mainloop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE

                if board.empty_square(row, col):
                    board.mark(row, col, game.player)
                    game.draw_fig(row, col)
                    game.next_player()

        if game.gamemode == "AI" and game.player == AI.player and not board.is_full():
            # update the board
            pygame.display.update()

            # ai method
            row, col = AI.eval(board)

            board.mark(row, col, game.player)
            game.draw_fig(row, col)
            game.next_player()

        pygame.display.update()

    

main()