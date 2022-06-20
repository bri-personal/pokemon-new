import pygame
from settings import *
from world import World

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
class Player(pygame.sprite.Sprite):
    SPEED=World.TILE_SIZE//5

    def __init__(self,game,x,y):
        self.game=game
        self.groups=self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.load_files()
        
        self.image=pygame.Surface((World.TILE_SIZE,World.TILE_SIZE))
        self.image.fill(RED)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
        self.dx=0
        self.dy=0
        
    def load_files(self):
        #load player images, sounds, etc.
        pass
    
    def update(self):
        self.dx=0
        self.dy=0
        #move left/right
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dx-=Player.SPEED
        if keys[pygame.K_RIGHT]:
            self.dx+=Player.SPEED
        if keys[pygame.K_DOWN]:
            self.dy+=Player.SPEED
        if keys[pygame.K_UP]:
            self.dy-=Player.SPEED
            
        self.rect.x+=self.dx
        self.rect.y+=self.dy
        
        #stop player from moving off screen
        if self.rect.x<0:
            self.rect.x=0 #player can go to left edge
        elif self.rect.right>WIDTH:
            self.rect.right=WIDTH #player can go to right edge
        if self.rect.y<World.TILE_SIZE:
            self.rect.y=World.TILE_SIZE #player can go to 1 TILE_SIZE below the top for landscape
        if self.rect.bottom>HEIGHT-World.TILE_SIZE:
            self.rect.bottom=HEIGHT-World.TILE_SIZE #player can go to 1 TILE_SIZE above the bottom for landscape

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
