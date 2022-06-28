import pygame
from settings import *

class World:
    NUM_TILES=15 #number of tiles to be shown on shorter dimension of screen
    TILE_SIZE=HEIGHT//NUM_TILES #size of tiles on screen

    def __init__(self,game,data,x,y): #data is matrix (list of lists) of tiles
        self.game=game
        self.all_tiles=[]
        self.floor_tiles=[]
        self.wall_tiles=[]
        self.grass_tiles=[]
        row_count=0
        for row in data:
            col_count=0
            for tile in row:
                if tile==0:
                    img=pygame.Surface((World.TILE_SIZE,World.TILE_SIZE))
                    img.fill(GREEN)
                    tile=Tile(img,x+World.TILE_SIZE*col_count,y+World.TILE_SIZE*row_count) #first tile has topleft at x,y
                    self.all_tiles.append(tile)
                    self.floor_tiles.append(tile)
                elif tile==1:
                    img=pygame.Surface((World.TILE_SIZE,World.TILE_SIZE))
                    img.fill(YELLOW)
                    tile=Tile(img,x+World.TILE_SIZE*col_count,y+World.TILE_SIZE*row_count)
                    self.all_tiles.append(tile)
                    self.wall_tiles.append(tile)
                elif tile==2:
                    img=pygame.Surface((World.TILE_SIZE,World.TILE_SIZE))
                    img.fill(DARK_GREEN)
                    tile=Tile(img,x+World.TILE_SIZE*col_count,y+World.TILE_SIZE*row_count)
                    self.all_tiles.append(tile)
                    self.grass_tiles.append(tile)

                col_count+=1
            row_count+=1
         
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



