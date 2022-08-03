from settings import *
from sprites import draw_text
import pygame


class BoxesMenuTab:
    TAB_WIDTH=2*(HEIGHT//10+HEIGHT//50) #2*(BoxesUI.BOX_BUTTON_SIZE+BoxesUI.BORDER_BTW_BUTTONS)
    TAB_HEIGHT=3*HEIGHT//10+2*HEIGHT//50 #3*BoxesUI.BOX_BUTTON_SIZE+2*BoxesUI.BORDER_BTW_BUTTONS

    def __init__(self):
        self.image=pygame.Surface((BoxesMenuTab.TAB_WIDTH,BoxesMenuTab.TAB_HEIGHT))
        self.rect=self.image.get_rect()
        
        #items to display on menu
        self.items=['View Stats','Held Item','Markings','Back']
        self.selection=0 #index of items selected

    #set location of tab based on provided orientation
    def set_loc(self,x,y,orientation):
        self.rect.x=x if 'right' in orientation else x-BoxesMenuTab.TAB_WIDTH
        self.rect.y=y if 'top' in orientation else y-BoxesMenuTab.TAB_HEIGHT

    #reset image so current selection is shown in different color
    def update(self):
        self.image.fill(WHITE)
        pygame.draw.rect(self.image,BLACK,(0,0,self.rect.width,self.rect.height),3)
        for i in range(len(self.items)):
            draw_text(self.image,self.items[i],BoxesMenuTab.TAB_HEIGHT//6,BLUE if i==self.selection else BLACK,BoxesMenuTab.TAB_WIDTH//2,i*BoxesMenuTab.TAB_HEIGHT//4,'midtop')

    #draw tab on screen
    def draw(self,surface):
        surface.blit(self.image,self.rect)

    #move selection down on menu tab
    def go_down(self):
        self.selection=(self.selection+1)%len(self.items)
        self.update()

    #move selection up on menu tab
    def go_up(self):
        self.selection=(self.selection-1)%len(self.items)
        self.update()