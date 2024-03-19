import random


class Player:

    def __init__(self, name, number):
        self.name = name
        self.maxhp = 5
        self.hp = 5
        self.maxmana = 10
        self.mana = 0
        self.position = 1
        self.shield = False
        self.revive = 1
        self.dice = (1, 6)
        self.number = number

    def lost_hp(self, dam):
        if not self.shield:
            self.hp -= dam
            if self.hp == 0:
                self.position = self.revive
                return [self.name + " got hit and lost 1 hp",
                        self.name + " lost all hp and returned to latest checkpoint he passed"]
            return [self.name + " got hit and lost 1 hp"]
        else:
            self.shield = False
            return [self.name + " got hit and lost his shield"]

    def use_mana(self, lost):
        if self.mana > lost:
            self.mana -= lost

    def get_mana(self, get):
        if self.mana + get > self.maxmana:
            self.mana = self.maxmana
        else:
            self.mana += get

    def shield_up(self):
        self.shield = True

    def roll_dice(self, w, h, checkpoints):
        distance = random.randint(self.dice[0], self.dice[1])
        if self.position + distance <= w * h:
            for x in range(len(checkpoints)):
                if self.position < checkpoints[-x] + 1 <= self.position + distance:
                    self.revive = checkpoints[-x] + 1
            self.position += distance
        else:
            self.position = w * h - (self.position + distance - w * h)
        return distance
