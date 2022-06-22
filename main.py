from sre_parse import WHITESPACE
import pygame
import random
from os import path
from enum import Enum
from settings import *
from sprites import *
from world import *
from player import *
from pokemon import *

class Pages(Enum):
    START=0
    WORLD=1
    BATTLE=2
    MENU=3
    DEX=4
    BOXES=5
    BAG=6
    CARD=7
    SAVE=8
    MAP=9
    CAMP=10
    GIFT=11
    VS=12
    SETTINGS=13
    END=-1
     
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
        for i in range(len(MENU_TEXT)):
            img=pygame.Surface((MENU_BUTTON_SIZE,MENU_BUTTON_SIZE))
            img.fill(WHITE)
            draw_text(img,MENU_TEXT[i],MENU_BUTTON_SIZE//6,MENU_COLORS[i],MENU_BUTTON_SIZE//2,MENU_BUTTON_SIZE//2,'center')
            self.menu_buttons.append(Button(self,WIDTH//2-5*MENU_BUTTON_SIZE//2-2*BORDER_BTW_BUTTONS+(i%(len(MENU_TEXT)//2))*(MENU_BUTTON_SIZE+BORDER_BTW_BUTTONS)+MENU_BUTTON_SIZE//2,HEIGHT//2-MENU_BUTTON_SIZE-BORDER_BTW_BUTTONS-BUTTON_TEXT_BORDER+(MENU_BUTTON_SIZE+BORDER_BTW_BUTTONS*2+BUTTON_TEXT_BORDER)*(i//(len(MENU_TEXT)//2)),img))

        #create player
        self.player=Player_Sprite(self,World.TILE_SIZE*2,World.TILE_SIZE*2,Player())
        
        #for testing catches
#        for _ in range(19):
#            self.player.catch(Pokemon('Bulbasaur'))
#            self.player.catch(Pokemon('Charmander'))
#
#        print(self.player.party)
#        print(self.player.boxes)
        ######################

        #create world
        self.world=World(self,TEST_WORLD)

        #index for which button is selected on the menu screen
        self.menu_selection=0

        #indices for which Pokemon are shown on the dex page and which is selected
        self.dex_start=0
        self.dex_selection=0
        
        self.page=Pages.START
        self.run()

    #main loop calls other methods for specific pages
    def run(self):
        self.playing=True
        while self.playing:
            #keep loop running at correct speed
            self.clock.tick(FPS)
            if self.page==Pages.START:
                self.start_screen()
            elif self.page==Pages.WORLD:
                self.world_screen()
            elif self.page==Pages.BATTLE:
                self.battle_screen()
            elif self.page==Pages.MENU:
                self.menu_screen()
            elif self.page==Pages.DEX:
                self.dex_screen()
            elif self.page==Pages.BOXES:
                self.boxes_screen()
            elif self.page==Pages.BAG:
                self.bag_screen()
            elif self.page==Pages.CARD:
                self.card_screen()
            elif self.page==Pages.SAVE:
                self.save_screen()
            elif self.page==Pages.MAP:
                self.map_screen()
            elif self.page==Pages.CAMP:
                self.camp_screen()
            elif self.page==Pages.GIFT:
                self.gift_screen()
            elif self.page==Pages.VS:
                self.vs_screen()
            elif self.page==Pages.SETTINGS:
                self.settings_screen()
            elif self.page==Pages.END:
                self.end_screen()
            else:
                print("Page not found!")
                self.page=Pages.START
            
    #screen for game menu
    def menu_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_a:
                    match self.menu_selection:
                        case 0:
                            self.page=Pages.DEX
                        case 1:
                            self.page=Pages.BOXES
                        case 2:
                            self.page=Pages.BAG
                        case 3:
                            self.page=Pages.CARD
                        case 4:
                            self.page=Pages.SAVE
                        case 5:
                            self.page=Pages.MAP
                        case 6:
                            self.page=Pages.CAMP
                        case 7:
                            self.page=Pages.GIFT
                        case 8:
                            self.page=Pages.VS
                        case 9:
                            self.page=Pages.SETTINGS
                if event.key==pygame.K_b:
                    self.page=Pages.WORLD
                if event.key==pygame.K_RIGHT:
                    if self.menu_selection==len(MENU_TEXT)//2-1:
                        self.menu_selection=0
                    elif self.menu_selection==len(MENU_TEXT)-1:
                        self.menu_selection=len(MENU_TEXT)//2
                    else:
                        self.menu_selection+=1
                if event.key==pygame.K_LEFT:
                    if self.menu_selection==0:
                        self.menu_selection=len(MENU_TEXT)//2-1
                    elif self.menu_selection==len(MENU_TEXT)//2:
                        self.menu_selection=len(MENU_TEXT)-1
                    else:
                        self.menu_selection-=1
                if event.key==pygame.K_DOWN:
                    self.menu_selection=(self.menu_selection+len(MENU_TEXT)//2)%len(MENU_TEXT)
                if event.key==pygame.K_UP:
                    self.menu_selection=(self.menu_selection-len(MENU_TEXT)//2)%len(MENU_TEXT)

        self.screen.fill(RED)

        #display menu buttons
        for i in range(len(self.menu_buttons)):
            draw_text(self.screen,MENU_TEXT[i],BUTTON_TEXT_BORDER//2,WHITE,WIDTH//2-5*MENU_BUTTON_SIZE//2-2*BORDER_BTW_BUTTONS+(i%(len(MENU_TEXT)//2))*(MENU_BUTTON_SIZE+BORDER_BTW_BUTTONS)+MENU_BUTTON_SIZE//2,HEIGHT//2-MENU_BUTTON_SIZE-BORDER_BTW_BUTTONS-BUTTON_TEXT_BORDER+(MENU_BUTTON_SIZE+BORDER_BTW_BUTTONS*2+BUTTON_TEXT_BORDER)*(i//(len(MENU_TEXT)//2))+MENU_BUTTON_SIZE+BORDER_BTW_BUTTONS//2,'midtop')
            if i==self.menu_selection:
                pygame.draw.rect(self.screen,WHITE,(WIDTH//2-5*MENU_BUTTON_SIZE//2-2*BORDER_BTW_BUTTONS+(i%(len(MENU_TEXT)//2))*(MENU_BUTTON_SIZE+BORDER_BTW_BUTTONS)-BORDER_BTW_BUTTONS//2,HEIGHT//2-MENU_BUTTON_SIZE-BORDER_BTW_BUTTONS-BUTTON_TEXT_BORDER+(MENU_BUTTON_SIZE+BORDER_BTW_BUTTONS*2+BUTTON_TEXT_BORDER)*(i//(len(MENU_TEXT)//2))-BORDER_BTW_BUTTONS//2,MENU_BUTTON_SIZE+BORDER_BTW_BUTTONS,MENU_BUTTON_SIZE+BORDER_BTW_BUTTONS),3)

            if self.menu_buttons[i].draw():
                match i:
                    case 0:
                        self.page=Pages.DEX
                    case 1:
                        self.page=Pages.BOXES
                    case 2:
                        self.page=Pages.BAG
                    case 3:
                        self.page=Pages.CARD
                    case 4:
                        self.page=Pages.SAVE
                    case 5:
                        self.page=Pages.MAP
                    case 6:
                        self.page=Pages.CAMP
                    case 7:
                        self.page=Pages.GIFT
                    case 8:
                        self.page=Pages.VS
                    case 9:
                        self.page=Pages.SETTINGS

        pygame.display.flip()

    #default game loop method
    def world_screen(self):
        #process input (events)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_x:
                    self.page=Pages.MENU
                
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

    def battle_screen(self):
        self.page=Pages.WORLD

    def dex_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_b:
                    self.page=Pages.MENU
                if event.key==pygame.K_DOWN:
                    if self.dex_selection<12-1: #replace 12 with length of dex
                        self.dex_selection+=1
                        if self.dex_selection>=self.dex_start+DEX_NUM_BUTTONS:
                            self.dex_start+=1
                    else:
                        self.dex_start=0
                        self.dex_selection=0
                if event.key==pygame.K_UP:
                    if self.dex_selection>0:
                        self.dex_selection-=1
                        if self.dex_selection<self.dex_start:
                            self.dex_start-=1
                    else:
                        self.dex_start=12-DEX_NUM_BUTTONS #replace 12 with length of dex
                        self.dex_selection=12-1 #replace 12 with length of dex

        self.screen.fill(MENU_COLORS[MENU_TEXT.index('Pokedex')])
        pygame.draw.rect(self.screen,WHITE,(WIDTH//20+WIDTH//2+WIDTH//20,HEIGHT//2-BORDER_BTW_BUTTONS*5//2-3*DEX_BUTTON_SIZE,WIDTH*7//20,DEX_NUM_BUTTONS*DEX_BUTTON_SIZE+(DEX_NUM_BUTTONS-1)*BORDER_BTW_BUTTONS),3)

        count=0
        for i in range(self.dex_start,self.dex_start+DEX_NUM_BUTTONS):
            if i==self.dex_selection:
                color=WHITE
            else:
                color=BLACK
            pygame.draw.rect(self.screen,color,(WIDTH//20,HEIGHT//2-BORDER_BTW_BUTTONS*5//2-3*DEX_BUTTON_SIZE+count*(DEX_BUTTON_SIZE+BORDER_BTW_BUTTONS),WIDTH//2,DEX_BUTTON_SIZE),3)
            draw_text(self.screen,str(i),DEX_BUTTON_SIZE//2,color,WIDTH//20+WIDTH//4,HEIGHT//2-BORDER_BTW_BUTTONS*5//2-3*DEX_BUTTON_SIZE+DEX_BUTTON_SIZE//2+count*(DEX_BUTTON_SIZE+BORDER_BTW_BUTTONS),'center')
            count+=1

        pygame.display.flip()

    def boxes_screen(self):
        self.page=Pages.WORLD

    def bag_screen(self):
        self.page=Pages.WORLD

    def card_screen(self):
        self.page=Pages.WORLD

    def save_screen(self):
        self.page=Pages.WORLD

    def map_screen(self):
        self.page=Pages.WORLD

    def camp_screen(self):
        self.page=Pages.WORLD

    def gift_screen(self):
        self.page=Pages.WORLD

    def vs_screen(self):
        self.page=Pages.WORLD

    def settings_screen(self):
        self.page=Pages.WORLD

    #start screen shown when game is first opened
    def start_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_a:
                    self.page=Pages.WORLD
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