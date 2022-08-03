import random
from pokedex import ALL_POKEMON_DATA, NATURES
from move import ALL_MOVES

class Pokemon:

    def __init__(self,species,level):
        self.nickname=species
        self.species=species
        self.level=level
        self.gender= 'male' if random.random()<ALL_POKEMON_DATA[self.species].gender_ratio else 'female' #50/50 for all for now, change for specific species
        self.types=ALL_POKEMON_DATA[self.species].types
        self.nature=random.choice(list(NATURES))
        self.item=None
        self.ability=random.choice(ALL_POKEMON_DATA[self.species].abilities)

        #up to four moves
        #get moves from moveset that can be learned at this level
        learnable=[]
        for move in ALL_POKEMON_DATA[self.species].moveset.keys():
            if ALL_POKEMON_DATA[self.species].moveset[move]<=self.level:
                learnable.append(move)
        #add up to 4 learnable moves to this pokemon's moves
        self.moves=[]
        for i in range(min(len(learnable),4)):
            self.moves.append(ALL_MOVES[learnable[i]])

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
            self.stats.append(ALL_POKEMON_DATA[self.species].base_stats[i]+self.level*self.ivs[i]+self.evs[i])

    def __repr__(self):
        return self.species+" level "+str(self.level)
