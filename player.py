from settings import *
from pokemon import Pokemon
from pokedex import ALL_POKEMON_DATA

class Player:
    MAX_PARTY_SIZE=6
    BOX_SIZE=30
    NUM_BOXES=8

    def __init__(self):
        #party is list of up to 6 Pokemon in current party
        self.party: list[Pokemon]=[None]*Player.MAX_PARTY_SIZE

        #boxes are lists of up to 30 Pokemon in storage, with up to 32 lists total
        self.boxes=[ [None]*Player.BOX_SIZE for _ in range(Player.NUM_BOXES)]

        #dex is dictionary of Pokemon (strings) and counts for number seen (0) and caught (1)
        self.dex={}
        for name in ALL_POKEMON_DATA:
            self.dex[name]=[0,0]

        #bag is dictionary of items (strings) and counts of that item player owns
        self.bag={'Pokeball':0,
                  'Potion':0,
                  'Revive':0}

    #adds to counts in player dex when pokemon is battled/caught
    def update_dex(self,name,is_caught):
        self.dex[name][0]+=1
        if is_caught:
            self.dex[name][1]+=1

    #adds pokemon to party or boxes and updates player's dex
    def catch(self,pokemon):
        self.update_dex(pokemon.species,True)

        i=0
        while i<len(self.party) and self.party[i] is not None:
            i+=1
        if i<len(self.party):
            self.party[i]=pokemon
        else:
            i=0
            while i<len(self.boxes)*len(self.boxes[0]) and self.boxes[i//len(self.boxes[0])][i%len(self.boxes[0])] is not None:
                i+=1
            if i<len(self.boxes)*len(self.boxes[0]):
                self.boxes[i//len(self.boxes[0])][i%len(self.boxes[0])]=pokemon
            else:
                print("There's no room in your boxes!")

    #remove pokemon from party at specified index, and shift all pokemon after it up
    def release_party(self,index):
        while index<len(self.party)-1:
            self.party[index]=self.party[index+1]
            index+=1
        self.party[-1]=None
        print(self.party)

    #remove pokemon from boxes at specified indices
    def release_boxes(self,page,index):
        self.boxes[page][index]=None
