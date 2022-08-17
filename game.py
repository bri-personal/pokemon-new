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
from dex_info_ui import DexInfoUI
from player import Player
from pokemon import Pokemon
from poke_types import PokeTypes
from pokedex import ALL_POKEMON_DATA, ALL_POKEMON
     
#Use keys A, B, Q, R, X, arrows

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

        #create player and world from saved data, if it exists
        self.load()
       
        #for testing catches
        for _ in range(13):
            self.player.catch(Pokemon('Bulbasaur',6))
            self.player.catch(Pokemon('Charmander',6))
            self.player.catch(Pokemon('Squirtle',6))
#
#        print(self.player.party)
#        print(self.player.boxes)
        ######################

        #create menu
        self.menu=MenuUI(self)

        #create dex ui
        self.dex_selection=0 #selected index on pokedex for dex ui and dex info ui
        self.dex_ui=DexUI(self)
        self.dex_info_ui=DexInfoUI(self)

        #create save ui
        self.save_ui=SaveUI(self)

        #create party ui
        self.party_ui=PartyUI(self)

        #create boxes ui
        self.boxes_ui=BoxesUI(self)
        
        self.page=Pages.START
        self.prev_page=Pages.START
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
            elif self.page==Pages.DEX_INFO:
                self.dex_info_screen()
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
                    self.prev_page=self.page
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
                    self.prev_page=self.page
                    self.page=self.menu.get_page_from_button()
                    if self.page==Pages.PARTY:
                        self.party_ui.reset_buttons()
                if event.key==pygame.K_b: #B to go back to world
                    self.prev_page=self.page
                    self.page=Pages.WORLD
                if event.key==pygame.K_r: #R is hotkey to save screen
                    self.prev_page=self.page
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
            self.menu.buttons[i].draw()
            draw_text(self.screen,MenuUI.MENU_TEXT[i],MenuUI.BUTTON_TEXT_BORDER//2,WHITE,self.menu.buttons[i].rect.x+MenuUI.MENU_BUTTON_SIZE//2,self.menu.buttons[i].rect.y+self.menu.buttons[i].rect.height+MenuUI.BORDER_BTW_BUTTONS//2,'midtop')
            if i==self.menu.selection:
                pygame.draw.rect(self.screen,BLUE,(self.menu.buttons[i].rect.x-1,self.menu.buttons[i].rect.y-1,self.menu.buttons[i].rect.width+2,self.menu.buttons[i].rect.height+2),4)

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
                if event.key==pygame.K_a:
                    if self.player.dex[ALL_POKEMON[self.dex_selection]][0]>0:
                        self.prev_page=self.page
                        self.page=Pages.DEX_INFO
                if event.key==pygame.K_b: #B to go back to menu
                    self.prev_page=self.page
                    self.page=Pages.MENU
                if event.key==pygame.K_DOWN: #arrows to move selection
                    self.dex_ui.move_down()
                if event.key==pygame.K_UP:
                    self.dex_ui.move_up()

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Pokedex')])

        #draw image box
        self.dex_ui.image_box.draw()

        #draw buttons
        for i in range(self.dex_ui.start,min(self.dex_ui.start+6,len(self.dex_ui.dex_buttons))):
            self.dex_ui.dex_buttons[i].draw()

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
                        self.prev_page=self.page
                        self.page=Pages.STATS #add attribute to select certain index of party
                if event.key==pygame.K_b: #B to go back to menu
                    self.prev_page=self.page
                    self.page=Pages.MENU
                if event.key==pygame.K_r: #R to go to boxes page
                    self.go_to_boxes()
                if event.key==pygame.K_DOWN: #arrows to move selection
                    self.party_ui.move_down()
                if event.key==pygame.K_UP:
                    self.party_ui.move_up()

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Boxes')])

        #draw buttons
        for i in range(len(self.party_ui.buttons)):
            self.party_ui.buttons[i].draw()
            if i==self.party_ui.selection:
                pygame.draw.rect(self.screen,BLUE,(self.party_ui.buttons[i].rect.x-1,self.party_ui.buttons[i].rect.y-1,self.party_ui.buttons[i].rect.width+2,self.party_ui.buttons[i].rect.height+2),4)

        if self.player.party[self.party_ui.selection] is not None:
            pygame.draw.rect(self.screen,PokeTypes.COLORS[self.player.party[self.party_ui.selection].types[0]],(WIDTH*5//8,(HEIGHT-WIDTH*3//10)//2,WIDTH*3//10,WIDTH*3//10))
            pygame.draw.rect(self.screen,BLACK if ALL_POKEMON_DATA[self.player.party[self.party_ui.selection].species].types[1] is None else PokeTypes.COLORS[ALL_POKEMON_DATA[self.player.party[self.party_ui.selection].species].types[1]],(WIDTH*5//8,(HEIGHT-WIDTH*3//10)//2,WIDTH*3//10,WIDTH*3//10),3)

        self.party_ui.boxes_button.draw()

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
                    #go back to prev page
                    temp=self.prev_page
                    self.prev_page=self.page
                    self.page=temp

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
                    self.prev_page=self.page
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
                if event.key==pygame.K_a: #A to save game and go back to menu
                    self.save()
                    self.prev_page=self.page
                    self.page=Pages.MENU
                if event.key==pygame.K_b: #B to go back to menu
                    self.prev_page=self.page
                    self.page=Pages.MENU

        self.screen.fill(MenuUI.MENU_COLORS[MenuUI.MENU_TEXT.index('Save')])
        draw_text(self.screen,'Save Your Progress',HEIGHT//10,WHITE,self.save_ui.button.rect.centerx,HEIGHT//6,'midtop')

        #draw pokemon images for current party
        for i in range(len(self.player.party)):
            if self.player.party[i] is not None:
                pygame.draw.rect(self.screen,PokeTypes.COLORS[self.player.party[i].types[0]],(self.save_ui.button.rect.centerx-3*HEIGHT//10-5*HEIGHT//50//2+i*(HEIGHT//10+HEIGHT//50),HEIGHT//6+HEIGHT//10+HEIGHT//20,HEIGHT//10,HEIGHT//10))
                pygame.draw.rect(self.screen,BLACK,(self.save_ui.button.rect.centerx-3*HEIGHT//10-5*HEIGHT//50//2+i*(HEIGHT//10+HEIGHT//50),HEIGHT//6+HEIGHT//10+HEIGHT//20,HEIGHT//10,HEIGHT//10),3)
        
        self.save_ui.button.draw()
        
        pygame.draw.rect(self.screen,BLUE,(self.save_ui.button.rect.x-1,self.save_ui.button.rect.y-1,self.save_ui.button.rect.width+2,self.save_ui.button.rect.height+2),4)

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
                    self.prev_page=self.page
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
                    self.prev_page=self.page
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
                    self.prev_page=self.page
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
                    self.prev_page=self.page
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
                    self.prev_page=self.page
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
                    if not self.boxes_ui.page_selected and ((self.boxes_ui.party_selected and self.player.party[self.boxes_ui.selection] is not None) or (not self.boxes_ui.party_selected and self.player.boxes[self.boxes_ui.page_index][self.boxes_ui.selection] is not None)):
                        #if in boxes or party, enable menu tab if not already enabled
                        if not self.boxes_ui.show_menu_tab:
                            self.boxes_ui.set_menu_tab()
                        #if menu tab is enabled go to current selection on it
                        else:
                            new_page=self.boxes_ui.menu_tab.get_page_from_selection()
                            #if going to other page, set boxes as prev page
                            if new_page==Pages.STATS or new_page==Pages.BAG:
                                self.prev_page=self.page
                            #if staying on boxes page, hide menu tab
                            elif new_page==Pages.BOXES:
                                self.boxes_ui.show_menu_tab=False
                                if self.boxes_ui.menu_tab.selection==3: #release
                                    if self.boxes_ui.party_selected: #release from party
                                        self.player.release_party(self.boxes_ui.selection)
                                        self.boxes_ui.reset_party_buttons(True)
                                        self.boxes_ui.reset_box_buttons(False)
                                        #if releasing caused new pokemon to move into selected button, show new pokemon
                                        if self.player.party[self.boxes_ui.selection] is not None:
                                            self.boxes_ui.stats_tab.set_pokemon(self.player.party[self.boxes_ui.selection])
                                    else: #release from boxes
                                        self.player.release_boxes(self.boxes_ui.page_index,self.boxes_ui.selection)
                                        self.boxes_ui.reset_party_buttons(False)
                                        self.boxes_ui.reset_box_buttons(True)
                            self.page=new_page
                if event.key==pygame.K_b:
                    #B to go back to party screen if party buttons selected
                    if self.boxes_ui.party_selected and not self.boxes_ui.page_selected:
                        if self.boxes_ui.show_menu_tab:
                            self.boxes_ui.show_menu_tab=False
                        else:
                            self.prev_page=self.page
                            self.page=Pages.PARTY
                    #B to disable boxes menu tab if it is on
                    elif not self.boxes_ui.page_selected and not self.boxes_ui.party_selected and self.boxes_ui.show_menu_tab:
                        self.boxes_ui.show_menu_tab=False
                    #B to go back to party buttons if box buttons or page button selected
                    elif self.boxes_ui.page_selected or (not self.boxes_ui.party_selected and not self.boxes_ui.page_selected):
                        self.boxes_ui.go_back()
                if event.key==pygame.K_EQUALS:
                    #switch stats tab on/off
                    self.boxes_ui.show_stats_tab=not self.boxes_ui.show_stats_tab
                if event.key==pygame.K_RIGHT:
                    self.boxes_ui.move_right()
                if event.key==pygame.K_LEFT:
                    self.boxes_ui.move_left()
                if event.key==pygame.K_UP:
                    #if menu tab active, go up/down on it
                    if self.boxes_ui.show_menu_tab:
                        self.boxes_ui.menu_tab.go_up()
                    #otherwise, go up/down in boxes
                    else:
                        self.boxes_ui.move_up()
                if event.key==pygame.K_DOWN:
                    #if menu tab active, go up/down on it
                    if self.boxes_ui.show_menu_tab:
                        self.boxes_ui.menu_tab.go_down()
                    #otherwise, go up/down in boxes
                    else:
                        self.boxes_ui.move_down()

        self.screen.fill(RED)
        pygame.draw.line(self.screen,WHITE,(BoxesUI.LEFT_BORDER*2+BoxesUI.PARTY_BUTTON_WIDTH,0),(BoxesUI.LEFT_BORDER*2+BoxesUI.PARTY_BUTTON_WIDTH,HEIGHT),3)
        draw_text(self.screen,"PARTY",BoxesUI.PARTY_BUTTON_HEIGHT*3//4,WHITE,BoxesUI.LEFT_BORDER+BoxesUI.PARTY_BUTTON_WIDTH//2,HEIGHT//2-BoxesUI.BORDER_BTW_BUTTONS*5//2-3*BoxesUI.PARTY_BUTTON_HEIGHT+BoxesUI.BOX_BUTTON_SIZE//2-BoxesUI.PARTY_BUTTON_HEIGHT,'midtop')
        draw_text(self.screen,"BOXES",BoxesUI.PARTY_BUTTON_HEIGHT*3//4,WHITE,BoxesUI.LEFT_BORDER*3+BoxesUI.PARTY_BUTTON_WIDTH+BoxesUI.BOX_BUTTON_SIZE//2+BoxesUI.BOX_BUTTON_SIZE*5//2+BoxesUI.BORDER_BTW_BUTTONS*3,HEIGHT//2-BoxesUI.BORDER_BTW_BUTTONS*5//2-3*BoxesUI.PARTY_BUTTON_HEIGHT+BoxesUI.BOX_BUTTON_SIZE//2-BoxesUI.PARTY_BUTTON_HEIGHT,'midtop')

        self.boxes_ui.page_button.draw()

        for button in self.boxes_ui.party_buttons:
            button.draw()

        for button in self.boxes_ui.box_buttons:
            button.draw()

        #draw rectangle around selected button
        if self.boxes_ui.party_selected and not self.boxes_ui.page_selected:
            button=self.boxes_ui.party_buttons[self.boxes_ui.selection]
            pygame.draw.rect(self.screen,BLUE,(button.rect.x-1,button.rect.y-1,button.rect.width+2,button.rect.height+2),4)
        elif not self.boxes_ui.party_selected and not self.boxes_ui.page_selected:
            button=self.boxes_ui.box_buttons[self.boxes_ui.selection]
            pygame.draw.rect(self.screen,BLUE,(button.rect.x-1,button.rect.y-1,button.rect.width+2,button.rect.height+2),4)
        elif self.boxes_ui.page_selected:
            button=self.boxes_ui.page_button
            pygame.draw.rect(self.screen,BLUE,(button.rect.x-1,button.rect.y-1,button.rect.width+2,button.rect.height+2),4)

        #show stats tab if pokemon is selected
        if not self.boxes_ui.page_selected and not ((self.boxes_ui.party_selected and self.player.party[self.boxes_ui.selection] is None) or (not self.boxes_ui.party_selected and self.player.boxes[self.boxes_ui.page_index][self.boxes_ui.selection] is None)):
            if self.boxes_ui.show_stats_tab:
                self.boxes_ui.stats_tab.draw(self.screen)
            else:
                if self.boxes_ui.party_selected:
                    pygame.draw.rect(self.screen,PokeTypes.COLORS[self.player.party[self.boxes_ui.selection].types[0]],(WIDTH-HEIGHT*5//16,HEIGHT*3//8,HEIGHT//4,HEIGHT//4))
                    pygame.draw.rect(self.screen,BLACK if ALL_POKEMON_DATA[self.player.party[self.boxes_ui.selection].species].types[1] is None else PokeTypes.COLORS[ALL_POKEMON_DATA[self.player.party[self.boxes_ui.selection].species].types[1]],(WIDTH-HEIGHT*5//16,HEIGHT*3//8,HEIGHT//4,HEIGHT//4),3)
                else:
                    pygame.draw.rect(self.screen,PokeTypes.COLORS[self.player.boxes[self.boxes_ui.page_index][self.boxes_ui.selection%BoxesUI.NUM_BOX_BUTTONS].types[0]],(WIDTH-HEIGHT*5//16,HEIGHT*3//8,HEIGHT//4,HEIGHT//4))
                    pygame.draw.rect(self.screen,BLACK if ALL_POKEMON_DATA[self.player.boxes[self.boxes_ui.page_index][self.boxes_ui.selection].species].types[1] is None else PokeTypes.COLORS[ALL_POKEMON_DATA[self.player.boxes[self.boxes_ui.page_index][self.boxes_ui.selection].species].types[1]],(WIDTH-HEIGHT*5//16,HEIGHT*3//8,HEIGHT//4,HEIGHT//4),3)

        #show menu tab
        if self.boxes_ui.show_menu_tab:
            self.boxes_ui.menu_tab.draw(self.screen)

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
                if event.key==pygame.K_b: #B to go back to party or boxes, whichever was previous page
                    temp=self.prev_page
                    self.prev_page=self.page
                    self.page=temp

        self.screen.fill(WHITE)
        draw_text(self.screen,'Pokemon',HEIGHT//10,BLACK,WIDTH//2,HEIGHT//2,'center')

        pygame.display.flip()

    #screen to show info of certain pokemon in dex
    def dex_info_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_q:
                    self.playing=False
                    self.running=False
                if event.key==pygame.K_b: #B to go back to dex screen
                    self.prev_page=self.page
                    self.page=Pages.DEX

        self.screen.fill(RED)
        draw_text(self.screen,ALL_POKEMON[self.dex_selection],HEIGHT//10,WHITE,WIDTH*7//10,HEIGHT//6,'midtop')
        self.dex_info_ui.image_box.draw()

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
                    self.prev_page=self.page
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

    #opens boxes screen from whichever screen was previous (party, bag, etc) and resets state so it looks correct on opening
    def go_to_boxes(self):
        self.prev_page=self.page
        self.page=Pages.BOXES
        self.boxes_ui.setup()



