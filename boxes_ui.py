import pygame
from settings import *
from sprites import Button, draw_text
from player import Player

class BoxesUI:
    NUM_BOXES=Player.NUM_BOXES

    NUM_PARTY_BUTTONS=Player.MAX_PARTY_SIZE
    PARTY_BUTTON_WIDTH=WIDTH//4
    PARTY_BUTTON_HEIGHT=HEIGHT//8

    NUM_BOX_BUTTONS=Player.BOX_SIZE
    NUM_BOX_BUTTON_ROWS=5 #must be even factor of NUM_BOX_BUTTONS
    NUM_BOX_BUTTON_COLS=NUM_BOX_BUTTONS//NUM_BOX_BUTTON_ROWS
    BOX_BUTTON_SIZE=HEIGHT//8
    BORDER_BTW_BUTTONS=HEIGHT//32

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
        self.page_button=Button(self.game,WIDTH//20+BoxesUI.PARTY_BUTTON_WIDTH+BoxesUI.BORDER_BTW_BUTTONS+BoxesUI.BOX_BUTTON_SIZE//2+BoxesUI.BOX_BUTTON_SIZE*5//2+3*BoxesUI.BORDER_BTW_BUTTONS,HEIGHT//2-BoxesUI.BORDER_BTW_BUTTONS*5//2-3*BoxesUI.PARTY_BUTTON_HEIGHT+BoxesUI.BOX_BUTTON_SIZE//2,img)

        #create party buttons
        self.party_buttons=[]
        for i in range(BoxesUI.NUM_PARTY_BUTTONS):
            img=pygame.Surface((BoxesUI.PARTY_BUTTON_WIDTH,BoxesUI.PARTY_BUTTON_HEIGHT))
            img.fill(WHITE)
            self.party_buttons.append(Button(self.game,WIDTH//20+BoxesUI.PARTY_BUTTON_WIDTH//2,HEIGHT//2-BoxesUI.BORDER_BTW_BUTTONS*5//2-3*BoxesUI.PARTY_BUTTON_HEIGHT+i*(BoxesUI.PARTY_BUTTON_HEIGHT+BoxesUI.BORDER_BTW_BUTTONS),img))

        #create box buttons
        self.box_buttons=[]
        for i in range(BoxesUI.NUM_BOX_BUTTON_ROWS):
            for j in range(BoxesUI.NUM_BOX_BUTTON_COLS):
                img=pygame.Surface((BoxesUI.BOX_BUTTON_SIZE,BoxesUI.BOX_BUTTON_SIZE))
                img.fill(LIGHT_GRAY)
                self.box_buttons.append(Button(self.game,WIDTH//20+BoxesUI.PARTY_BUTTON_WIDTH+BoxesUI.BORDER_BTW_BUTTONS+BoxesUI.BOX_BUTTON_SIZE//2+j*(BoxesUI.BOX_BUTTON_SIZE+BoxesUI.BORDER_BTW_BUTTONS),HEIGHT//2-BoxesUI.BORDER_BTW_BUTTONS*5//2-3*BoxesUI.PARTY_BUTTON_HEIGHT+(i+1)*(BoxesUI.BOX_BUTTON_SIZE+BoxesUI.BORDER_BTW_BUTTONS),img))

    def move_right(self):
        if self.party_selected and not self.page_selected: #if in party, go to page button if index is 0 or go to box buttons otherwise
            if self.selection==0:
                self.page_selected=True
            else:
                self.party_selected=False
                self.selection=(self.selection-1)*BoxesUI.NUM_BOX_BUTTON_COLS
            self.reset_box_buttons(WHITE)
            self.reset_party_buttons(LIGHT_GRAY)
        elif not self.party_selected and not self.page_selected: #if in box, go to adjacent button and wrap around in box if at edge
            self.selection=self.selection//BoxesUI.NUM_BOX_BUTTON_COLS*BoxesUI.NUM_BOX_BUTTON_COLS+(self.selection+1)%BoxesUI.NUM_BOX_BUTTON_COLS
        elif self.page_selected: #if in page button, go to next page
            self.page_index=(self.page_index+1)%BoxesUI.NUM_BOXES
            self.reset_box_buttons(WHITE)

    def move_left(self):
        if not self.party_selected and not self.page_selected: #if in box, go to adjacent button and wrap around in box if at edge
            self.selection=self.selection//BoxesUI.NUM_BOX_BUTTON_COLS*BoxesUI.NUM_BOX_BUTTON_COLS+(self.selection-1)%BoxesUI.NUM_BOX_BUTTON_COLS
        elif self.page_selected: #if in page button, go to previous page
            self.page_index=(self.page_index-1)%BoxesUI.NUM_BOXES
            self.reset_box_buttons(WHITE)
        #if in party, do nothing

    def move_up(self):
        if self.party_selected and not self.page_selected: #if in party, go up and wrap around at top edge
            self.selection=(self.selection-1)%BoxesUI.NUM_PARTY_BUTTONS
        elif not self.party_selected and not self.page_selected: #if in box, go to page button if at top row or row above otherwise
            if self.selection<BoxesUI.NUM_BOX_BUTTON_COLS:
                self.page_selected=True
            else:
                self.selection=(self.selection-BoxesUI.NUM_BOX_BUTTON_COLS)%BoxesUI.NUM_BOX_BUTTONS
        #do nothing if on page button
            
    def move_down(self):
        if self.party_selected and not self.page_selected: #if in party, go down and wrap around at bottom edge
            self.selection=(self.selection+1)%BoxesUI.NUM_PARTY_BUTTONS
        elif not self.party_selected and not self.page_selected: #if in box, go to row below and wrap around at bottom edge
            self.selection=(self.selection+BoxesUI.NUM_BOX_BUTTON_COLS)%BoxesUI.NUM_BOX_BUTTONS
        elif self.page_selected: #if in page button, go to middle of top row of box
            if self.party_selected:
                self.selection=BoxesUI.NUM_BOX_BUTTON_COLS//2-1
            self.page_selected=False
            self.party_selected=False

    #when B is pressed and boxes or page button is selected, go back to party buttons selection
    def go_back(self):
        if self.page_selected:
            self.selection=0
        else: #party_selected must be false for this method to be called
            self.selection=self.selection//BoxesUI.NUM_BOX_BUTTON_COLS+1
        self.page_selected=False
        self.party_selected=True
        self.reset_box_buttons(LIGHT_GRAY)
        self.reset_party_buttons(WHITE)

    #gray out party buttons when moving selection to box buttons
    def reset_party_buttons(self,color):
        for i in range(len(self.party_buttons)):
            self.party_buttons[i].image.fill(color)
            if self.game.player.party[i] is not None:
                img=pygame.Surface((BoxesUI.PARTY_BUTTON_HEIGHT*3//4,BoxesUI.PARTY_BUTTON_HEIGHT*3//4))
                img.fill(BLACK)
                self.party_buttons[i].image.blit(img,(BoxesUI.PARTY_BUTTON_HEIGHT//8,BoxesUI.PARTY_BUTTON_HEIGHT//8))
                draw_text(self.party_buttons[i].image,self.game.player.party[i].nickname,BoxesUI.PARTY_BUTTON_HEIGHT//3,BLACK,BoxesUI.PARTY_BUTTON_HEIGHT,BoxesUI.PARTY_BUTTON_HEIGHT//8,'topleft')

    #gray out box buttons and page button when moving selection to party buttons
    def reset_box_buttons(self,color):
        for i in range(len(self.box_buttons)):
            self.box_buttons[i].image.fill(color)
            if self.game.player.boxes[self.page_index][i%BoxesUI.NUM_BOX_BUTTONS] is not None:
                img=pygame.Surface((BoxesUI.BOX_BUTTON_SIZE*3//4,BoxesUI.BOX_BUTTON_SIZE*3//4))
                img.fill(BLACK)
                self.box_buttons[i].image.blit(img,(BoxesUI.BOX_BUTTON_SIZE//8,BoxesUI.BOX_BUTTON_SIZE//8))
                
        self.page_button.image.fill(color)
        draw_text(self.page_button.image,"Box "+str(self.page_index+1),BoxesUI.BOX_BUTTON_SIZE//3,BLACK,(BoxesUI.BOX_BUTTON_SIZE+BoxesUI.BORDER_BTW_BUTTONS)*3//2,BoxesUI.BOX_BUTTON_SIZE//4,'center')
