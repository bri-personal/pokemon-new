import random
from poke_types import PokeTypes

class Pokemon:
    def __init__(self,species,level):
        self.nickname=species
        self.species=species
        self.level=level
        self.gender= 'male' if random.random()>0.5 else 'female' #50/50 for all for now, change for specific species
        self.types=[random.choice(PokeTypes.TYPES),random.choice(PokeTypes.TYPES) if random.random()>0.5 else None]
        self.nature='Nature '+str(random.randrange(32))
        self.item='None'
        self.ability='Ability '+str(random.randrange(100))

        #up to four moves
        self.moves=[]
        for i in range(4):
            self.moves.append(str(i)+': Move '+str(random.randrange(100)))

        #individual values - stats determined on init
        self.ivs=[]
        for _ in range(6):
            self.ivs.append(random.randrange(32))
        
        #effort values - stats changed during gameplay
        self.evs=[0]*6

        #final stats calculated from level, ivs, evs, etc
        self.stats=[]
        #calculate stats based on base stats
        for i in range(len(self.ivs)):
            self.stats.append(self.level*self.ivs[i]+self.evs[i])

    def __repr__(self):
        return self.species+" level "+str(self.level)
