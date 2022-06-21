import random

class Pokemon:
    def __init__(self,name):
        self.name=name
        self.num=random.randrange(100) #temporary attribute for testing
    
    def __repr__(self):
        return self.name+str(self.num)
