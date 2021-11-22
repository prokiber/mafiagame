
 class Lobby(object):
    def __init__(self):
        self.game={}
        
        
class Ninja(object):
    def __init__(self):
        self.hp=20
        self.damage=4
        self.evade=10
        self.accuracy=10
        self.cost=80
        
        
class Robot(object):
    def __init__(self):
        self.hp=25
        self.damage=3
        self.evade=2
        self.accuracy=10
        self.cost=80
        
        
class Berserk(object):
    def __init__(self):
        self.hp=25
        self.damage=6
        self.evade=5
        self.accuracy=10
        self.cost=80
        
berserk=Berserk()        
robot=Robot()        
ninja=Ninja()        
lobby = Lobby()
