import pygame
from os import path
from pages import Pages
from settings import *
from sprites import *
from world import *
from menu import MenuUI
from dex import DexUI
from player import Player
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
        #pass

        #create menu
        self.menu=MenuUI(self)

        #create dex
        self.dex=DexUI(self)

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

    #default game loop method
    def world_screen(self):
        #process input (events)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
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

    #screen for game menu
    def menu_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_a:
                    self.page=self.menu.get_page_from_button()
                if event.key==pygame.K_b:
                    self.page=Pages.WORLD
                if event.key==pygame.K_RIGHT:
                    self.menu.move_right()
                if event.key==pygame.K_LEFT:
                    self.menu.move_left()
                if event.key==pygame.K_UP:
                    self.menu.move_up()
                if event.key==pygame.K_DOWN:
                    self.menu.move_down()

        self.screen.fill(RED)

        #display menu buttons
        for i in range(len(self.menu.buttons)):
            draw_text(self.screen,MenuUI.MENU_TEXT[i],MenuUI.BUTTON_TEXT_BORDER//2,WHITE,WIDTH//2-5*MenuUI.MENU_BUTTON_SIZE//2-2*MenuUI.BORDER_BTW_BUTTONS+(i%(len(MenuUI.MENU_TEXT)//2))*(MenuUI.MENU_BUTTON_SIZE+MenuUI.BORDER_BTW_BUTTONS)+MenuUI.MENU_BUTTON_SIZE//2,HEIGHT//2-MenuUI.MENU_BUTTON_SIZE-MenuUI.BORDER_BTW_BUTTONS-MenuUI.BUTTON_TEXT_BORDER+(MenuUI.MENU_BUTTON_SIZE+MenuUI.BORDER_BTW_BUTTONS*2+MenuUI.BUTTON_TEXT_BORDER)*(i//(len(MenuUI.MENU_TEXT)//2))+MenuUI.MENU_BUTTON_SIZE+MenuUI.BORDER_BTW_BUTTONS//2,'midtop')
            if i==self.menu.selection:
                pygame.draw.rect(self.screen,WHITE,(WIDTH//2-5*MenuUI.MENU_BUTTON_SIZE//2-2*MenuUI.BORDER_BTW_BUTTONS+(i%(len(MenuUI.MENU_TEXT)//2))*(MenuUI.MENU_BUTTON_SIZE+MenuUI.BORDER_BTW_BUTTONS)-MenuUI.BORDER_BTW_BUTTONS//2,HEIGHT//2-MenuUI.MENU_BUTTON_SIZE-MenuUI.BORDER_BTW_BUTTONS-MenuUI.BUTTON_TEXT_BORDER+(MenuUI.MENU_BUTTON_SIZE+MenuUI.BORDER_BTW_BUTTONS*2+MenuUI.BUTTON_TEXT_BORDER)*(i//(len(MenuUI.MENU_TEXT)//2))-MenuUI.BORDER_BTW_BUTTONS//2,MenuUI.MENU_BUTTON_SIZE+MenuUI.BORDER_BTW_BUTTONS,MenuUI.MENU_BUTTON_SIZE+MenuUI.BORDER_BTW_BUTTONS),3)

            #buttons can be pressed to open screens
            if self.menu.buttons[i].draw():
                self.menu.selection=i
                self.page=self.menu.get_page_from_button()

        pygame.display.flip()

    def dex_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b:
                    self.page=Pages.MENU
                if event.key==pygame.K_DOWN:
                    self.dex.move_down()
                if event.key==pygame.K_UP:
                    self.dex.move_up()

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Pokedex')])
        pygame.draw.rect(self.screen,WHITE,(WIDTH//20+WIDTH//2+WIDTH//20,HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_SIZE,WIDTH*7//20,DexUI.DEX_NUM_BUTTONS*DexUI.DEX_BUTTON_SIZE+(DexUI.DEX_NUM_BUTTONS-1)*DexUI.BORDER_BTW_BUTTONS),3)

        count=0
        for i in range(self.dex.start,self.dex.start+DexUI.DEX_NUM_BUTTONS):
            if i==self.dex.selection:
                color=WHITE
            else:
                color=BLACK
            pygame.draw.rect(self.screen,color,(WIDTH//20,HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_SIZE+count*(DexUI.DEX_BUTTON_SIZE+DexUI.BORDER_BTW_BUTTONS),WIDTH//2,DexUI.DEX_BUTTON_SIZE),3)
            draw_text(self.screen,str(i),DexUI.DEX_BUTTON_SIZE//2,color,WIDTH//20+WIDTH//4,HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_SIZE+DexUI.DEX_BUTTON_SIZE//2+count*(DexUI.DEX_BUTTON_SIZE+DexUI.BORDER_BTW_BUTTONS),'center')
            count+=1

        pygame.display.flip()

    def boxes_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b:
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Boxes')])
        draw_text(self.screen,'Boxes',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    def bag_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b:
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Bag')])
        draw_text(self.screen,'Bag',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    def card_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b:
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Card')])
        draw_text(self.screen,'Card',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    def save_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b:
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Save')])
        draw_text(self.screen,'Save',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    def map_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b:
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Map')])
        draw_text(self.screen,'Map',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    def camp_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b:
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Camp')])
        draw_text(self.screen,'Camp',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    def gift_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b:
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Mystery Gift')])
        draw_text(self.screen,'Mystery Gift',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    def vs_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b:
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('VS')])
        draw_text(self.screen,'VS',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    def settings_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b:
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Settings')])
        draw_text(self.screen,'Settings',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    #start screen shown when game is first opened
    def start_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
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
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
        self.screen.fill(BLACK)
        draw_text(self.screen,"GAME OVER",48,WHITE,WIDTH//2,HEIGHT//4,'midtop')
        pygame.display.flip()




