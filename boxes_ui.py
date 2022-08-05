import pygame
from settings import *
from sprites import Button, draw_text
from boxes_stats_tab import BoxesStatsTab
from boxes_menu_tab import BoxesMenuTab
from player import Player
from poke_types import PokeTypes

class BoxesUI:
    NUM_BOXES=Player.NUM_BOXES
    LEFT_BORDER=WIDTH//40

    NUM_PARTY_BUTTONS=Player.MAX_PARTY_SIZE
    PARTY_BUTTON_WIDTH=WIDTH//5
    PARTY_BUTTON_HEIGHT=HEIGHT//9

    NUM_BOX_BUTTONS=Player.BOX_SIZE
    NUM_BOX_BUTTON_ROWS=5 #must be even factor of NUM_BOX_BUTTONS
    NUM_BOX_BUTTON_COLS=NUM_BOX_BUTTONS//NUM_BOX_BUTTON_ROWS
    BOX_BUTTON_SIZE=HEIGHT//10
    BORDER_BTW_BUTTONS=HEIGHT//50

    def __init__(self,game):
        self.game=game

        self.selection=0 #selection of buttons on current box page
        self.party_selected=True #True if selection refers to party buttons, false if selection refers to box buttons
        self.page_index=0 #index of this box in all box pages, max is BoxesUI.NUM_BOXES-1
        self.page_selected=False #True if page button is selected, false otherwise

        #create page button
        img=pygame.Surface((3*BoxesUI.BOX_BUTTON_SIZE+3*BoxesUI.BORDER_BTW_BUTTONS,BoxesUI.BOX_BUTTON_SIZE//2))
        img.fill(LIGHT_GRAY)
        draw_text(img,"Box "+str(self.page_index+1),BoxesUI.BOX_BUTTON_SIZE//3,BLACK,(BoxesUI.BOX_BUTTON_SIZE+BoxesUI.BORDER_BTW_BUTTONS)*3//2,BoxesUI.BOX_BUTTON_SIZE//4,'center')
        self.page_button=Button(self.game,BoxesUI.LEFT_BORDER*3+BoxesUI.PARTY_BUTTON_WIDTH+BoxesUI.BOX_BUTTON_SIZE//2+BoxesUI.BOX_BUTTON_SIZE*5//2+BoxesUI.BORDER_BTW_BUTTONS*3,HEIGHT//2-BoxesUI.BORDER_BTW_BUTTONS*5//2-3*BoxesUI.PARTY_BUTTON_HEIGHT+BoxesUI.BOX_BUTTON_SIZE//2,img)

        #create party buttons
        self.party_buttons=[]
        for i in range(BoxesUI.NUM_PARTY_BUTTONS):
            img=pygame.Surface((BoxesUI.PARTY_BUTTON_WIDTH,BoxesUI.PARTY_BUTTON_HEIGHT))
            img.fill(WHITE)
            self.party_buttons.append(Button(self.game,BoxesUI.LEFT_BORDER+BoxesUI.PARTY_BUTTON_WIDTH//2,HEIGHT//2-BoxesUI.BORDER_BTW_BUTTONS*5//2-3*BoxesUI.PARTY_BUTTON_HEIGHT+BoxesUI.BOX_BUTTON_SIZE//2+i*(BoxesUI.PARTY_BUTTON_HEIGHT+BoxesUI.BORDER_BTW_BUTTONS),img))

        #create box buttons
        self.box_buttons=[]
        for i in range(BoxesUI.NUM_BOX_BUTTON_ROWS):
            for j in range(BoxesUI.NUM_BOX_BUTTON_COLS):
                img=pygame.Surface((BoxesUI.BOX_BUTTON_SIZE,BoxesUI.BOX_BUTTON_SIZE))
                img.fill(LIGHT_GRAY)
                self.box_buttons.append(Button(self.game,BoxesUI.LEFT_BORDER*3+BoxesUI.PARTY_BUTTON_WIDTH+BoxesUI.BOX_BUTTON_SIZE//2+j*(BoxesUI.BOX_BUTTON_SIZE+BoxesUI.BORDER_BTW_BUTTONS),HEIGHT//2-BoxesUI.BORDER_BTW_BUTTONS*5//2-3*BoxesUI.PARTY_BUTTON_HEIGHT+(i+1)*(BoxesUI.BOX_BUTTON_SIZE+BoxesUI.BORDER_BTW_BUTTONS),img))
        
        #create pokemon view stats tab
        self.stats_tab=BoxesStatsTab()
        self.show_stats_tab=False #determines whether tab or pokemon image is shown

        #create boxes menu tab
        self.menu_tab=BoxesMenuTab()
        self.show_menu_tab=False #determines whether tab is shown or not

    def move_right(self):
        if not self.show_menu_tab:
            if self.party_selected and not self.page_selected: #if in party, go to page button if index is 0 or go to box buttons otherwise
                if self.selection==0:
                    self.page_selected=True
                else:
                    self.party_selected=False
                    self.selection=(self.selection-1)*BoxesUI.NUM_BOX_BUTTON_COLS
                    if self.game.player.boxes[self.page_index][self.selection] is not None:
                        self.stats_tab.set_pokemon(self.game.player.boxes[self.page_index][self.selection])
                self.reset_box_buttons(True)
                self.reset_party_buttons(False)
            elif not self.party_selected and not self.page_selected: #if in box, go to adjacent button and wrap around in box if at edge
                self.selection=self.selection//BoxesUI.NUM_BOX_BUTTON_COLS*BoxesUI.NUM_BOX_BUTTON_COLS+(self.selection+1)%BoxesUI.NUM_BOX_BUTTON_COLS
                if self.game.player.boxes[self.page_index][self.selection] is not None:
                    self.stats_tab.set_pokemon(self.game.player.boxes[self.page_index][self.selection])
            elif self.page_selected: #if in page button, go to next page
                self.page_index=(self.page_index+1)%BoxesUI.NUM_BOXES
                self.reset_box_buttons(True)

    def move_left(self):
        if not self.show_menu_tab:
            if not self.party_selected and not self.page_selected: #if in box, go to adjacent button and wrap around in box if at edge
                self.selection=self.selection//BoxesUI.NUM_BOX_BUTTON_COLS*BoxesUI.NUM_BOX_BUTTON_COLS+(self.selection-1)%BoxesUI.NUM_BOX_BUTTON_COLS
                if self.game.player.boxes[self.page_index][self.selection] is not None:
                    self.stats_tab.set_pokemon(self.game.player.boxes[self.page_index][self.selection])
            elif self.page_selected: #if in page button, go to previous page
                self.page_index=(self.page_index-1)%BoxesUI.NUM_BOXES
                self.reset_box_buttons(WHITE)
            #if in party, do nothing

    def move_up(self):
        if self.show_menu_tab:
            pass
        else:
            if self.party_selected and not self.page_selected: #if in party, go up and wrap around at top edge
                self.selection=(self.selection-1)%BoxesUI.NUM_PARTY_BUTTONS
                if self.game.player.party[self.selection] is not None:
                    self.stats_tab.set_pokemon(self.game.player.party[self.selection])
            elif not self.party_selected and not self.page_selected: #if in box, go to page button if at top row or row above otherwise
                if self.selection<BoxesUI.NUM_BOX_BUTTON_COLS:
                    self.page_selected=True
                else:
                    self.selection=(self.selection-BoxesUI.NUM_BOX_BUTTON_COLS)%BoxesUI.NUM_BOX_BUTTONS
                    if self.game.player.boxes[self.page_index][self.selection] is not None:
                        self.stats_tab.set_pokemon(self.game.player.boxes[self.page_index][self.selection])
            #do nothing if on page button
            
    def move_down(self):
        if self.show_menu_tab:
            pass
        else:
            if self.party_selected and not self.page_selected: #if in party, go down and wrap around at bottom edge
                self.selection=(self.selection+1)%BoxesUI.NUM_PARTY_BUTTONS
                if self.game.player.party[self.selection] is not None:
                    self.stats_tab.set_pokemon(self.game.player.party[self.selection])
            elif not self.party_selected and not self.page_selected: #if in box, go to row below and wrap around at bottom edge
                self.selection=(self.selection+BoxesUI.NUM_BOX_BUTTON_COLS)%BoxesUI.NUM_BOX_BUTTONS
                if self.game.player.boxes[self.page_index][self.selection] is not None:
                    self.stats_tab.set_pokemon(self.game.player.boxes[self.page_index][self.selection])
            elif self.page_selected: #if in page button, go to middle of top row of box
                if self.party_selected:
                    self.selection=BoxesUI.NUM_BOX_BUTTON_COLS//2-1
                self.page_selected=False
                self.party_selected=False
                if self.game.player.boxes[self.page_index][self.selection] is not None:
                    self.stats_tab.set_pokemon(self.game.player.boxes[self.page_index][self.selection])

    #when B is pressed and boxes or page button is selected, go back to party buttons selection
    def go_back(self):
        if self.page_selected:
            self.selection=0
        else: #party_selected must be false for this method to be called
            self.selection=self.selection//BoxesUI.NUM_BOX_BUTTON_COLS+1
        self.page_selected=False
        self.party_selected=True
        self.reset_box_buttons(False)
        self.reset_party_buttons(True)
        if self.game.player.party[self.selection] is not None:
            self.stats_tab.set_pokemon(self.game.player.party[self.selection])

    #when A is pressed on pokemon box button, activate menu tab
    def set_menu_tab(self):
        self.show_menu_tab=True
        orientation=''

        #if party selected, tab goes on topright if upper half or bottomright if lower half
        if self.party_selected:
            if self.selection<BoxesUI.NUM_PARTY_BUTTONS//2:
                y=self.party_buttons[self.selection].rect.top
                orientation+='top'
            else:
                y=self.party_buttons[self.selection].rect.bottom
                orientation+='bottom'
            x=self.party_buttons[self.selection].rect.right
            orientation+='right'
        #if boxes selected, tab goes on right of left half of boxes, left on right half of boxes, top on first half of rows, bottom of second half of rows
        else:
            if self.selection//BoxesUI.NUM_BOX_BUTTON_COLS<BoxesUI.NUM_BOX_BUTTON_ROWS//2+1:
                y=self.box_buttons[self.selection].rect.y
                orientation+='top'
            else:
                y=self.box_buttons[self.selection].rect.bottom
                orientation+='bottom'

            if self.selection%BoxesUI.NUM_BOX_BUTTON_COLS<BoxesUI.NUM_BOX_BUTTON_COLS//2:
                x=self.box_buttons[self.selection].rect.right
                orientation+='right'
            else:
                x=self.box_buttons[self.selection].rect.left
                orientation+='left'

        self.menu_tab.set_loc(x,y,orientation)
        self.menu_tab.selection=0
        self.menu_tab.update()

    #gray out party buttons when moving selection to box buttons
    def reset_party_buttons(self,active: bool):
        for i in range(len(self.party_buttons)):
            self.party_buttons[i].image.fill(WHITE if active else LIGHT_GRAY)
            if self.game.player.party[i] is not None:
                img=pygame.Surface((BoxesUI.PARTY_BUTTON_HEIGHT*3//4,BoxesUI.PARTY_BUTTON_HEIGHT*3//4))
                img.fill(PokeTypes.COLORS[self.game.player.party[i].types[0]])
                pygame.draw.rect(img,BLACK,img.get_rect(),3)
                self.party_buttons[i].image.blit(img,(BoxesUI.PARTY_BUTTON_HEIGHT//8,BoxesUI.PARTY_BUTTON_HEIGHT//8))
                draw_text(self.party_buttons[i].image,self.game.player.party[i].nickname,BoxesUI.PARTY_BUTTON_HEIGHT//3,BLACK,BoxesUI.PARTY_BUTTON_HEIGHT,BoxesUI.PARTY_BUTTON_HEIGHT//8,'topleft')

    #gray out box buttons and page button when moving selection to party buttons
    def reset_box_buttons(self,active: bool):
        for i in range(len(self.box_buttons)):
            self.box_buttons[i].image.fill(WHITE if active else LIGHT_GRAY)
            if self.game.player.boxes[self.page_index][i%BoxesUI.NUM_BOX_BUTTONS] is not None:
                img=pygame.Surface((BoxesUI.BOX_BUTTON_SIZE*3//4,BoxesUI.BOX_BUTTON_SIZE*3//4))
                img.fill(PokeTypes.COLORS[self.game.player.boxes[self.page_index][i%BoxesUI.NUM_BOX_BUTTONS].types[0]])
                pygame.draw.rect(img,BLACK,img.get_rect(),3)
                self.box_buttons[i].image.blit(img,(BoxesUI.BOX_BUTTON_SIZE//8,BoxesUI.BOX_BUTTON_SIZE//8))
                
        self.page_button.image.fill(WHITE if active else LIGHT_GRAY)
        draw_text(self.page_button.image,"Box "+str(self.page_index+1),BoxesUI.BOX_BUTTON_SIZE//3,BLACK,(BoxesUI.BOX_BUTTON_SIZE+BoxesUI.BORDER_BTW_BUTTONS)*3//2,BoxesUI.BOX_BUTTON_SIZE//4,'center')
