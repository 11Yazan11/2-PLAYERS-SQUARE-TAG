import pygame
import numpy as np
import random
import time
import os
from matrix import *
from camera import *

class Grid:
    def __init__(self, window, wnx, wny, draw=True):
        self.wnx = wnx
        self.wny = wny
        self.sidex = 180
        self.sidey = int(self.sidex / 1.5)
        self.matrix = np.array(matrix)
        self.matrix = self.matrix.reshape(self.sidex, self.sidey, 3)
        self.colorer = [0, 0, 0]  # default color
        self.selector = 0
        self.size = 1
        self.window = window
        self.zoom_index = 2
        self.player_position = [3, 108]
        self.is_tager = True
        self.matrix[self.player_position[0], self.player_position[1]] = [255, 0, 0]
        self.draw = draw
        if self.draw:
            self.zoom_index = 0
        self.camera = Camera(self.window, self.wnx, self.wny, self.zoom_index, self.player_position, self.sidex, self.sidey)   
        self.camera_x_corr = 0
        self.camera_corr_speed = 31.36
        self.camera_y_corr = 0
        self.got_taged = False
        self.can_move = False


    def updater(self, grid, tagged_someone):
        self.got_taged = False
        if tagged_someone:
            self.is_tager = False
        self.matrix = grid
        if self.draw:
            self.drawer()
        else:   
            if self.can_move: 
                self.mover()
        self.camera_handle()
        self.tag_handle()
        self.matrix[self.player_position[0], self.player_position[1]] = [255, 0, 0]
        return self.matrix, self.is_tager, self.got_taged 

    def tag_handle(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_UP]:
            self.can_move = True

        if not self.is_tager:
            if self.matrix[self.player_position[0]-1, self.player_position[1], 0] == 0 and self.matrix[self.player_position[0]+1, self.player_position[1], 1] == 255 and self.matrix[self.player_position[0]+1, self.player_position[1], 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1]] = [0, 0, 0]
                self.player_position = [3, 108]
                self.is_tager = True
                self.camera_x_corr = 0
                self.camera_y_corr = 0 
                self.camera = Camera(self.window, self.wnx, self.wny, self.zoom_index, self.player_position, self.sidex, self.sidey)
                self.got_taged = True

            elif self.matrix[self.player_position[0]+1, self.player_position[1], 0] == 0 and self.matrix[self.player_position[0]-1, self.player_position[1], 1] == 255 and self.matrix[self.player_position[0]-1, self.player_position[1], 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1]] = [0, 0, 0]
                self.player_position = [3, 108]
                self.is_tager = True
                self.camera_x_corr = 0
                self.camera_y_corr = 0 
                self.camera = Camera(self.window, self.wnx, self.wny, self.zoom_index, self.player_position, self.sidex, self.sidey) 
                self.got_taged = True

            elif self.matrix[self.player_position[0], self.player_position[1]+1, 0] == 0 and self.matrix[self.player_position[0], self.player_position[1]+1, 1] == 255 and self.matrix[self.player_position[0], self.player_position[1]+1, 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1]] = [0, 0, 0]
                self.player_position = [3, 108]
                self.is_tager = True
                self.camera_x_corr = 0
                self.camera_y_corr = 0 
                self.camera = Camera(self.window, self.wnx, self.wny, self.zoom_index, self.player_position, self.sidex, self.sidey)
                self.got_taged = True

            elif self.matrix[self.player_position[0], self.player_position[1]-1, 0] == 0 and self.matrix[self.player_position[0], self.player_position[1]-1, 1] == 255 and self.matrix[self.player_position[0], self.player_position[1]-1, 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1]] = [0, 0, 0]
                self.player_position = [3, 108]
                self.is_tager = True
                self.camera_x_corr = 0
                self.camera_y_corr = 0 
                self.camera = Camera(self.window, self.wnx, self.wny, self.zoom_index, self.player_position, self.sidex, self.sidey)
                self.got_taged = True
            else:
                self.is_tager = False    




               


    def mover(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d] and self.player_position[0] < self.sidex - 4:   
            self.matrix[self.player_position[0], self.player_position[1], 0] = 0
            self.player_position[0] += 1
            if self.matrix[self.player_position[0], self.player_position[1], 0] == 0 and self.matrix[self.player_position[0], self.player_position[1], 1] == 0 and self.matrix[self.player_position[0], self.player_position[1], 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1], 0] = 255
                self.matrix[self.player_position[0], self.player_position[1], 1] = 0
                self.matrix[self.player_position[0], self.player_position[1], 2] = 0
                if self.camera_x_corr <= -self.camera_corr_speed :
                    self.camera_x_corr -= self.camera_corr_speed 
                else:
                    self.camera_x_corr = -self.camera_corr_speed 
            else:
                self.player_position[0] -= 1
                self.matrix[self.player_position[0], self.player_position[1], 0] = 255    

        elif pressed[pygame.K_q] and self.player_position[0] > 3:     
            self.matrix[self.player_position[0], self.player_position[1], 0] = 0
            self.player_position[0] -= 1
            if self.matrix[self.player_position[0], self.player_position[1], 0] == 0 and self.matrix[self.player_position[0], self.player_position[1], 1] == 0 and self.matrix[self.player_position[0], self.player_position[1], 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1], 0] = 255
                self.matrix[self.player_position[0], self.player_position[1], 1] = 0
                self.matrix[self.player_position[0], self.player_position[1], 2] = 0
                if self.camera_x_corr <= self.camera_corr_speed :
                    self.camera_x_corr += self.camera_corr_speed 
                else:
                    self.camera_x_corr = self.camera_corr_speed
            else:
                self.player_position[0] += 1 
                self.matrix[self.player_position[0], self.player_position[1], 0] = 255   

        elif pressed[pygame.K_z] and self.player_position[1] > 0:
            self.matrix[self.player_position[0], self.player_position[1], 0] = 0
            self.player_position[1] -= 1
            if self.matrix[self.player_position[0], self.player_position[1], 0] == 0 and self.matrix[self.player_position[0], self.player_position[1], 1] == 0 and self.matrix[self.player_position[0], self.player_position[1], 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1], 0] = 255
                self.matrix[self.player_position[0], self.player_position[1], 1] = 0
                self.matrix[self.player_position[0], self.player_position[1], 2] = 0
                if self.camera_y_corr >= self.camera_corr_speed :
                    self.camera_y_corr += self.camera_corr_speed 
                else:
                    self.camera_y_corr = self.camera_corr_speed
            else:
                self.player_position[1] += 1
                self.matrix[self.player_position[0], self.player_position[1], 0] = 255    

        elif pressed[pygame.K_s]:

            self.matrix[self.player_position[0], self.player_position[1], 0] = 0
            self.player_position[1] += 1
            if self.matrix[self.player_position[0], self.player_position[1], 0] == 0 and self.matrix[self.player_position[0], self.player_position[1], 1] == 0 and self.matrix[self.player_position[0], self.player_position[1], 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1], 0] = 255
                self.matrix[self.player_position[0], self.player_position[1], 1] = 0
                self.matrix[self.player_position[0], self.player_position[1], 2] = 0
                if self.camera_y_corr >= -self.camera_corr_speed :
                    self.camera_y_corr -= self.camera_corr_speed 
                else:
                    self.camera_y_corr = -self.camera_corr_speed
            else:
                self.player_position[1] -= 1 #cancel movement 
                self.matrix[self.player_position[0], self.player_position[1], 0] = 255          

    def camera_handle(self): 
        self.camera.updater(self.matrix, self.player_position, self.camera_x_corr, self.camera_y_corr)     


    def drawer(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_a]:
            self.selector = 0

        elif pressed[pygame.K_z]:
            self.selector = 1

        elif pressed[pygame.K_e]:
            self.selector = 2

        if pressed[pygame.K_r] and self.size < 2:
            self.size += 0.01
        if pressed[pygame.K_t] and self.size > 0:
            self.size -= 0.01


        if pressed[pygame.K_UP] and self.colorer[self.selector] < 250:
            self.colorer[self.selector] += 1
        elif pressed[pygame.K_DOWN] and self.colorer[self.selector] > 0:
            self.colorer[self.selector] -= 1

        self.letter = "RED" if self.selector == 0 else "GREEN" if self.selector == 1 else "BLUE"
        caption = (f"SELECTOR = {self.letter}, COLOR = {self.colorer}, SIZE = {int(self.size)} | [A]=RED, [Z]=GREEN, [E]=BLUE, [UP/DOWN]=+/-, LONG PRESS : [R/T]=+/- SIZE.")
        pygame.display.set_caption(caption)

        if pygame.mouse.get_pressed()[0]:
            x_matrix = (pygame.mouse.get_pos()[0] * self.sidex) // self.wnx
            y_matrix = (pygame.mouse.get_pos()[1] * self.sidey) // self.wny
            for i in range(int(self.size)):
                if 0 <= x_matrix + i <= self.sidex - 1 and 0 <= y_matrix + i <= self.sidey - 1 and 0 <= x_matrix - i <= self.sidex - 1 and 0 <= y_matrix - i <= self.sidey - 1:
                    self.matrix[x_matrix + i, y_matrix + i] = (self.colorer[0], self.colorer[1], self.colorer[2])
                    self.matrix[x_matrix - i, y_matrix - i] = (self.colorer[0], self.colorer[1], self.colorer[2])
                    self.matrix[x_matrix + i, y_matrix - i] = (self.colorer[0], self.colorer[1], self.colorer[2])
                    self.matrix[x_matrix - i, y_matrix + i] = (self.colorer[0], self.colorer[1], self.colorer[2])

                    self.matrix[x_matrix + i, y_matrix] = (self.colorer[0], self.colorer[1], self.colorer[2])
                    self.matrix[x_matrix - i, y_matrix] = (self.colorer[0], self.colorer[1], self.colorer[2])
                    self.matrix[x_matrix, y_matrix - i] = (self.colorer[0], self.colorer[1], self.colorer[2])
                    self.matrix[x_matrix, y_matrix + i] = (self.colorer[0], self.colorer[1], self.colorer[2])

















