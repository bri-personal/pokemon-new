import pygame
from settings import *
from sprites import draw_text
from poke_types import PokeTypes
from pokedex import NATURES, ALL_POKEMON_DATA

#tab that shows pokemon data on sidebar in boxes screen
class BoxesStatsTab:
    TAB_WIDTH=2*WIDTH//40+WIDTH//5 #BoxesUI.LEFT_BORDER*2+BoxesUI.PARTY_BUTTON_WIDTH
    TAB_HEIGHT=HEIGHT*5//6

    def __init__(self, pokemon=None):
        self.pokemon=None

        #create image
        self.image=pygame.Surface((BoxesStatsTab.TAB_WIDTH,BoxesStatsTab.TAB_HEIGHT))
        self.image.fill(WHITE)
        self.rect=self.image.get_rect()
        self.rect.right=WIDTH
        self.rect.y=(HEIGHT-BoxesStatsTab.TAB_HEIGHT)//2
        if self.pokemon is not None:
            self.set_pokemon(pokemon)

    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def set_pokemon(self,pokemon):
        self.pokemon=pokemon
        self.image.fill(WHITE)

        #keep track of y of next element on tab and increment with height of each element so if height of one thing changes it doesn't affect rest
        #if changing size of any element, change number added to y as well
        y=0 

        #top bar of tab
        pygame.draw.rect(self.image,LIGHT_GRAY,(0,y,BoxesStatsTab.TAB_WIDTH,BoxesStatsTab.TAB_WIDTH*3//20))
        #draw ball image
        pygame.draw.circle(self.image,BLACK,(BoxesStatsTab.TAB_WIDTH//40+BoxesStatsTab.TAB_WIDTH//20,y+BoxesStatsTab.TAB_WIDTH*3//40),BoxesStatsTab.TAB_WIDTH//20,3)
        #name
        draw_text(self.image,pokemon.nickname,BoxesStatsTab.TAB_WIDTH*3//40,BLACK,BoxesStatsTab.TAB_WIDTH//20+BoxesStatsTab.TAB_WIDTH//10,y+BoxesStatsTab.TAB_WIDTH//30,'topleft')
        #draw gender image
        color=BLUE if self.pokemon.gender=='male' else RED
        pygame.draw.circle(self.image,color,(BoxesStatsTab.TAB_WIDTH-(BoxesStatsTab.TAB_WIDTH//40+BoxesStatsTab.TAB_WIDTH//20),y+BoxesStatsTab.TAB_WIDTH*3//40),BoxesStatsTab.TAB_WIDTH//20,3)
        #level
        draw_text(self.image,"Lv. "+str(pokemon.level),BoxesStatsTab.TAB_WIDTH*3//40,BLACK,BoxesStatsTab.TAB_WIDTH-(BoxesStatsTab.TAB_WIDTH//20+BoxesStatsTab.TAB_WIDTH//10),y+BoxesStatsTab.TAB_WIDTH//30,'topright')

        y+=BoxesStatsTab.TAB_WIDTH*3//20+BoxesStatsTab.TAB_WIDTH//40 #top box height + spacing

        #middle part of tab
        #species/number
        draw_text(self.image,pokemon.species+" - No. "+str(ALL_POKEMON_DATA[self.pokemon.species].number),BoxesStatsTab.TAB_WIDTH*5//80,BLACK,BoxesStatsTab.TAB_WIDTH//40,y,'topleft')

        y+=BoxesStatsTab.TAB_WIDTH//10

        #types
        pygame.draw.rect(self.image,PokeTypes.COLORS[self.pokemon.types[0]],(BoxesStatsTab.TAB_WIDTH//40,y,BoxesStatsTab.TAB_WIDTH//2-BoxesStatsTab.TAB_WIDTH//30,BoxesStatsTab.TAB_WIDTH*3//20))
        pygame.draw.rect(self.image,WHITE,(BoxesStatsTab.TAB_WIDTH//20,y+BoxesStatsTab.TAB_WIDTH//40,BoxesStatsTab.TAB_WIDTH//10,BoxesStatsTab.TAB_WIDTH//10),2)
        draw_text(self.image,self.pokemon.types[0].upper(),BoxesStatsTab.TAB_WIDTH*3//40,WHITE,BoxesStatsTab.TAB_WIDTH//20+BoxesStatsTab.TAB_WIDTH//10+BoxesStatsTab.TAB_WIDTH//40,y+BoxesStatsTab.TAB_WIDTH*3//40,'midleft')
        if self.pokemon.types[1] is not None: #show second type if applicable
            pygame.draw.rect(self.image,PokeTypes.COLORS[self.pokemon.types[1]],(BoxesStatsTab.TAB_WIDTH//50+BoxesStatsTab.TAB_WIDTH//2,y,BoxesStatsTab.TAB_WIDTH//2-BoxesStatsTab.TAB_WIDTH//30,BoxesStatsTab.TAB_WIDTH*3//20))
            pygame.draw.rect(self.image,WHITE,(BoxesStatsTab.TAB_WIDTH//20+BoxesStatsTab.TAB_WIDTH//2,y+BoxesStatsTab.TAB_WIDTH//40,BoxesStatsTab.TAB_WIDTH//10,BoxesStatsTab.TAB_WIDTH//10),2)
            draw_text(self.image,self.pokemon.types[1].upper(),BoxesStatsTab.TAB_WIDTH*3//40,WHITE,BoxesStatsTab.TAB_WIDTH//20+BoxesStatsTab.TAB_WIDTH//10+BoxesStatsTab.TAB_WIDTH//40+BoxesStatsTab.TAB_WIDTH//2,y+BoxesStatsTab.TAB_WIDTH*3//40,'midleft')

        y+=BoxesStatsTab.TAB_WIDTH*3//20+BoxesStatsTab.TAB_WIDTH//20

        pygame.draw.line(self.image,LIGHT_GRAY,(BoxesStatsTab.TAB_WIDTH//40,y),(BoxesStatsTab.TAB_WIDTH-BoxesStatsTab.TAB_WIDTH//40,y),1)

        y+=BoxesStatsTab.TAB_WIDTH//40

        #stats
        stat_text=['HP:         ', 'ATK:       ', 'DEF:       ', 'SPATK:   ', 'SPDEF:  ', 'SPD:       ']
        for i in range(len(stat_text)):
            text=stat_text[i]+str(self.pokemon.stats[i])
            if NATURES[self.pokemon.nature][i]==1.1:
                color=BLUE
                text+=' ↑'
            elif NATURES[self.pokemon.nature][i]==0.9:
                color=RED
                text+=' ↓'
            else:
                color=BLACK
            text+=' ('+self.get_IV_level(self.pokemon.ivs[i])+')'
            draw_text(self.image,text,BoxesStatsTab.TAB_WIDTH*5//80,color,BoxesStatsTab.TAB_WIDTH//40,y,'topleft')
            y+=BoxesStatsTab.TAB_WIDTH*5//80+BoxesStatsTab.TAB_WIDTH//40

        y+=BoxesStatsTab.TAB_WIDTH//40

        #nature, item, ability
        draw_text(self.image,self.pokemon.nature+' by nature!',BoxesStatsTab.TAB_WIDTH*5//80,BLACK,BoxesStatsTab.TAB_WIDTH//40,y,'topleft')

        y+=BoxesStatsTab.TAB_WIDTH*5//80+BoxesStatsTab.TAB_WIDTH//40

        draw_text(self.image,'Held item: '+('---' if self.pokemon.item is None else self.pokemon.item),BoxesStatsTab.TAB_WIDTH*5//80,BLACK,BoxesStatsTab.TAB_WIDTH//40,y,'topleft')

        y+=BoxesStatsTab.TAB_WIDTH*5//80+BoxesStatsTab.TAB_WIDTH//40

        draw_text(self.image,'Ability: '+(self.pokemon.ability[3:] if self.pokemon.ability[:3]=='ha_' else self.pokemon.ability),BoxesStatsTab.TAB_WIDTH*5//80,BLACK,BoxesStatsTab.TAB_WIDTH//40,y,'topleft')

        y+=BoxesStatsTab.TAB_WIDTH*5//80+BoxesStatsTab.TAB_WIDTH//20

        pygame.draw.line(self.image,LIGHT_GRAY,(BoxesStatsTab.TAB_WIDTH//40,y),(BoxesStatsTab.TAB_WIDTH-BoxesStatsTab.TAB_WIDTH//40,y),1)

        y+=BoxesStatsTab.TAB_WIDTH//40

        #moves
        draw_text(self.image,'Moves:',BoxesStatsTab.TAB_WIDTH*5//80,BLACK,BoxesStatsTab.TAB_WIDTH//40,y,'topleft')

        y+=BoxesStatsTab.TAB_WIDTH*5//80+BoxesStatsTab.TAB_WIDTH//40
        
        for i in range(4):
            if i<len(self.pokemon.moves):
                pygame.draw.rect(self.image,PokeTypes.COLORS[self.pokemon.moves[i].type],(BoxesStatsTab.TAB_WIDTH//40,y,BoxesStatsTab.TAB_WIDTH-BoxesStatsTab.TAB_WIDTH//20,BoxesStatsTab.TAB_WIDTH*3//20))
                pygame.draw.rect(self.image,WHITE,(BoxesStatsTab.TAB_WIDTH//20,y+BoxesStatsTab.TAB_WIDTH//40,BoxesStatsTab.TAB_WIDTH//10,BoxesStatsTab.TAB_WIDTH//10),2)
                draw_text(self.image,self.pokemon.moves[i].name,BoxesStatsTab.TAB_WIDTH*3//40,WHITE,BoxesStatsTab.TAB_WIDTH//20+BoxesStatsTab.TAB_WIDTH//10+BoxesStatsTab.TAB_WIDTH//40,y+BoxesStatsTab.TAB_WIDTH*3//40,'midleft')
            y+=BoxesStatsTab.TAB_WIDTH//20+BoxesStatsTab.TAB_WIDTH//10+BoxesStatsTab.TAB_WIDTH//40

        #markings
        for i in range(6):
            pygame.draw.rect(self.image,LIGHT_GRAY,(BoxesStatsTab.TAB_WIDTH//2-3*BoxesStatsTab.TAB_WIDTH//20-5*BoxesStatsTab.TAB_WIDTH//40//2+i*(BoxesStatsTab.TAB_WIDTH//20+BoxesStatsTab.TAB_WIDTH//40),y,BoxesStatsTab.TAB_WIDTH//20,BoxesStatsTab.TAB_WIDTH//20))

    #return string for IV level of stat
    def get_IV_level(self,iv: int):
        if iv==0:
            return 'No Good'
        elif iv<=10:
            return 'Decent'
        elif iv<=20:
            return 'Pretty Good'
        elif iv<=29:
            return 'Very Good'
        elif iv==30:
            return 'Fantastic'
        else:
            return 'Best'
