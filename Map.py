import random
import math

import Utilities
from Utilities import *


def create_map(w, h):
    matrix = []
    for x in range(w * h):
        matrix.append([x + 1, Tiles(w, h)])

    tiles_list = [Checkpoints(w, h), ManaFountains(w, h),
                  BluePortals(w, h), GreenPortals(w, h)]
    for current in tiles_list:
        matrix = current.set_tiles(matrix, current)
    matrix[(w * h) - 1][1] = Tiles(w, h)
    return matrix


checkpoints = []


# Parent class
class Tiles:

    def __init__(self, width, height):
        self.image = None
        self.first = 0
        self.min = 1
        self.probability = 1
        self.distance = (1, 98)
        self.tiles = []
        self.width = width
        self.height = height

    def set_tiles(self, matrix, tile_type):
        distance = 0
        quantity = 0
        min_distance = self.distance[0]
        max_distance = self.distance[1]
        while quantity < self.min:
            position = 0
            if matrix[self.first][1].image is None:
                matrix[self.first][1] = tile_type
            while position + distance < self.width * self.height:
                if matrix[position + distance][1].image is None:
                    position = position + distance
                    ctrl = random.randint(1, self.probability)
                    if ctrl == 1:
                        matrix[position][1] = tile_type
                        quantity += 1
                    if tile_type.image == "Icons\Checkpoint.jpg":
                        checkpoints.append(position)
                distance = random.randint(min_distance, max_distance)
        return matrix

    def activate(self, player):
        pass


# Child classes
class Checkpoints(Tiles):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.image = "Icons\Checkpoint.jpg"
        self.distance = (17, 23)

    def activate(self, player):
        player.hp = player.maxhp
        Utilities.update_log(log, player.name + " arrived to a Checkpoint and got a full health recover")


class ManaFountains(Tiles):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.image = "Icons\ManaFountain.jpg"
        self.first = random.randint(2, 5)
        self.distance = (17, 23)

    def activate(self, player):
        player.mana = player.maxmana
        Utilities.update_log(log, player.name + " visited a Mana Fountain and got a full mana recover")


class BluePortals(Tiles):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.image = "Icons\BluePortal.jpg"
        self.probability = 10
        # self.min = math.floor((self.width * self.height) / self.probability)
        self.min = 0


class GreenPortals(Tiles):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.image = "Icons\GreenPortal.jpg"
        self.probability = 5
        self.min = math.floor((self.width * self.height) / self.probability)

    def activate(self, player):
        old_position = player.position
        player.position = random.randint(1, 99)
        Utilities.update_log(log, player.name +
                             " stepped into a sPortal and got teleported from " +
                             str(old_position) + " to " + str(player.position))
