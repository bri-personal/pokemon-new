import pygame
from settings import *

class World:
    NUM_TILES=15 #number of tiles to be shown on shorter dimension of screen
    TILE_SIZE=HEIGHT//NUM_TILES #size of tiles on screen

    def __init__(self,game,data,x,bottom): #data is matrix (list of lists) of tiles
        self.game=game
        self.all_tiles=[]
        self.floor_tiles=[]
        self.wall_tiles=[]
        self.grass_tiles=[]
        
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j]==0:
                    img=pygame.Surface((World.TILE_SIZE,World.TILE_SIZE))
                    img.fill(GREEN)
                    self.add_tile(img,x,bottom,i,j)
                    self.floor_tiles.append(self.all_tiles[-1])
                elif data[i][j]==1:
                    img=pygame.Surface((World.TILE_SIZE,World.TILE_SIZE))
                    img.fill(YELLOW)
                    self.add_tile(img,x,bottom,i,j)
                    self.wall_tiles.append(self.all_tiles[-1])
                elif data[i][j]==2:
                    img=pygame.Surface((World.TILE_SIZE,World.TILE_SIZE))
                    img.fill(DARK_GREEN)
                    self.add_tile(img,x,bottom,i,j)
                    self.grass_tiles.append(self.all_tiles[-1])

    #uniform way to create tiles
    def add_tile(self,img,x,bottom,row_count,col_count):
        tile=Tile(img,x+World.TILE_SIZE*col_count,bottom+World.TILE_SIZE*row_count)
        self.all_tiles.append(tile)
         
    #draw all tiles on screen
    def draw_tiles(self):
        for tile in self.all_tiles:
            tile.draw(self.game.screen)

class Tile:

    def __init__(self, image, x, bottom):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.bottom=bottom

        self.hitbox=pygame.Rect(self.rect.x,self.rect.bottom-World.TILE_SIZE,World.TILE_SIZE,World.TILE_SIZE)

    #draw tile image on screen
    def draw(self,surface):
        surface.blit(self.image,self.rect)

    #move tile and hitbox in x dir
    def move_x(self,dx):
        self.rect.x+=dx
        self.hitbox.x+=dx
    
    #move tile and hitbox in y dir
    def move_y(self,dy):
        self.rect.y+=dy
        self.hitbox.y+=dy



