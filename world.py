import pygame
from settings import *

class World:
    NUM_TILES=15 #number of tiles to be shown on shorter dimension of screen
    TILE_SIZE=HEIGHT//NUM_TILES #size of tiles on screen

    def __init__(self,game,data): #data is matrix (list of lists) of tiles
        self.game=game
        self.all_tiles=[]
        row_count=0
        for row in data:
            col_count=0
            for tile in row:
                if tile==0:
                    img=pygame.Surface((World.TILE_SIZE,World.TILE_SIZE))
                    img.fill(GREEN)
                    img_rect=img.get_rect()
                    img_rect.x=World.TILE_SIZE*col_count
                    img_rect.bottom=World.TILE_SIZE*(row_count+1)
                    tile=(img,img_rect)
                    self.all_tiles.append(tile)
                elif tile==1:
                    img=pygame.Surface((World.TILE_SIZE,World.TILE_SIZE))
                    img.fill(YELLOW)
                    img_rect=img.get_rect()
                    img_rect.x=World.TILE_SIZE*col_count
                    img_rect.bottom=World.TILE_SIZE*(row_count+1)
                    tile=(img,img_rect)
                    self.all_tiles.append(tile)
                col_count+=1
            row_count+=1
         
    def draw_tiles(self):
        for tile in self.all_tiles:
            self.game.screen.blit(tile[0],tile[1])

