from pstats import Stats
import pygame
from settings import *
from sprites import draw_text

#tab that shows pokemon data on sidebar in boxes screen
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

        #keep track of y of next element on tab and increment with height of each element so if height of one thing changes it doesn't affect rest
        #if changing size of any element, change number added to y as well
        y=0 

        #top bar of tab
        pygame.draw.rect(self.image,LIGHT_GRAY,(0,y,StatsTab.TAB_WIDTH,StatsTab.TAB_WIDTH*3//20))
        #draw ball image
        pygame.draw.circle(self.image,BLACK,(StatsTab.TAB_WIDTH//40+StatsTab.TAB_WIDTH//20,y+StatsTab.TAB_WIDTH*3//40),StatsTab.TAB_WIDTH//20,3)
        #name
        draw_text(self.image,pokemon.nickname,StatsTab.TAB_WIDTH*3//40,BLACK,StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//10,y+StatsTab.TAB_WIDTH//30,'topleft')
        #draw gender image
        color=BLUE if self.pokemon.gender=='male' else RED
        pygame.draw.circle(self.image,color,(StatsTab.TAB_WIDTH-(StatsTab.TAB_WIDTH//40+StatsTab.TAB_WIDTH//20),y+StatsTab.TAB_WIDTH*3//40),StatsTab.TAB_WIDTH//20,3)
        #level
        draw_text(self.image,"Lv. "+str(pokemon.level),StatsTab.TAB_WIDTH*3//40,BLACK,StatsTab.TAB_WIDTH-(StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//10),y+StatsTab.TAB_WIDTH//30,'topright')

        y+=StatsTab.TAB_WIDTH*3//20+StatsTab.TAB_WIDTH//40 #top box height + spacing

        #middle part of tab
        #species/number
        draw_text(self.image,pokemon.species+" - No. "+"0",StatsTab.TAB_WIDTH*5//80,BLACK,StatsTab.TAB_WIDTH//40,y,'topleft')

        y+=StatsTab.TAB_WIDTH//10

        #types
        pygame.draw.rect(self.image,GRAY,(StatsTab.TAB_WIDTH//40,y,StatsTab.TAB_WIDTH//2-StatsTab.TAB_WIDTH//20,StatsTab.TAB_WIDTH*3//20))
        pygame.draw.rect(self.image,WHITE,(StatsTab.TAB_WIDTH//20,y+StatsTab.TAB_WIDTH//40,StatsTab.TAB_WIDTH//10,StatsTab.TAB_WIDTH//10),3)
        draw_text(self.image,"Type 1",StatsTab.TAB_WIDTH*3//40,WHITE,StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//10+StatsTab.TAB_WIDTH//40,y+StatsTab.TAB_WIDTH*3//40,'midleft')
        if True: #show second type if applicable
            pygame.draw.rect(self.image,GRAY,(StatsTab.TAB_WIDTH//40+StatsTab.TAB_WIDTH//2,y,StatsTab.TAB_WIDTH//2-StatsTab.TAB_WIDTH//20,StatsTab.TAB_WIDTH*3//20))
            pygame.draw.rect(self.image,WHITE,(StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//2,y+StatsTab.TAB_WIDTH//40,StatsTab.TAB_WIDTH//10,StatsTab.TAB_WIDTH//10),3)
            draw_text(self.image,"Type 2",StatsTab.TAB_WIDTH*3//40,WHITE,StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//10+StatsTab.TAB_WIDTH//40+StatsTab.TAB_WIDTH//2,y+StatsTab.TAB_WIDTH*3//40,'midleft')

        y+=StatsTab.TAB_WIDTH*3//20+StatsTab.TAB_WIDTH//20

        pygame.draw.line(self.image,LIGHT_GRAY,(StatsTab.TAB_WIDTH//40,y),(StatsTab.TAB_WIDTH-StatsTab.TAB_WIDTH//40,y),1)

        y+=StatsTab.TAB_WIDTH//40

        #stats and other info
        stat_text=['HP:         ', 'ATK:       ', 'DEF:       ', 'SPATK:   ', 'SPDEF:  ', 'SPD:       ']
        for i in range(len(stat_text)):
            draw_text(self.image,stat_text[i]+str(self.pokemon.stats[i]),StatsTab.TAB_WIDTH*5//80,BLACK,StatsTab.TAB_WIDTH//40,y,'topleft')
            y+=StatsTab.TAB_WIDTH*5//80+StatsTab.TAB_WIDTH//40

        y+=StatsTab.TAB_WIDTH//40

        draw_text(self.image,self.pokemon.nature+' by nature',StatsTab.TAB_WIDTH*5//80,BLACK,StatsTab.TAB_WIDTH//40,y,'topleft')

        y+=StatsTab.TAB_WIDTH*5//80+StatsTab.TAB_WIDTH//40

        draw_text(self.image,'Held item: '+self.pokemon.item,StatsTab.TAB_WIDTH*5//80,BLACK,StatsTab.TAB_WIDTH//40,y,'topleft')

        y+=StatsTab.TAB_WIDTH*5//80+StatsTab.TAB_WIDTH//40

        draw_text(self.image,'Ability: '+self.pokemon.ability,StatsTab.TAB_WIDTH*5//80,BLACK,StatsTab.TAB_WIDTH//40,y,'topleft')

        y+=StatsTab.TAB_WIDTH*5//80+StatsTab.TAB_WIDTH//20

        pygame.draw.line(self.image,LIGHT_GRAY,(StatsTab.TAB_WIDTH//40,y),(StatsTab.TAB_WIDTH-StatsTab.TAB_WIDTH//40,y),1)

        y+=StatsTab.TAB_WIDTH//40

        #moves
        draw_text(self.image,'Moves:',StatsTab.TAB_WIDTH*5//80,BLACK,StatsTab.TAB_WIDTH//40,y,'topleft')

        y+=StatsTab.TAB_WIDTH*5//80+StatsTab.TAB_WIDTH//40
        
        for i in range(4):
            if i<len(self.pokemon.moves):
                pygame.draw.rect(self.image,GRAY,(StatsTab.TAB_WIDTH//40,y,StatsTab.TAB_WIDTH-StatsTab.TAB_WIDTH//20,StatsTab.TAB_WIDTH*3//20))
                pygame.draw.rect(self.image,WHITE,(StatsTab.TAB_WIDTH//20,y+StatsTab.TAB_WIDTH//40,StatsTab.TAB_WIDTH//10,StatsTab.TAB_WIDTH//10),3)
                draw_text(self.image,self.pokemon.moves[i],StatsTab.TAB_WIDTH*3//40,WHITE,StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//10+StatsTab.TAB_WIDTH//40,y+StatsTab.TAB_WIDTH*3//40,'midleft')
            y+=StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//10+StatsTab.TAB_WIDTH//40

        #markings
        for i in range(6):
            pygame.draw.rect(self.image,LIGHT_GRAY,(StatsTab.TAB_WIDTH//2-3*StatsTab.TAB_WIDTH//20-5*StatsTab.TAB_WIDTH//40//2+i*(StatsTab.TAB_WIDTH//20+StatsTab.TAB_WIDTH//40),y,StatsTab.TAB_WIDTH//20,StatsTab.TAB_WIDTH//20))

        