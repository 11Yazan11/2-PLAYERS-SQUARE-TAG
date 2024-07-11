import pygame
import numpy as np
import random
import time
import sys
import os
from matrix import *



np.set_printoptions(threshold=sys.maxsize)

from grid import *
from camera import *


pygame.init()


class Game:
    def __init__(self, draw):

        self.wnx = 900
        self.wny = 600

        self.s1x = 651
        self.s1y = 434 

        self.s2x = 651
        self.s2y = 434 

        
        self.surf1 = pygame.surface.Surface((self.s1x, self.s1y))
        self.surf2 = pygame.surface.Surface((self.s2x, self.s2y))


        
        if draw == False:
            self.screen = pygame.display.set_mode((1300, self.s1y))
            self.window = self.surf1
            self.window2 = self.surf2
        else:
            self.screen = pygame.display.set_mode((self.wnx, self.wny))

        
        self.fps = 120
        self.clock = pygame.time.Clock()
        self.draw = draw

        self.runner_img = pygame.transform.scale(pygame.image.load('runner_face.jpg').convert_alpha(), (100, 100))
        self.runner_img.set_alpha(170)
        self.tager_img = pygame.transform.scale(pygame.image.load('tager_face.jpg').convert_alpha(), (100, 100))
        self.tager_img.set_alpha(170)

    def updater(self):
        if not self.draw:
            self.screen.blit(self.window, (0, 0))
            pygame.draw.rect(self.screen, "red",(self.s1x-2, 0, 4, self.s1x))
            self.screen.blit(self.window2, (self.s1x, 0))
            self.window.fill((100, 20, 40))
            self.window2.fill((40, 20, 100))
            self.clock.tick(self.fps)

        else:
            self.screen.fill((100, 20, 40))

            

              
        
            



def main():
    draw = input("DRAW MODE ? [answer : True/False] [else will stop program]")
    if draw == "True":
         draw = True
    elif draw == "False":
         draw = False
    else:
        return #stop main()
    run = True
    game = Game(draw)
    if draw:
        grid = Grid(game.screen, game.wnx, game.wny, draw)
    else:
        grid1 = Grid(game.window, game.s1x, game.s1y, draw)
        grid2 = Grid2(game.window2, game.s2x, game.s2y, draw)

    matrix_changes = np.array(matrix).reshape(180, int(180/1.5), 3) 

    player1_tagged_someone = False
    player2_tagged_someone = False  

    player1_is_tager = None
    player2_is_tager = None

    player_1_score = 0
    player_2_score = 0

    score_factor = 10

    font = pygame.font.Font(size=25)
    tagger_txt = font.render("TAGGER", True, (255, 255, 0))
    runner_txt = font.render("RUNNER", True, (0, 255, 255))

    tagger_txt.set_alpha(150)
    runner_txt.set_alpha(150)
  

    
    while run: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        game.updater() 

        if not draw:
            if player1_is_tager:
                game.window.fill((100, 20, 40))
                game.window2.fill((40, 20, 100))
            if player2_is_tager:
                game.window2.fill((100, 20, 40))
                game.window.fill((40, 20, 100))    

            matrix_changes, player1_is_tager, player1_got_taged = grid1.updater(matrix_changes, player1_tagged_someone)
            matrix_changes, player2_is_tager, player2_got_taged = grid2.updater(matrix_changes, player2_tagged_someone)

            player1_tagged_someone = False
            player2_tagged_someone = False

            if player1_is_tager:
                game.window.blit(game.tager_img, (10, 10))
                game.window.blit(tagger_txt, (20, 140))
                game.window2.blit(game.runner_img, (10, 10))
                game.window2.blit(runner_txt, (10, 140))
                

            if player2_is_tager:

                game.window.blit(game.runner_img, (10, 10))
                game.window.blit(runner_txt, (20, 140))
                game.window2.blit(game.tager_img, (10, 10))
                game.window2.blit(tagger_txt, (10, 140))


            score_factor -= 0.005

            if player1_got_taged:
                player_2_score += int(score_factor*10)/10
                score_factor = 10
                player2_tagged_someone = True 
            if player2_got_taged:
                player_1_score += int(score_factor*10)/10 
                score_factor = 10
                player1_tagged_someone = True


            pygame.display.set_caption(f" | [SQUARE TAG] | [YOU SHOULD SEARCH UP 'GORILLA TAG VR' ON GOOGLE...].  |              PLAYER-1 SCORE = {player_1_score}  VS   PLAYER-2 SCORE = {player_2_score}            |  GAINS WHEN TAGGING ARE DECREASING : {int(score_factor*10)/10} points left !")
    
        else:
            matrix_changes, _, _ = grid.updater(matrix_changes, None)
            
        pygame.display.flip()
        


    pygame.quit() 

    if draw:
        os.system('clear')
        print(np.array2string(grid.matrix, separator=', '))


       
    


if __name__ == "__main__":
    main()

            
        


