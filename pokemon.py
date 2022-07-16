import random

class Pokemon:
    def __init__(self,species,level):
        self.nickname=species
        self.species=species
        self.level=level
        self.gender= 'male' if random.random()>0.5 else 'female' #50/50 for all for now, change for specific species

        #individual values - stats determined on init
        self.ivs=[]
        for _ in range(6):
            self.ivs.append(random.randrange(32))
        
        #effort values - stats changed during gameplay
        self.evs=[0]*6

        #final stats calculated from level, ivs, evs, etc
        self.stats=[]
        #calculate stats based on base stats

    def __repr__(self):
        return self.species+" level "+str(self.level)
