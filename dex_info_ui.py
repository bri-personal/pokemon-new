from settings import *
from sprites import Button, draw_text
from pokedex import ALL_POKEMON, ALL_POKEMON_DATA
from poke_types import PokeTypes
import pygame

class DexInfoUI:

    IMAGE_BOX_WIDTH=WIDTH*7//20
    IMAGE_BOX_HEIGHT=HEIGHT*17//20

    TEXT_BOX_WIDTH=WIDTH//2
    TEXT_BOX_HEIGHT=HEIGHT//3

    def __init__(self,game):
        self.game=game

        #box to show selected pokemon in dex
        img=pygame.Surface((DexInfoUI.IMAGE_BOX_WIDTH,DexInfoUI.IMAGE_BOX_HEIGHT))
        self.image_box=Button(self.game,WIDTH-(WIDTH//20+WIDTH//2+WIDTH//20)-DexInfoUI.IMAGE_BOX_WIDTH//2,(HEIGHT-DexInfoUI.IMAGE_BOX_HEIGHT)//2,img)
        self.reset_image_box()

        #text box
        img=pygame.Surface((DexInfoUI.TEXT_BOX_WIDTH,DexInfoUI.TEXT_BOX_HEIGHT))
        self.text_box=Button(self.game,WIDTH-DexInfoUI.TEXT_BOX_WIDTH//2-WIDTH//20,HEIGHT//2,img)
        self.reset_text_box()

    #change image shown in image box to reflect current selection
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

    #change text shown in text box to reflect current selection
    def reset_text_box(self):
        self.text_box.image.fill(RED)

        #draw lines of text
        y=self.text_box.rect.height//20
        lines=self.get_text_lines(ALL_POKEMON_DATA[ALL_POKEMON[self.game.dex_selection]].pokedex_entry,50)
        for line in lines:
            draw_text(self.text_box.image,line,self.text_box.rect.width//20,WHITE,self.text_box.rect.width//2,y,'midtop')
            y+=self.text_box.rect.width//20

        pygame.draw.rect(self.text_box.image,WHITE,(0,0,self.text_box.rect.width,self.text_box.rect.height),3)

    #split string into lines of text based on punctuation and char limit
    def get_text_lines(self, text:str, limit: int):
        text_lines=[]
        line=''
        word=''
        while len(text)>0:
            if text[0]==' ':
                if len(line)+len(word)+1<limit:
                    word+=text[0]
                    text=text[1:]
                    line+=word
                    word=''
                elif len(line)+len(word)<limit:
                    text=text[1:]
                    line+=word
                    word=''
                    text_lines.append(line)
                    line=''
                else:
                    text_lines.append(line)
                    word+=text[0]
                    text=text[1:]
                    line=word
                    word=''
            elif text[0]=='.' or text[0]==',':
                if len(line)+len(word)+1<limit:
                    word+=text[0]
                    text=text[1:]
                    line+=word
                    word=''
                else:
                    text_lines.append(line)
                    word+=text[0]
                    text=text[1:]
                    line=word
                    word=''
            else:
                word+=text[0]
                text=text[1:]
        if word!='':
            line+=word
        if line!='':
            text_lines.append(line)
            
        return text_lines

    #resets state when going from dex screen to dex info screen to reflect currently selected pokemon in pokedex
    def setup(self):
        self.reset_image_box()
        self.reset_text_box()