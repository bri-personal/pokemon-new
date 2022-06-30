from settings import *
from pokemon import Pokemon

class Player:
    MAX_PARTY_SIZE=6

    def __init__(self):
        #party is list of up to 6 Pokemon in current party
        self.party: list[Pokemon]=[None]*Player.MAX_PARTY_SIZE

        #boxes are lists of up to 30 Pokemon in storage, with up to 32 lists total
        self.boxes=[ [None]*30 for _ in range(32)]

        #dex is dictionary of Pokemon (strings) and counts for number seen (0) and caught (1)
        self.dex={'Bulbasaur':[0,0],
                  'Charmander':[0,0],
                  'Squirtle':[0,0]}

        #bag is dictionary of items (strings) and counts of that item player owns
        self.bag={'Pokeball':0,
                  'Potion':0,
                  'Revive':0}

    def update_dex(self,name,is_caught):
        self.dex[name][0]+=1
        if is_caught:
            self.dex[name][1]+=1

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
