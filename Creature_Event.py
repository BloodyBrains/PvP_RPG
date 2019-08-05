# NOT IMPLEMENTED


class CreatureEvent():
    def __init__(self, event):
        self.event = event

    def __str__(self):
        return self.event

    def __cmp__(self, other):
        return cmp(self.event, other.event)

    def __hash__(self):
        return hash(self.event)



CreatureEvent.idle = CreatureEvent('idle')
CreatureEvent.attack = CreatureEvent('attack')
CreatureEvent.die = CreatureEvent('die')
