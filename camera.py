import pygame
import numpy as np
import time

class Camera:
    def __init__(self, window, wnx, wny, zoom_index, player_position, sidex, sidey):
        self.window = window
        self.wnx = wnx
        self.wny = wny
        self.zoom_index = zoom_index
        self.player_position = player_position
        self.sidex = sidex
        self.sidey = sidey
        self.og_wnx = self.wnx
        self.og_wny = self.wny
        if self.zoom_index == 0:
            self.zoom = 1
        if self.zoom_index == 1:
            self.zoom = 1
        if self.zoom_index == 2:
            self.zoom = 9.5       
        

    def surface_zone_handle(self):
        # Calculate the new camera position

        self.player_screen_x = self.player_position[0] * (self.og_wnx // self.sidex)
        self.player_screen_y = self.player_position[1] * (self.og_wny // self.sidey) + self.og_wny*(self.zoom-2) if self.zoom_index == 2 else self.player_position[1] * (self.og_wny // self.sidey) - 2*self.sidey

        self.wnx = self.og_wnx * self.zoom
        self.wny = self.og_wny * self.zoom


        if self.zoom_index == 2:
            self.x = -self.player_screen_x + self.wnx // self.zoom*0.5 - 120

            self.y = -self.player_screen_y + self.wny // self.zoom*0.5 - 120

        if self.zoom_index == 1:
            self.x = -self.player_screen_x + self.wnx // 2

            self.y = -self.player_screen_y + self.wny // 2    

        if self.zoom_index == 0:
            self.x = 0

            self.y = -self.player_screen_y + self.wny // 2

  
        
        
    def updater(self, matrix, player_position, x_corrector, y_corrector):
        self.x_corrector = x_corrector
        self.y_corrector = y_corrector
        self.matrix = matrix
        self.player_position = player_position
        self.surface_zone_handle()
        self.draw_matrix()


    def draw_matrix(self):
        self.surface = pygame.transform.scale(pygame.surfarray.make_surface(self.matrix), (self.wnx, self.wny))
        if self.zoom_index == 2:
            self.window.blit(self.surface, (self.x + self.x_corrector, self.y+self.y_corrector))
        else:
            self.window.blit(self.surface, (self.x, self.y))    

       
