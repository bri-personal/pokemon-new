import pygame
from settings import *
from world import World
from player import *

#show text on surface with parameters given
def draw_text(surface,text,size,color,x,y,orientation):
    font=pygame.font.Font(pygame.font.match_font(FONT_NAME),size)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect()
    if orientation=='topleft':
        text_rect.topleft=(x,y)
    elif orientation=='midtop':
        text_rect.midtop=(x,y)
    elif orientation=='center':
        text_rect.center=(x,y)
    surface.blit(text_surface,text_rect)

#classes
class Player_Sprite(pygame.sprite.Sprite,Player):
    SPEED=World.TILE_SIZE//5

    def __init__(self,game,x,y,player):
        self.game=game
        self.groups=self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        Player.__init__(self)
        self.load_files()
        
        self.image=pygame.Surface((World.TILE_SIZE,World.TILE_SIZE))
        self.image.fill(RED)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
        self.dx=0 #change in x for each frame
        self.dy=0 #change in y for each frame

        self.player=player
        
    def load_files(self):
        #load player images, sounds, etc.
        pass
    
    def update(self):
        self.dx=0
        self.dy=0
        #move left/right
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dx-=Player_Sprite.SPEED
        if keys[pygame.K_RIGHT]:
            self.dx+=Player_Sprite.SPEED
        if keys[pygame.K_DOWN]:
            self.dy+=Player_Sprite.SPEED
        if keys[pygame.K_UP]:
            self.dy-=Player_Sprite.SPEED

        #prevents player from walking through walls
        for tile in self.game.world.wall_tiles:
            #rect is bottom tile_size x tile_size square of sprite, so collisions only happen with tile-sized object on the tile
            #if tile image extends above tile square, player can pass through it
            if tile.hitbox.colliderect(self.rect.x+self.dx,self.rect.y,self.rect.width,self.rect.height):
                if self.dx<0:
                    self.dx=tile.hitbox.right-self.rect.left
                if self.dx>0:
                    self.dx=tile.hitbox.left-self.rect.right
            if tile.hitbox.colliderect(self.rect.x,self.rect.y+self.dy,self.rect.width,self.rect.height):
               if self.dy<0:
                    self.dy=tile.hitbox.bottom-self.rect.top
               if self.dy>0:
                    self.dy=tile.hitbox.top-self.rect.bottom

        #prevents player from moving off screen
        if self.rect.x+self.dx<0:
            self.dx=-self.rect.left #player can go to left edge
        elif self.rect.right+self.dx>WIDTH:
            self.dx=WIDTH-self.rect.right #player can go to right edge
        if self.rect.y+self.dy<World.TILE_SIZE:
            self.dy=World.TILE_SIZE-self.rect.top #player can go to 1 TILE_SIZE below the top for landscape
        elif self.rect.bottom+self.dy>HEIGHT-World.TILE_SIZE:
            self.dy=HEIGHT-World.TILE_SIZE-self.rect.bottom #player can go to 1 TILE_SIZE above the bottom for landscape

        self.rect.x+=self.dx
        self.rect.y+=self.dy

class Button:
    def __init__(self,game,x,y,image):
        self.game=game
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.y=y
        self.clicked=False
    
    def draw(self):
        action=False
        #get mouse pos
        pos=pygame.mouse.get_pos()
        
        #check mouseover and click conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and not self.clicked:
                self.clicked=True
                action=True
            if pygame.mouse.get_pressed()[0]==0 and self.clicked:
                self.clicked=False
        
        self.game.screen.blit(self.image,self.rect)
        return action
