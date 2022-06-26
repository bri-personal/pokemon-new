import pygame
from settings import *

class DexUI:
    #dex menu data
    DEX_NUM_BUTTONS=6
    DEX_BUTTON_SIZE=HEIGHT//8
    BORDER_BTW_BUTTONS=HEIGHT//32

    def __init__(self,game):
        self.game=game

        #indices for which Pokemon are shown on the dex page and which is selected
        self.start=0
        self.selection=0

    def move_down(self):
        if self.selection<12-1: #replace 12 with length of dex
            self.selection+=1
            if self.selection>=self.start+DexUI.DEX_NUM_BUTTONS:
                self.start+=1
        else:
            self.start=0
            self.selection=0

    def move_up(self):
        if self.selection>0:
            self.selection-=1
            if self.selection<self.start:
                self.start-=1
        else:
            self.start=12-DexUI.DEX_NUM_BUTTONS #replace 12 with length of dex
            self.selection=12-1 #replace 12 with length of dex




