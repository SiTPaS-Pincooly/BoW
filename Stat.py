import math

import Utilities
from Utilities import *

casual_color = "black"
casual_font = "times new roman"


def clear_bg(source):
    image = pygame.image.load(source)
    image = image.convert_alpha()
    trans_image = image.copy()
    target_colors = [image.get_at((0, 0)),
                     image.get_at((0, image.get_height() - 1))]
    for x in range(trans_image.get_width()):
        for y in range(trans_image.get_height()):
            r, g, b, a = trans_image.get_at((x, y))
            if (r, g, b) in target_colors:
                trans_image.set_at((x, y), (r, g, b, 0))
    return trans_image


class Stat:
    def __init__(self, width, color):
        self.width = width
        self.height = width / 9 * 4
        self.color = color
        self.hp_icon = clear_bg("Icons\Hp.png")
        self.mana_icon = clear_bg("Icons\Mana.png")

    def show_stat(self, player, screen, x, y):
        pygame.draw.rect(screen, self.color,
                         pygame.Rect(x, y, self.width, self.height))

        size = math.floor(self.height / 5)
        text_height = math.floor(self.height / 3)
        width_blank = math.floor((text_height - size) / 2)

        text = [str(player.number) + ". " + player.name, "Hp: " + str(player.hp) + "/" + str(player.maxhp),
                "Mana: " + str(player.mana) + "/" + str(player.maxmana)]
        for a in range(len(text)):
            Utilities.print_text(screen, text[a],
                                 (x + width_blank, y + (text_height - size) // 2 + text_height * a),
                                 casual_color, size, casual_font)
