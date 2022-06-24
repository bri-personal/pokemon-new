import pygame
from pages import Pages
from settings import *
from sprites import draw_text,Button

class Menu:
    #menu data
    MENU_TEXT=['Pokedex','Boxes','Bag','Card','Save','Map','Camp','Mystery Gift','VS','Settings'] #10 buttons
    MENU_COLORS=[RED,RED,ORANGE,BLUE,CYAN,GREEN,ORANGE,MAGENTA,GREEN,PURPLE] #must be same length as MENU_TEXT
    MENU_BUTTON_SIZE=HEIGHT//4
    BORDER_BTW_BUTTONS=HEIGHT//32
    BUTTON_TEXT_BORDER=HEIGHT//9

    def __init__(self,game):
        self.game=game

        #index for which button is selected on the menu screen
        self.selection=0

        #make buttons for main game menu
        self.buttons=[]
        for i in range(len(Menu.MENU_TEXT)):
            img=pygame.Surface((Menu.MENU_BUTTON_SIZE,Menu.MENU_BUTTON_SIZE))
            img.fill(WHITE)
            draw_text(img,Menu.MENU_TEXT[i],Menu.MENU_BUTTON_SIZE//6,Menu.MENU_COLORS[i],Menu.MENU_BUTTON_SIZE//2,Menu.MENU_BUTTON_SIZE//2,'center')
            self.buttons.append(Button(self.game,WIDTH//2-5*Menu.MENU_BUTTON_SIZE//2-2*Menu.BORDER_BTW_BUTTONS+(i%(len(Menu.MENU_TEXT)//2))*(Menu.MENU_BUTTON_SIZE+Menu.BORDER_BTW_BUTTONS)+Menu.MENU_BUTTON_SIZE//2,HEIGHT//2-Menu.MENU_BUTTON_SIZE-Menu.BORDER_BTW_BUTTONS-Menu.BUTTON_TEXT_BORDER+(Menu.MENU_BUTTON_SIZE+Menu.BORDER_BTW_BUTTONS*2+Menu.BUTTON_TEXT_BORDER)*(i//(len(Menu.MENU_TEXT)//2)),img))

    #move menu selection right in row
    def move_right(self):
        if self.selection==len(Menu.MENU_TEXT)//2-1:
            self.selection=0
        elif self.selection==len(Menu.MENU_TEXT)-1:
            self.selection=len(Menu.MENU_TEXT)//2
        else:
            self.selection+=1
    
    #move menu selection left in row
    def move_left(self):
        if self.selection==0:
            self.selection=len(Menu.MENU_TEXT)//2-1
        elif self.selection==len(Menu.MENU_TEXT)//2:
            self.selection=len(Menu.MENU_TEXT)-1
        else:
            self.selection-=1

    #move menu selection up in column
    def move_up(self):
        self.selection=(self.selection-len(Menu.MENU_TEXT)//2)%len(Menu.MENU_TEXT)

    #move menu selection down in column
    def move_down(self):
        self.selection=(self.selection+len(Menu.MENU_TEXT)//2)%len(Menu.MENU_TEXT)

    #return Page corresponding to current menu selection
    def get_page_from_button(self):
        match self.selection:
            case 0: #index of Pokedex in MENU_TEXT
                return Pages.DEX
            case 1: #index of Boxes in MENU_TEXT
                return Pages.BOXES
            case 2: #index of Bag in MENU_TEXT
                return Pages.BAG
            case 3: #index of Card in MENU_TEXT
                return Pages.CARD
            case 4: #index of Save in MENU_TEXT
                return Pages.SAVE
            case 5: #index of Map in MENU_TEXT
                return Pages.MAP
            case 6: #index of Camp in MENU_TEXT
                return Pages.CAMP
            case 7: #index of Mystery Gift in MENU_TEXT
                return Pages.GIFT
            case 8: #index of VS in MENU_TEXT
                return Pages.VS
            case 9: #index of Settings in MENU_TEXT
                return Pages.SETTINGS


