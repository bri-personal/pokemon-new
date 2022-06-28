import random

class Pokemon:
    def __init__(self,species,level):
        self.nickname=species
        self.species=species
        self.level=level

        self.ivs=[]
        for _ in range(6):
            self.ivs.append(random.randrange(32))
        
        self.evs=[0]*6

        self.stats=[]
        #calculate stats based on base stats

    def __repr__(self):
        return self.species+" level "+str(self.level)
