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

        #top bar of tab
        pygame.draw.rect(self.image,LIGHT_GRAY,(0,0,StatsTab.TAB_WIDTH,StatsTab.TAB_WIDTH*3//20))
        #draw ball image
        pygame.draw.circle(self.image,BLACK,(StatsTab.TAB_WIDTH//40+StatsTab.TAB_WIDTH//20,StatsTab.TAB_WIDTH*3//40),StatsTab.TAB_WIDTH//20,3)
        #name
        draw_text(self.image,pokemon.nickname,StatsTab.TAB_WIDTH*3//40,BLACK,StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//10,StatsTab.TAB_WIDTH//30,'topleft')
        #draw gender image
        pygame.draw.circle(self.image,BLUE,(StatsTab.TAB_WIDTH-(StatsTab.TAB_WIDTH//40+StatsTab.TAB_WIDTH//20),StatsTab.TAB_WIDTH*3//40),StatsTab.TAB_WIDTH//20,3)
        #level
        draw_text(self.image,"Lv. "+str(pokemon.level),StatsTab.TAB_WIDTH*3//40,BLACK,StatsTab.TAB_WIDTH-(StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//10),StatsTab.TAB_WIDTH//30,'topright')

        #middle part of tab
        #species/number
        draw_text(self.image,pokemon.species+" - No. "+"0",StatsTab.TAB_WIDTH//20,BLACK,StatsTab.TAB_WIDTH//40,StatsTab.TAB_WIDTH*3//20+StatsTab.TAB_WIDTH//40,'topleft')
        #types
        pygame.draw.rect(self.image,GRAY,(StatsTab.TAB_WIDTH//40,StatsTab.TAB_WIDTH*3//20+StatsTab.TAB_WIDTH*5//40,StatsTab.TAB_WIDTH//2-StatsTab.TAB_WIDTH//20,StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//10))
        pygame.draw.rect(self.image,WHITE,(StatsTab.TAB_WIDTH//20,StatsTab.TAB_WIDTH*3//20+StatsTab.TAB_WIDTH*3//20,StatsTab.TAB_WIDTH//10,StatsTab.TAB_WIDTH//10),3)
        draw_text(self.image,"Type 1",StatsTab.TAB_WIDTH*3//40,WHITE,StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//10+StatsTab.TAB_WIDTH//40,StatsTab.TAB_WIDTH*3//20+StatsTab.TAB_WIDTH*8//40,'midleft')
        if True:
            pygame.draw.rect(self.image,GRAY,(StatsTab.TAB_WIDTH//40+StatsTab.TAB_WIDTH//2,StatsTab.TAB_WIDTH*3//20+StatsTab.TAB_WIDTH*5//40,StatsTab.TAB_WIDTH//2-StatsTab.TAB_WIDTH//20,StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//10))
            pygame.draw.rect(self.image,WHITE,(StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//2,StatsTab.TAB_WIDTH*3//20+StatsTab.TAB_WIDTH*3//20,StatsTab.TAB_WIDTH//10,StatsTab.TAB_WIDTH//10),3)
            draw_text(self.image,"Type 2",StatsTab.TAB_WIDTH*3//40,WHITE,StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//10+StatsTab.TAB_WIDTH//40+StatsTab.TAB_WIDTH//2,StatsTab.TAB_WIDTH*3//20+StatsTab.TAB_WIDTH*8//40,'midleft')
