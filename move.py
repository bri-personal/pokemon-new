class Move:
    def __init__(self,name:str,move_type:str,atk_type:str,power:int,accuracy:float,pp:int,max_pp:int,priority:int):
        self.name=name
        self.type=move_type #elemental type of move, used to calculate effectiveness
        self.atk_type=atk_type #physical or special move, determines which attack stat is used for dmg
        self.power=power #int power factor to user in damage calculation
        self.accuracy=accuracy #float btw 0 and 1, move hits if random.random() is less than this
        self.pp=pp #int number of times move can be used
        self.max_pp=max_pp #maximum to which pp can be increased
        self.priority=priority #int determines order in which moves are played, along with speed stats

#dictionary of all move names matched to respective move objects
#for now, priority=0 for all of them but change later
ALL_MOVES={'Tackle':        Move('Tackle','normal','physical',40,1,35,56,0),
           'Quick Attack':  Move('Quick Attack','normal','physical',40,1,35,56,0),
           'Vine Whip':     Move('Vine Whip','grass','physical',45,1,25,40,0),
           'Ember':         Move('Ember','fire','special',40,1,25,40,0),
           'Water Gun':     Move('Water Gun','water','special',40,1,25,40,0),
           'Thunder Shock': Move('Thunder Shock','electric','special',40,1,40,48,0)
          }



