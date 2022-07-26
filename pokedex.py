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
        Pokemon_Data.__init__(self,'Bulbasaur',1,['grass','poison'],0.875,['Ability 1','Ability 2', 'ha_Ability 3'],{'Tackle':1,'Vine Whip':3},[1,2,3,4,5,6],'This is Bulbasaur')

class Charmander_Data(Pokemon_Data):
    def __init__(self):
        Pokemon_Data.__init__(self,'Bulbasaur',2,['fire',None],0.875,['Ability 4','Ability 5', 'ha_Ability 6'],{'Tackle':1,'Ember':3},[1,2,3,4,5,6],'This is Charmander')

class Squirtle_Data(Pokemon_Data):
    def __init__(self):
        Pokemon_Data.__init__(self,'Bulbasaur',3,['water',None],0.875,['Ability 7','Ability 8', 'ha_Ability 9'],{'Tackle':1,'Water Gun':3},[1,2,3,4,5,6],'This is Squirtle')


#dictionary matching species strings to respective pokemon_data child class
ALL_POKEMON_DATA={'Bulbasaur':Bulbasaur_Data(),
                  'Charmander':Charmander_Data(),
                  'Squirtle':Squirtle_Data()
                 }
