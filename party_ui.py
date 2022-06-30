import pygame
from settings import *
from sprites import Button, draw_text
from player import Player

class PartyUI:
    NUM_BUTTONS=Player.MAX_PARTY_SIZE
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

    #move menu selection down
    def move_down(self):
        self.selection=(self.selection+1)%PartyUI.NUM_BUTTONS

    #move menu selection up
    def move_up(self):
        self.selection=(self.selection-1)%PartyUI.NUM_BUTTONS

    #sets button images to reflect player's current party
    def reset_buttons(self):
        for i in range(len(self.buttons)):
            self.buttons[i].image.fill(WHITE)
            if self.game.player.party[i] is not None:
                img=pygame.Surface((PartyUI.PARTY_BUTTON_HEIGHT*3//4,PartyUI.PARTY_BUTTON_HEIGHT*3//4))
                img.fill(BLACK)
                self.buttons[i].image.blit(img,(PartyUI.PARTY_BUTTON_HEIGHT//8,PartyUI.PARTY_BUTTON_HEIGHT//8))
                draw_text(self.buttons[i].image,self.game.player.party[i].nickname,PartyUI.PARTY_BUTTON_HEIGHT//3,BLACK,PartyUI.PARTY_BUTTON_HEIGHT,PartyUI.PARTY_BUTTON_HEIGHT//8,'topleft')


