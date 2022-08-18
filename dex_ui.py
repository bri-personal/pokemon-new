from xml.etree.ElementInclude import include
import pygame
from settings import *
from sprites import Button, draw_text
from pokedex import ALL_POKEMON_DATA, ALL_POKEMON
from poke_types import PokeTypes

class DexUI:
    #dex menu data
    DEX_NUM_BUTTONS=6
    DEX_BUTTON_WIDTH=WIDTH//2
    DEX_BUTTON_HEIGHT=HEIGHT//8
    BORDER_BTW_BUTTONS=HEIGHT//32

    IMAGE_BOX_WIDTH=WIDTH*7//20
    IMAGE_BOX_HEIGHT=DEX_NUM_BUTTONS*DEX_BUTTON_HEIGHT+(DEX_NUM_BUTTONS-1)*BORDER_BTW_BUTTONS

    def __init__(self,game):
        self.game=game

        #indices for which Pokemon are shown on the dex page and which is selected
        self.start=0
        while self.game.dex_selection<len(ALL_POKEMON) and self.game.player.dex[ALL_POKEMON[self.game.dex_selection]][0]==0:
            self.game.dex_selection+=1
        if self.game.dex_selection>=len(ALL_POKEMON):
            self.game.dex_selection=0

        #dex buttons
        self.dex_buttons=[]
        for i in range(len(ALL_POKEMON)):
            img=pygame.Surface((DexUI.DEX_BUTTON_WIDTH,DexUI.DEX_BUTTON_HEIGHT))
            self.dex_buttons.append(Button(self.game,WIDTH-WIDTH//20-DexUI.DEX_BUTTON_WIDTH//2,HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_HEIGHT+i*(DexUI.DEX_BUTTON_HEIGHT+DexUI.BORDER_BTW_BUTTONS),img))
            self.recolor_dex_buttons()
            #change y of buttons to not go so far off screen if they don't need to be shown

        #box to show selected pokemon in dex from button
        img=pygame.Surface((DexUI.IMAGE_BOX_WIDTH,DexUI.IMAGE_BOX_HEIGHT))
        self.image_box=Button(self.game,WIDTH-(WIDTH//20+WIDTH//2+WIDTH//20)-DexUI.IMAGE_BOX_WIDTH//2,HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_HEIGHT,img)
        self.reset_image_box()

    #highlight selected button
    def recolor_dex_buttons(self):
        for i in range(len(self.dex_buttons)): #when pokedex has enough items, change back
            #if pokemon at this index has been caught
            if self.game.player.dex[ALL_POKEMON[i]][1]>0:
                color=GREEN
            #if pokemon at this index has not been caught but has been seen
            elif self.game.player.dex[ALL_POKEMON[i]][0]>0:
                color=YELLOW
            #pokemon has not been caught or seen
            else:
                color=BLACK

            self.dex_buttons[i].image.fill(RED)
            pygame.draw.rect(self.dex_buttons[i].image,WHITE if i==self.game.dex_selection else BLACK,(0,0,self.dex_buttons[i].rect.width,self.dex_buttons[i].rect.height),3)
            draw_text(self.dex_buttons[i].image,str(i+1)+' - '+(ALL_POKEMON[i] if self.game.player.dex[ALL_POKEMON[i]][0]>0 else '???'),DexUI.DEX_BUTTON_HEIGHT//2,color,self.dex_buttons[i].rect.width//2,self.dex_buttons[i].rect.height//2,'center')

    #change image shown in image box
    def reset_image_box(self):
        self.image_box.image.fill(RED)
        pygame.draw.rect(self.image_box.image,WHITE,(0,0,self.image_box.rect.width,self.image_box.rect.height),3)

        #image inside image box
        if self.game.player.dex[ALL_POKEMON[self.game.dex_selection]][0]>0:
            pygame.draw.rect(self.image_box.image,PokeTypes.COLORS[ALL_POKEMON_DATA[ALL_POKEMON[self.game.dex_selection]].types[0]],(self.image_box.rect.width//4,self.image_box.rect.height//2-self.image_box.rect.width//4,self.image_box.rect.width//2,self.image_box.rect.width//2))
            pygame.draw.rect(self.image_box.image,BLACK if ALL_POKEMON_DATA[ALL_POKEMON[self.game.dex_selection]].types[1] is None else PokeTypes.COLORS[ALL_POKEMON_DATA[ALL_POKEMON[self.game.dex_selection]].types[1]],(self.image_box.rect.width//4,self.image_box.rect.height//2-self.image_box.rect.width//4,self.image_box.rect.width//2,self.image_box.rect.width//2),3)
            draw_text(self.image_box.image,str(self.game.dex_selection+1),DexUI.IMAGE_BOX_WIDTH//5,WHITE,self.image_box.rect.width//2,self.image_box.rect.height//2,'center')
        else:
            draw_text(self.image_box.image,'???',DexUI.IMAGE_BOX_WIDTH//5,WHITE,self.image_box.rect.width//2,self.image_box.rect.height//2,'center')

    #move dex buttons down
    def move_down(self):
        if self.game.dex_selection<len(ALL_POKEMON)-1:
            self.game.dex_selection+=1
            if self.game.dex_selection>=self.start+DexUI.DEX_NUM_BUTTONS:
                self.start+=1
                for button in self.dex_buttons:
                    button.rect.y-=DexUI.DEX_BUTTON_HEIGHT+DexUI.BORDER_BTW_BUTTONS
        else:
            self.start=0
            self.game.dex_selection=0
            for i in range(len(self.dex_buttons)):
                self.dex_buttons[i].rect.y=HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_HEIGHT+i*(DexUI.DEX_BUTTON_HEIGHT+DexUI.BORDER_BTW_BUTTONS)    
        self.recolor_dex_buttons()
        self.reset_image_box()

    #move dex buttons up
    def move_up(self):
        if self.game.dex_selection>0:
            self.game.dex_selection-=1
            if self.game.dex_selection<self.start:
                self.start-=1
                for button in self.dex_buttons:
                    button.rect.y+=DexUI.DEX_BUTTON_HEIGHT+DexUI.BORDER_BTW_BUTTONS
        else:
            self.start=len(ALL_POKEMON)-DexUI.DEX_NUM_BUTTONS
            self.game.dex_selection=len(ALL_POKEMON)-1
            for i in range(len(self.dex_buttons)):
                self.dex_buttons[i].rect.y=HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_HEIGHT+(i-(len(self.dex_buttons)-DexUI.DEX_NUM_BUTTONS))*(DexUI.DEX_BUTTON_HEIGHT+DexUI.BORDER_BTW_BUTTONS)
        self.recolor_dex_buttons()
        self.reset_image_box()

    #move dex buttons down, jumping so new start is one after current last button
    def jump_down(self):
        inc=min(DexUI.DEX_NUM_BUTTONS,len(self.dex_buttons)-DexUI.DEX_NUM_BUTTONS-self.start)
        self.start+=inc
        self.game.dex_selection=min(self.game.dex_selection+inc,len(self.dex_buttons)-1)
        for button in self.dex_buttons:
             button.rect.y-=inc*(DexUI.DEX_BUTTON_HEIGHT+DexUI.BORDER_BTW_BUTTONS)
        self.recolor_dex_buttons()
        self.reset_image_box()




