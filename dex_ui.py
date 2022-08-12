import pygame
from settings import *
from sprites import Button, draw_text

class DexUI:
    #dex menu data
    DEX_NUM_BUTTONS=6
    DEX_BUTTON_WIDTH=WIDTH//2
    DEX_BUTTON_HEIGHT=HEIGHT//8
    BORDER_BTW_BUTTONS=HEIGHT//32

    def __init__(self,game):
        self.game=game

        #indices for which Pokemon are shown on the dex page and which is selected
        self.start=0
        self.selection=0

        #dex buttons
        self.dex_buttons=[]
        for i in range(12): #replace 12 with length of dex
            img=pygame.Surface((DexUI.DEX_BUTTON_WIDTH,DexUI.DEX_BUTTON_HEIGHT))
            self.dex_buttons.append(Button(self.game,WIDTH-WIDTH//20-DexUI.DEX_BUTTON_WIDTH//2,HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_HEIGHT+i*(DexUI.DEX_BUTTON_HEIGHT+DexUI.BORDER_BTW_BUTTONS),img))
            self.recolor_dex_buttons()
            #change y of buttons to not go so far off screen if they don't need to be shown

        #box to show selected pokemon in dex from button
        img=pygame.Surface((WIDTH*7//20,DexUI.DEX_NUM_BUTTONS*DexUI.DEX_BUTTON_HEIGHT+(DexUI.DEX_NUM_BUTTONS-1)*DexUI.BORDER_BTW_BUTTONS))
        img.fill(RED)
        pygame.draw.rect(img,WHITE,(0,0,img.get_rect().width,img.get_rect().height),3)
        self.image_box=Button(self.game,WIDTH-(WIDTH//20+WIDTH//2+WIDTH//20)-WIDTH*7//20//2,HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_HEIGHT,img)

    #highlight selected button
    def recolor_dex_buttons(self):
        for i in range(len(self.dex_buttons)):
            self.dex_buttons[i].image.fill(RED)
            pygame.draw.rect(self.dex_buttons[i].image,WHITE if i==self.selection else BLACK,(0,0,self.dex_buttons[i].rect.width,self.dex_buttons[i].rect.height),3)
            draw_text(self.dex_buttons[i].image,str(i),DexUI.DEX_BUTTON_HEIGHT//2,WHITE if i==self.selection else BLACK,self.dex_buttons[i].rect.width//2,self.dex_buttons[i].rect.height//2,'center')

    #move dex buttons down
    def move_down(self):
        if self.selection<12-1: #replace 12 with length of dex
            self.selection+=1
            if self.selection>=self.start+DexUI.DEX_NUM_BUTTONS:
                self.start+=1
                for button in self.dex_buttons:
                    button.rect.y-=DexUI.DEX_BUTTON_HEIGHT+DexUI.BORDER_BTW_BUTTONS
        else:
            self.start=0
            self.selection=0
            for i in range(len(self.dex_buttons)):
                self.dex_buttons[i].rect.y=HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_HEIGHT+i*(DexUI.DEX_BUTTON_HEIGHT+DexUI.BORDER_BTW_BUTTONS)
        self.recolor_dex_buttons()

    #move dex buttons up
    def move_up(self):
        if self.selection>0:
            self.selection-=1
            if self.selection<self.start:
                self.start-=1
                for button in self.dex_buttons:
                    button.rect.y+=DexUI.DEX_BUTTON_HEIGHT+DexUI.BORDER_BTW_BUTTONS
        else:
            self.start=12-DexUI.DEX_NUM_BUTTONS #replace 12 with length of dex
            self.selection=12-1 #replace 12 with length of dex
            for i in range(len(self.dex_buttons)): #fix
                self.dex_buttons[i].rect.y=HEIGHT//2-DexUI.BORDER_BTW_BUTTONS*5//2-3*DexUI.DEX_BUTTON_HEIGHT+(i-DexUI.DEX_NUM_BUTTONS)*(DexUI.DEX_BUTTON_HEIGHT+DexUI.BORDER_BTW_BUTTONS)
        self.recolor_dex_buttons()




