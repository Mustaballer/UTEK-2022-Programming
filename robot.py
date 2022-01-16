

class Robot:
    def __init__(self, name, moveEff, cleanEff, x=0, y=0):
        self.x = x
        self.y = y
        self.name = name
        self.moveEff = moveEff
        self.cleanEff = cleanEff

class Location:
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time