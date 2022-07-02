import pygame
from settings import *
from sprites import draw_text

class StatsTab:
    TAB_WIDTH=2*WIDTH//40+WIDTH//5 #BoxesUI.LEFT_BORDER*2+BoxesUI.PARTY_BUTTON_WIDTH
    TAB_HEIGHT=HEIGHT*5//6

    def __init__(self, pokemon=None):
        self.pokemon=None

        #create image
        self.image=pygame.Surface((StatsTab.TAB_WIDTH,StatsTab.TAB_HEIGHT))
        self.image.fill(WHITE)
        self.rect=self.image.get_rect()
        self.rect.right=WIDTH
        self.rect.y=(HEIGHT-StatsTab.TAB_HEIGHT)//2
        if self.pokemon is not None:
            self.set_pokemon(pokemon)

    def set_pokemon(self,pokemon):
        self.pokemon=pokemon
        self.image.fill(WHITE)
        draw_text(self.image,pokemon.nickname,StatsTab.TAB_WIDTH//10,BLACK,StatsTab.TAB_WIDTH//2,StatsTab.TAB_WIDTH//20,'midtop')