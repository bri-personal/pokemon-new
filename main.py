import pygame
import random
from os import path
from settings import *
from sprites import *
from world import *
from player import *
from pokemon import *
     
class Game:
    def __init__(self):
        #initialize pygame and create window
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.mixer.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock=pygame.time.Clock()
        self.font_name=pygame.font.match_font(FONT_NAME)
        self.load_data()
        self.running=True
        
    #load images, sounds, etc.
    def load_data(self):
        #set folders to find images and sounds
        self.dir=path.dirname(__file__)
        self.img_dir=path.join(self.dir,'img')
        self.snd_dir=path.join(self.dir,'snd')
    
    #start a new game
    def new(self):
        #create Sprite groups
        self.all_sprites=pygame.sprite.Group()

        #create buttons
        self.menu_buttons=[] #make buttons for main game menu
        for i in range(len(menu_text)):
            img=pygame.Surface((BUTTON_SIZE,BUTTON_SIZE))
            img.fill(WHITE)
            draw_text(img,menu_text[i],32,RED,BUTTON_SIZE//2,BUTTON_SIZE//2,'center')
            self.menu_buttons.append(Button(self,WIDTH//2-2*BUTTON_SIZE-1.5*BORDER_BTW_BUTTONS+(i%(len(menu_text)//2))*(BUTTON_SIZE+BORDER_BTW_BUTTONS)+BUTTON_SIZE//2,HEIGHT//2-BUTTON_SIZE-BORDER_BTW_BUTTONS-BUTTON_TEXT_BORDER+(BUTTON_SIZE+BORDER_BTW_BUTTONS*2+BUTTON_TEXT_BORDER)*(i//(len(menu_text)//2)),img))

        #create player
        self.player=Player_Sprite(self,World.TILE_SIZE*2,World.TILE_SIZE*2,Player())
        
        #for testing catches
        for _ in range(19):
            self.player.catch(Pokemon('Bulbasaur'))
            self.player.catch(Pokemon('Charmander'))

        print(self.player.party)
        print(self.player.boxes)
        ######################

        #create world
        self.world=World(self,TEST_WORLD)
        
        self.page='start'
        self.run()

    #main loop calls other methods for specific pages
    def run(self):
        self.playing=True
        while self.playing:
            #keep loop running at correct speed
            self.clock.tick(FPS)
            if self.page=='start':
                self.start_screen()
            elif self.page=='play':
                self.play_screen()
            elif self.page=='menu':
                self.menu_screen()
            elif self.page=='end':
                self.end_screen()
            else:
                print("Page not found!")
                self.page='start'
            
    #screen for game menu
    def menu_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_b:
                    self.page='play'

        self.screen.fill(RED)

        #display menu buttons
        for i in range(len(self.menu_buttons)):
            self.menu_buttons[i].draw()
            draw_text(self.screen,menu_text[i],BUTTON_TEXT_BORDER//2,WHITE,WIDTH//2-2*BUTTON_SIZE-1.5*BORDER_BTW_BUTTONS+(i%(len(menu_text)//2))*(BUTTON_SIZE+BORDER_BTW_BUTTONS)+BUTTON_SIZE//2,HEIGHT//2-BUTTON_SIZE-BORDER_BTW_BUTTONS-BUTTON_TEXT_BORDER+(BUTTON_SIZE+BORDER_BTW_BUTTONS*2+BUTTON_TEXT_BORDER)*(i//(len(menu_text)//2))+BUTTON_SIZE+BORDER_BTW_BUTTONS,'midtop')

        pygame.display.flip()

    #default game loop method
    def play_screen(self):
        #process input (events)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_x:
                    self.page='menu'
                
        #update
        self.all_sprites.update()
        
        #draw/render
        #scroll world as player moves across screen if world is too big for screen
        #scroll left/right
        if self.player.rect.x<WIDTH//2 and self.world.all_tiles[0].rect.x<0 or self.player.rect.x>WIDTH//2 and self.world.all_tiles[len(self.world.all_tiles)-1].rect.right>WIDTH:
            self.player.dx=self.player.rect.x-WIDTH//2
            for tile in self.world.all_tiles:
                tile.move_x(-self.player.dx)
            for sprite in self.all_sprites:
                sprite.rect.x-=self.player.dx
                
        #make sure edge tiles do not move past left/right edges
        if self.world.all_tiles[0].rect.x>0:
            dx=self.world.all_tiles[0].rect.x
            for tile in self.world.all_tiles:
                tile.move_x(-dx)
            for sprite in self.all_sprites:
                sprite.rect.x-=dx
                
        if self.world.all_tiles[len(self.world.all_tiles)-1].rect.right<WIDTH:
            dx=WIDTH-self.world.all_tiles[len(self.world.all_tiles)-1].rect.right
            for tile in self.world.all_tiles:
                tile.move_x(dx)
            for sprite in self.all_sprites:
                sprite.rect.x+=dx
                
        #scroll up/down
        if self.player.rect.y<HEIGHT//2 and self.world.all_tiles[0].rect.y<World.TILE_SIZE or self.player.rect.y>HEIGHT//2 and self.world.all_tiles[len(self.world.all_tiles)-1].rect.bottom>HEIGHT-World.TILE_SIZE:
            self.player.dy=self.player.rect.y-HEIGHT//2
            for tile in self.world.all_tiles:
                tile.move_y(-self.player.dy)
            for sprite in self.all_sprites:
                sprite.rect.y-=self.player.dy
             
        #make sure edge tiles do not move past top/bottom edges
        if self.world.all_tiles[0].rect.y>World.TILE_SIZE:
            dy=self.world.all_tiles[0].rect.y-World.TILE_SIZE
            for tile in self.world.all_tiles:
                tile.move_y(-dy)
            for sprite in self.all_sprites:
                sprite.rect.y-=dy
                
        if self.world.all_tiles[len(self.world.all_tiles)-1].rect.bottom<HEIGHT-World.TILE_SIZE:
            dy=HEIGHT-World.TILE_SIZE-self.world.all_tiles[len(self.world.all_tiles)-1].rect.bottom
            for tile in self.world.all_tiles:
                tile.move_y(dy)
            for sprite in self.all_sprites:
                sprite.rect.y+=dy
        ######################
        
        self.screen.fill(DARK_GREEN)
        self.world.draw_tiles()
        self.all_sprites.draw(self.screen)
        
        pygame.display.flip()

    #start screen shown when game is first opened
    def start_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_a:
                    self.page='play'
        self.screen.fill(BLACK)
        draw_text(self.screen,TITLE,48,WHITE,WIDTH//2,HEIGHT//4,'midtop')
        draw_text(self.screen,"Press 'A' to start",36,WHITE,WIDTH//2,HEIGHT//2,'midtop')
        pygame.display.flip()
        
    #end screen shown when game is over
    def end_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
        self.screen.fill(BLACK)
        draw_text(self.screen,"GAME OVER",48,WHITE,WIDTH//2,HEIGHT//4,'midtop')
        pygame.display.flip()

if __name__=='__main__':
    g=Game()
    while g.running:
        g.new()

    pygame.quit()