import random
from poke_types import PokeTypes

class Pokemon:

    #Nature:[multiplier for each stat, 1 for no change, 1.1 for increase, 0.9 for decrease]
    NATURES={"Hardy":[1,1,1,1,1,1], #none
             "Lonely":[1,1.1,0.9,1,1,1],
             "Brave":[1,1.1,1,1,1,0.9],
             "Adamant":[1,1.1,1,0.9,1,1],
             "Naughty":[1,1.1,1,1,0.9,1],
             "Bold":[1,0.9,1.1,1,1,1],
             "Docile":[1,1,1,1,1,1], #none
             "Relaxed":[1,1,1.1,1,1,0.9],
             "Impish":[1,1,1.1,0.9,1,1],
             "Lax":[1,1,1.1,1,0.9,1],
             "Timid":[1,0.9,1,1,1,1.1],
             "Hasty":[1,1,0.9,1,1,1.1],
             "Serious":[1,1,1,1,1,1], #none
             "Jolly":[1,1,1,0.9,1,1.1],
             "Naive":[1,1,1,1,0.9,1.1],
             "Modest":[1,0.9,1,1.1,1,1],
             "Mild":[1,1,0.9,1.1,1,1],
             "Quiet":[1,1,1,1.1,1,0.9],
             "Bashful":[1,1,1,1,1,1], #none
             "Rash":[1,1,1,1.1,0.9,1],
             "Calm":[1,0.9,1,1,1.1,1],
             "Gentle":[1,1,0.9,1,1.1,1],
             "Sassy":[1,1,1,1,1.1,0.9],
             "Careful":[1,1,1,0.9,1.1,1],
             "Quirky":[1,1,1,1,1,1] #none
            }

    def __init__(self,species,level):
        self.nickname=species
        self.species=species
        self.level=level
        self.gender= 'male' if random.random()<0.5 else 'female' #50/50 for all for now, change for specific species
        self.types=[random.choice(PokeTypes.TYPES),random.choice(PokeTypes.TYPES) if random.random()>0.5 else None]
        self.nature=random.choice(list(Pokemon.NATURES))
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