class Grid2:
    def __init__(self, window, wnx, wny, draw=False):
        self.wnx = wnx
        self.wny = wny
        self.sidex = 180
        self.sidey = int(self.sidex / 1.5)
        self.matrix = np.array(matrix)
        self.matrix = self.matrix.reshape(self.sidex, self.sidey, 3)
        self.size = 1
        self.window = window
        self.zoom_index = 2
        self.is_tager = False
        self.player_position = [5, 108]
        self.matrix[self.player_position[0], self.player_position[1]] = [0, 255, 0]
        self.camera = Camera(self.window, self.wnx, self.wny, self.zoom_index, self.player_position, self.sidex, self.sidey)   
        self.camera_x_corr = 0
        self.camera_corr_speed = 31.36
        self.camera_y_corr = 0
        self.got_taged = False


    def updater(self, grid, tagged_someone):
        self.got_taged = False
        if tagged_someone:
            self.is_tager = False
        self.matrix = grid
        self.mover()
        self.camera_handle()
        self.tag_handle()
        self.matrix[self.player_position[0], self.player_position[1]] = [0, 255, 0]
        return self.matrix, self.is_tager, self.got_taged
    
    def tag_handle(self):
        if not self.is_tager:
            if self.matrix[self.player_position[0]-1, self.player_position[1], 0] == 255 and self.matrix[self.player_position[0]+1, self.player_position[1], 1] == 0 and self.matrix[self.player_position[0]+1, self.player_position[1], 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1]] = [0, 0, 0]
                self.player_position = [5, 108]
                self.camera_x_corr = 0
                self.camera_y_corr = 0
                self.camera = Camera(self.window, self.wnx, self.wny, self.zoom_index, self.player_position, self.sidex, self.sidey)
                self.is_tager = True
                self.got_taged = True

            elif self.matrix[self.player_position[0]+1, self.player_position[1], 0] == 255 and self.matrix[self.player_position[0]-1, self.player_position[1], 1] == 0 and self.matrix[self.player_position[0]-1, self.player_position[1], 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1]] = [0, 0, 0]
                self.player_position = [5, 108] 
                self.camera_x_corr = 0
                self.camera_y_corr = 0
                self.camera = Camera(self.window, self.wnx, self.wny, self.zoom_index, self.player_position, self.sidex, self.sidey)
                self.is_tager = True
                self.got_taged = True


            elif self.matrix[self.player_position[0], self.player_position[1]+1, 0] == 255 and self.matrix[self.player_position[0], self.player_position[1]+1, 1] == 0 and self.matrix[self.player_position[0], self.player_position[1]+1, 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1]] = [0, 0, 0]
                self.player_position = [5, 108]
                self.camera_x_corr = 0
                self.camera_y_corr = 0
                self.camera = Camera(self.window, self.wnx, self.wny, self.zoom_index, self.player_position, self.sidex, self.sidey)
                self.is_tager = True
                self.got_taged = True


            elif self.matrix[self.player_position[0], self.player_position[1]-1, 0] == 255 and self.matrix[self.player_position[0], self.player_position[1]-1, 1] == 0 and self.matrix[self.player_position[0], self.player_position[1]-1, 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1]] = [0, 0, 0]
                self.player_position = [5, 108]
                self.camera_x_corr = 0
                self.camera_y_corr = 0 
                self.camera = Camera(self.window, self.wnx, self.wny, self.zoom_index, self.player_position, self.sidex, self.sidey)
                self.is_tager = True
                self.got_taged = True
            else:
                self.is_tager = False    


            
        


    def mover(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT] and self.player_position[0] < self.sidex - 4:   
            self.matrix[self.player_position[0], self.player_position[1], 1] = 0
            self.player_position[0] += 1
            if self.matrix[self.player_position[0], self.player_position[1], 0] == 0 and self.matrix[self.player_position[0], self.player_position[1], 1] == 0 and self.matrix[self.player_position[0], self.player_position[1], 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1], 0] = 0
                self.matrix[self.player_position[0], self.player_position[1], 1] = 255
                self.matrix[self.player_position[0], self.player_position[1], 2] = 0
                if self.camera_x_corr <= -self.camera_corr_speed :
                    self.camera_x_corr -= self.camera_corr_speed 
                else:
                    self.camera_x_corr = -self.camera_corr_speed 
            else:
                self.player_position[0] -= 1
                self.matrix[self.player_position[0], self.player_position[1], 1] = 255    

        elif pressed[pygame.K_LEFT] and self.player_position[0] > 3:     
            self.matrix[self.player_position[0], self.player_position[1], 1] = 0
            self.player_position[0] -= 1
            if self.matrix[self.player_position[0], self.player_position[1], 0] == 0 and self.matrix[self.player_position[0], self.player_position[1], 1] == 0 and self.matrix[self.player_position[0], self.player_position[1], 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1], 0] = 0
                self.matrix[self.player_position[0], self.player_position[1], 1] = 255
                self.matrix[self.player_position[0], self.player_position[1], 2] = 0
                if self.camera_x_corr <= self.camera_corr_speed :
                    self.camera_x_corr += self.camera_corr_speed 
                else:
                    self.camera_x_corr = self.camera_corr_speed
            else:
                self.player_position[0] += 1 
                self.matrix[self.player_position[0], self.player_position[1], 1] = 255   

        elif pressed[pygame.K_UP] and self.player_position[1] > 0:
            self.matrix[self.player_position[0], self.player_position[1], 1] = 0
            self.player_position[1] -= 1
            if self.matrix[self.player_position[0], self.player_position[1], 0] == 0 and self.matrix[self.player_position[0], self.player_position[1], 1] == 0 and self.matrix[self.player_position[0], self.player_position[1], 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1], 0] = 0
                self.matrix[self.player_position[0], self.player_position[1], 1] = 255
                self.matrix[self.player_position[0], self.player_position[1], 2] = 0
                if self.camera_y_corr >= self.camera_corr_speed :
                    self.camera_y_corr += self.camera_corr_speed 
                else:
                    self.camera_y_corr = self.camera_corr_speed
            else:
                self.player_position[1] += 1
                self.matrix[self.player_position[0], self.player_position[1], 1] = 255   

        elif pressed[pygame.K_DOWN]:

            self.matrix[self.player_position[0], self.player_position[1], 1] = 0
            self.player_position[1] += 1
            if self.matrix[self.player_position[0], self.player_position[1], 0] == 0 and self.matrix[self.player_position[0], self.player_position[1], 1] == 0 and self.matrix[self.player_position[0], self.player_position[1], 2] == 0:
                self.matrix[self.player_position[0], self.player_position[1], 0] = 0
                self.matrix[self.player_position[0], self.player_position[1], 1] = 255
                self.matrix[self.player_position[0], self.player_position[1], 2] = 0
                if self.camera_y_corr >= -self.camera_corr_speed :
                    self.camera_y_corr -= self.camera_corr_speed 
                else:
                    self.camera_y_corr = -self.camera_corr_speed
            else:
                self.player_position[1] -= 1 #cancel movement 
                self.matrix[self.player_position[0], self.player_position[1], 1] = 255         

    def camera_handle(self): 
        self.camera.updater(self.matrix, self.player_position, self.camera_x_corr, self.camera_y_corr)     


    
