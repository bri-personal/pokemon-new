import pygame
from settings import *
from sprites import Button

class PartyUI:
    NUM_BUTTONS=6
    PARTY_BUTTON_WIDTH=WIDTH//2
    PARTY_BUTTON_HEIGHT=HEIGHT//8
    BORDER_BTW_BUTTONS=HEIGHT//32

    def __init__(self,game):
        self.game=game

        self.selection=0

        self.buttons=[]
        for i in range(PartyUI.NUM_BUTTONS):
            img=pygame.Surface((PartyUI.PARTY_BUTTON_WIDTH,PartyUI.PARTY_BUTTON_HEIGHT))
            img.fill(WHITE)
            self.buttons.append(Button(self.game,WIDTH//20+PartyUI.PARTY_BUTTON_WIDTH//2,HEIGHT//2-PartyUI.BORDER_BTW_BUTTONS*5//2-3*PartyUI.PARTY_BUTTON_HEIGHT+i*(PartyUI.PARTY_BUTTON_HEIGHT+PartyUI.BORDER_BTW_BUTTONS),img))

    def move_down(self):
        self.selection=(self.selection+1)%PartyUI.NUM_BUTTONS

    def move_up(self):
        self.selection=(self.selection-1)%PartyUI.NUM_BUTTONS


