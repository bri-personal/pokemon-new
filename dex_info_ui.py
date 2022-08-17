from settings import *
from sprites import Button, draw_text
from pokedex import ALL_POKEMON, ALL_POKEMON_DATA
from poke_types import PokeTypes
import pygame

class DexInfoUI:

    IMAGE_BOX_WIDTH=WIDTH*7//20
    IMAGE_BOX_HEIGHT=HEIGHT*17//20

    def __init__(self,game):
        self.game=game

        #box to show selected pokemon in dex
        img=pygame.Surface((DexInfoUI.IMAGE_BOX_WIDTH,DexInfoUI.IMAGE_BOX_HEIGHT))
        self.image_box=Button(self.game,WIDTH-(WIDTH//20+WIDTH//2+WIDTH//20)-WIDTH*7//20//2,(HEIGHT-DexInfoUI.IMAGE_BOX_HEIGHT)//2,img)
        self.reset_image_box()

    #change image shown in image box
    def reset_image_box(self):
        self.image_box.image.fill(RED)
        pygame.draw.rect(self.image_box.image,WHITE,(0,0,self.image_box.rect.width,self.image_box.rect.height),3)

        #image inside image box
        if self.game.player.dex[ALL_POKEMON[self.game.dex_selection]][0]>0:
            pygame.draw.rect(self.image_box.image,PokeTypes.COLORS[ALL_POKEMON_DATA[ALL_POKEMON[self.game.dex_selection]].types[0]],(self.image_box.rect.width//4,self.image_box.rect.height//2-self.image_box.rect.width//4,self.image_box.rect.width//2,self.image_box.rect.width//2))
            pygame.draw.rect(self.image_box.image,BLACK if ALL_POKEMON_DATA[ALL_POKEMON[self.game.dex_selection]].types[1] is None else PokeTypes.COLORS[ALL_POKEMON_DATA[ALL_POKEMON[self.game.dex_selection]].types[1]],(self.image_box.rect.width//4,self.image_box.rect.height//2-self.image_box.rect.width//4,self.image_box.rect.width//2,self.image_box.rect.width//2),3)
            draw_text(self.image_box.image,str(self.game.dex_selection+1),DexInfoUI.IMAGE_BOX_WIDTH//5,WHITE,self.image_box.rect.width//2,self.image_box.rect.height//2,'center')
        else:
            draw_text(self.image_box.image,'???',DexInfoUI.IMAGE_BOX_WIDTH//5,WHITE,self.image_box.rect.width//2,self.image_box.rect.height//2,'center')
