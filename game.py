import pygame
from os import path
from pages import Pages
from settings import *
from sprites import *
from world import World
from menu_ui import MenuUI
from dex_ui import DexUI
from save_ui import SaveUI
from party_ui import PartyUI
from boxes_ui import BoxesUI
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

        #create save ui
        self.save_ui=SaveUI(self)

        #create party ui
        self.party_ui=PartyUI(self)

        #create boxes ui
        self.boxes_ui=BoxesUI(self)

        #create player and world from saved data, if it exists
        self.load()
       
        #for testing catches
        for _ in range(1):
            self.player.catch(Pokemon('Bulbasaur',5))
            self.player.catch(Pokemon('Charmander',5))
            self.player.catch(Pokemon('Squirtle',5))
#
#        print(self.player.party)
#        print(self.player.boxes)
        ######################
        
        self.page=Pages.START
        self.run()

    #main loop calls other methods for specific pages
    def run(self):
        self.playing=True
        while self.playing:
            #keep loop running at correct speed
            self.clock.tick(FPS)
            #go to method based on current page
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
            elif self.page==Pages.PARTY:
                self.party_screen()
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
            elif self.page==Pages.BOXES:
                self.boxes_screen()
            elif self.page==Pages.STATS:
                self.stats_screen()
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
            #if left tiles have left edge off screen or right tiles have right edge off screen when player is still closer to that edge
            self.player.dx=self.player.rect.x-WIDTH//2 #player is moved to middle
            for tile in self.world.all_tiles: #tiles move according to how player would move if it was not in the middle
                tile.move_x(-self.player.dx)
            for sprite in self.all_sprites:
                sprite.rect.x-=self.player.dx
                
        #make sure edge tiles do not move past left/right edges the wrong way
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
        if self.player.rect.y<HEIGHT//2 and self.world.all_tiles[0].rect.y<0 or self.player.rect.y>HEIGHT//2 and self.world.all_tiles[len(self.world.all_tiles)-1].rect.bottom>HEIGHT:
            #if top tiles have top edge off screen or bottom tiles have bottom edge off screen when player is still closer to that edge
            self.player.dy=self.player.rect.y-HEIGHT//2 #player is moved to middle
            for tile in self.world.all_tiles: #tiles move according to how player would move if it was not in the middle
                tile.move_y(-self.player.dy)
            for sprite in self.all_sprites:
                sprite.rect.y-=self.player.dy
             
        #make sure edge tiles do not move past top/bottom edges the wrong way
        if self.world.all_tiles[0].rect.y>0:
            dy=self.world.all_tiles[0].rect.y
            for tile in self.world.all_tiles:
                tile.move_y(-dy)
            for sprite in self.all_sprites:
                sprite.rect.y-=dy
                
        if self.world.all_tiles[len(self.world.all_tiles)-1].rect.bottom<HEIGHT:
            dy=HEIGHT-self.world.all_tiles[len(self.world.all_tiles)-1].rect.bottom
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
                if event.key==pygame.K_a: #A to select button
                    self.page=self.menu.get_page_from_button()
                    if self.page==Pages.PARTY:
                        self.party_ui.reset_buttons()
                if event.key==pygame.K_b: #B to go back to world
                    self.page=Pages.WORLD
                if event.key==pygame.K_r: #R is hotkey to save screen
                    self.page=Pages.SAVE
                if event.key==pygame.K_RIGHT: #arrows to move selection
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
            draw_text(self.screen,MenuUI.MENU_TEXT[i],MenuUI.BUTTON_TEXT_BORDER//2,WHITE,self.menu.buttons[i].rect.x+MenuUI.MENU_BUTTON_SIZE//2,self.menu.buttons[i].rect.y+self.menu.buttons[i].rect.height+MenuUI.BORDER_BTW_BUTTONS//2,'midtop')
            if i==self.menu.selection:
                pygame.draw.rect(self.screen,WHITE,(self.menu.buttons[i].rect.x-MenuUI.BORDER_BTW_BUTTONS//2,self.menu.buttons[i].rect.y-MenuUI.BORDER_BTW_BUTTONS//2,self.menu.buttons[i].rect.width+MenuUI.BORDER_BTW_BUTTONS,self.menu.buttons[i].rect.height+MenuUI.BORDER_BTW_BUTTONS),3)

            #buttons can be pressed to open screens
            if self.menu.buttons[i].draw():
                self.menu.selection=i
                self.page=self.menu.get_page_from_button()

        pygame.display.flip()

    #show screen for player's pokedex
    def dex_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b: #B to go back to menu
                    self.page=Pages.MENU
                if event.key==pygame.K_DOWN: #arrows to move selection
                    self.dex.move_down()
                if event.key==pygame.K_UP:
                    self.dex.move_up()

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Pokedex')])
        pygame.draw.rect(self.screen,WHITE,(WIDTH//20+WIDTH//2+WIDTH//20,HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_HEIGHT,WIDTH*7//20,DexUI.DEX_NUM_BUTTONS*DexUI.DEX_BUTTON_HEIGHT+(DexUI.DEX_NUM_BUTTONS-1)*DexUI.BORDER_BTW_BUTTONS),3)

        #draw buttons
        count=0
        for i in range(self.dex.start,self.dex.start+DexUI.DEX_NUM_BUTTONS):
            if i==self.dex.selection:
                color=WHITE
            else:
                color=BLACK
            pygame.draw.rect(self.screen,color,(WIDTH//20,HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_HEIGHT+count*(DexUI.DEX_BUTTON_HEIGHT+DexUI.BORDER_BTW_BUTTONS),DexUI.DEX_BUTTON_WIDTH,DexUI.DEX_BUTTON_HEIGHT),3)
            draw_text(self.screen,str(i),DexUI.DEX_BUTTON_HEIGHT//2,color,WIDTH//20+WIDTH//4,HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_HEIGHT+DexUI.DEX_BUTTON_HEIGHT//2+count*(DexUI.DEX_BUTTON_HEIGHT+DexUI.BORDER_BTW_BUTTONS),'center')
            count+=1

        pygame.display.flip()

    #show screen for player's pokemon
    def party_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_a: #A to select current selection
                    if self.player.party[self.party_ui.selection] is not None:
                        self.page=Pages.STATS #add attribute to select certain index of party
                if event.key==pygame.K_b: #B to go back to menu
                    self.page=Pages.MENU
                if event.key==pygame.K_r: #R to go to boxes page
                    self.page=Pages.BOXES
                if event.key==pygame.K_DOWN: #arrows to move selection
                    self.party_ui.move_down()
                if event.key==pygame.K_UP:
                    self.party_ui.move_up()

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Boxes')])
        #draw buttons
        for i in range(len(self.party_ui.buttons)):
            self.party_ui.buttons[i].draw()
            if i==self.party_ui.selection:
                pygame.draw.rect(self.screen,WHITE,(self.party_ui.buttons[i].rect.x-PartyUI.BORDER_BTW_BUTTONS//2,self.party_ui.buttons[i].rect.y-PartyUI.BORDER_BTW_BUTTONS//2,self.party_ui.buttons[i].rect.width+PartyUI.BORDER_BTW_BUTTONS,self.party_ui.buttons[i].rect.height+PartyUI.BORDER_BTW_BUTTONS),3)


        pygame.display.flip()

    #show screen for player's items
    def bag_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b: #B to go back to menu
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Bag')])
        draw_text(self.screen,'Bag',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    #show screen to look at player's and others' league cards
    def card_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b: #B to go back to menu
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Card')])
        draw_text(self.screen,'Card',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    #show screen to save game data
    def save_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_a:
                    self.save()
                    self.page=Pages.MENU
                if event.key==pygame.K_b: #B to go back to menu
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Save')])
        pygame.draw.rect(self.screen,WHITE,(self.save_ui.button.rect.x-10,self.save_ui.button.rect.y-10,self.save_ui.button.rect.width+20,self.save_ui.button.rect.height+20),3)
        if self.save_ui.button.draw():
            self.save()
            self.page=Pages.MENU

        pygame.display.flip()

    #show screen for region map and using Fly to get around
    def map_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b: #B to go back to menu
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Map')])
        draw_text(self.screen,'Map',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    #show screen for playing pokemon camp
    def camp_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b: #B to go back to menu
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Camp')])
        draw_text(self.screen,'Camp',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    #show screen for receiving mystery gifts
    def gift_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b: #B to go back to menu
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Mystery Gift')])
        draw_text(self.screen,'Mystery Gift',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    #show screen for searching for VS battles
    def vs_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b: #B to go back to menu
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('VS')])
        draw_text(self.screen,'VS',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    #show screen for changing in game settings
    def settings_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b: #B to go back to menu
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Settings')])
        draw_text(self.screen,'Settings',HEIGHT//10,WHITE,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    #show screen for looking at all pokemon in boxes
    def boxes_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_a: #A to select current button
                    pass
                if event.key==pygame.K_b:
                    #B to go back to party screen if party buttons selected
                    if self.boxes_ui.party_selected and not self.boxes_ui.page_selected:
                        self.page=Pages.PARTY
                    #B to go back to party buttons if box buttons or page button selected
                    elif self.boxes_ui.page_selected or (not self.boxes_ui.party_selected and not self.boxes_ui.page_selected):
                        self.boxes_ui.go_back()
                if event.key==pygame.K_RIGHT:
                    self.boxes_ui.move_right()
                if event.key==pygame.K_LEFT:
                    self.boxes_ui.move_left()
                if event.key==pygame.K_UP:
                    self.boxes_ui.move_up()
                if event.key==pygame.K_DOWN:
                    self.boxes_ui.move_down()

        self.screen.fill(RED)
        self.boxes_ui.page_button.draw()

        for button in self.boxes_ui.party_buttons:
            button.draw()

        for button in self.boxes_ui.box_buttons:
            button.draw()

        #draw rectangle around selected button
        if self.boxes_ui.party_selected and not self.boxes_ui.page_selected:
            button=self.boxes_ui.party_buttons[self.boxes_ui.selection]
            pygame.draw.rect(self.screen,BLUE,(button.rect.x,button.rect.y,button.rect.width,button.rect.height),5)
        elif not self.boxes_ui.party_selected and not self.boxes_ui.page_selected:
            button=self.boxes_ui.box_buttons[self.boxes_ui.selection]
            pygame.draw.rect(self.screen,BLUE,(button.rect.x,button.rect.y,button.rect.width,button.rect.height),5)
        elif self.boxes_ui.page_selected:
            button=self.boxes_ui.page_button
            pygame.draw.rect(self.screen,BLUE,(button.rect.x,button.rect.y,button.rect.width,button.rect.height),5)


        pygame.display.flip()

    #how screen for individual pokemon's stats
    def stats_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b: #B to go back to party
                    self.page=Pages.PARTY #add attribute to know whether to go back to party or boxess

        self.screen.fill(WHITE)
        draw_text(self.screen,'Pokemon',HEIGHT//10,BLACK,WIDTH//2,HEIGHT//2,'center')

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
                if event.key==pygame.K_a: #A to go to world
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

    #save data for persistent data
    def save(self):
        o_f = open('save_data.txt', 'w')
        o_f.write("Player "+str(self.player.rect.x)+" "+str(self.player.rect.y))
        o_f.write('\n')
        o_f.write("World "+str(self.world.all_tiles[0].rect.x)+" "+str(self.world.all_tiles[0].rect.bottom))
        o_f.close()
        
    #load data from save.txt for location of player and first tile in world
    def load(self):
        self.player=None
        self.world=None
        try:
            i_f=open('save_data.txt','r')
            lines=i_f.readlines()
            for i in range(len(lines)):
                line=lines[i].split()
                if line[0]=="Player": #create player
                    self.player=Player_Sprite(self,int(line[1]),int(line[2]),Player())
                elif line[0]=="World": #create world
                    self.world=World(self,TEST_WORLD,int(line[1]),int(line[2]))
            i_f.close()
            
        except:
            #create player from scratch
            if not self.player:
                self.player=Player_Sprite(self,World.TILE_SIZE*2,World.TILE_SIZE*2,Player()) #player starts with topleft at TILE_SIZE*2 x,y

            #create world from scratch
            if not self.world:
                self.world=World(self,TEST_WORLD,0,World.TILE_SIZE) #tiles start with bottomleft at 0,TILE_SIZE



