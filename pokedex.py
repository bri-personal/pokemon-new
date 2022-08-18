#Parent class to store game data for all pokemon
##child classes inherit this and fill attributes, which can be called through Pokedex class's DEX attribute
class Pokemon_Data:
    def __init__(self,species: str,number: int,types: list[str],gender_ratio:float,abilities:list[str],moveset:dict[int,str],base_stats:list[int],entry:str):
        self.species=species #species string, same as name of child class
        self.number=number #pokedex number, determined by index of child class in ALL_POKEMON_DATA
        self.types=types #types, list of strings
        self.gender_ratio=gender_ratio #double, used as rate of male (ex. 0.25 -> 25% male, 75% female)
        self.abilities=abilities #possible abilities, list of strings. HA is marked with 'ha_' if exists and should be last index
        self.moveset=moveset #dictionary matching move strings to level they are learned at, retrieved from moves dictionary
        self.base_stats=base_stats #list of ints for base stats
        self.pokedex_entry=entry #string of pokedex entry

#child classes of Pokemon_Data
class Bulbasaur_Data(Pokemon_Data):
    def __init__(self):
        Pokemon_Data.__init__(self,'Bulbasaur',1,['grass','poison'],0.875,['Ability 1','Ability 2', 'ha_Ability 3'],{'Tackle':1,'Vine Whip':3},[1,2,3,4,5,6],'This is Bulbasaur. It is the seed pokemon. Not everyone knows this, but this text now takes up multiple lines. That is cool, right.')

class Ivysaur_Data(Pokemon_Data):
    def __init__(self):
        Pokemon_Data.__init__(self,'Ivysaur',2,['grass','poison'],0.875,['Ability 1','Ability 2', 'ha_Ability 3'],{'Tackle':1,'Vine Whip':3},[1,2,3,4,5,6],'This is Ivysaur')

class Venusaur_Data(Pokemon_Data):
    def __init__(self):
        Pokemon_Data.__init__(self,'Venusaur',3,['grass','poison'],0.875,['Ability 1','Ability 2', 'ha_Ability 3'],{'Tackle':1,'Vine Whip':3},[1,2,3,4,5,6],'This is Venusaur')

class Charmander_Data(Pokemon_Data):
    def __init__(self):
        Pokemon_Data.__init__(self,'Charmander',4,['fire',None],0.875,['Ability 4','Ability 5', 'ha_Ability 6'],{'Tackle':1,'Ember':3},[1,2,3,4,5,6],'This is Charmander')

class Charmeleon_Data(Pokemon_Data):
    def __init__(self):
        Pokemon_Data.__init__(self,'Charmeleon',5,['fire',None],0.875,['Ability 4','Ability 5', 'ha_Ability 6'],{'Tackle':1,'Ember':3},[1,2,3,4,5,6],'This is Charmeleon')

class Charizard_Data(Pokemon_Data):
    def __init__(self):
        Pokemon_Data.__init__(self,'Charizard',6,['fire','flying'],0.875,['Ability 4','Ability 5', 'ha_Ability 6'],{'Tackle':1,'Ember':3},[1,2,3,4,5,6],'This is Charizard')

class Squirtle_Data(Pokemon_Data):
    def __init__(self):
        Pokemon_Data.__init__(self,'Squirtle',7,['water',None],0.875,['Ability 7','Ability 8', 'ha_Ability 9'],{'Tackle':1,'Water Gun':3},[1,2,3,4,5,6],'This is Squirtle')

class Wartortle_Data(Pokemon_Data):
    def __init__(self):
        Pokemon_Data.__init__(self,'Wartortle',8,['water',None],0.875,['Ability 7','Ability 8', 'ha_Ability 9'],{'Tackle':1,'Water Gun':3},[1,2,3,4,5,6],'This is Wartortle')

class Blastoise_Data(Pokemon_Data):
    def __init__(self):
        Pokemon_Data.__init__(self,'Blastoise',9,['water',None],0.875,['Ability 7','Ability 8', 'ha_Ability 9'],{'Tackle':1,'Water Gun':3},[1,2,3,4,5,6],'This is Blastoise')

class Pikachu_Data(Pokemon_Data):
    def  __init__(self):
        Pokemon_Data.__init__(self,'Pikachu',10,['electric',None],0.875,['Ability 10','Ability 11','ha_Ability 12'],{'Quick Attack':1,'Thunder Shock':1},[1,2,3,4,5,6],'This is Pikachu, the Pokemon mascot. It is loved by fans across the world.')

#dictionary matching species strings to respective pokemon_data child class
#to add pokemon, create new #_Data class inheriting Pokemon_Data, add it to ALL_POKEMON_DATA dict, add any new moves to ALL_MOVES in move.py
ALL_POKEMON_DATA={'Bulbasaur':Bulbasaur_Data(),
                  'Ivysaur':Ivysaur_Data(),
                  'Venusaur':Venusaur_Data(),
                  'Charmander':Charmander_Data(),
                  'Charmeleon':Charmeleon_Data(),
                  'Charizard':Charizard_Data(),
                  'Squirtle':Squirtle_Data(),
                  'Wartortle':Wartortle_Data(),
                  'Blastoise':Blastoise_Data(),
                  'Pikachu':Pikachu_Data()
                 }

ALL_POKEMON=list(ALL_POKEMON_DATA)

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