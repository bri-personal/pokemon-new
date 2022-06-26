import pygame
from settings import *
from sprites import draw_text, Button
from world import World

class SaveUI:
    SAVE_BUTTON_WIDTH=WIDTH//2
    SAVE_BUTTON_HEIGHT=HEIGHT//8

    def __init__(self,game):
        self.game=game

        #save button
        img=pygame.Surface((SaveUI.SAVE_BUTTON_WIDTH,SaveUI.SAVE_BUTTON_HEIGHT))
        img.fill(WHITE)
        draw_text(img,'SAVE',SaveUI.SAVE_BUTTON_HEIGHT*2//3,BLACK,SaveUI.SAVE_BUTTON_WIDTH//2,SaveUI.SAVE_BUTTON_HEIGHT//2,'center')
        self.button=Button(self.game,WIDTH*2//3,HEIGHT//2,img)


