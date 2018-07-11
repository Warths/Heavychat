import json
import math
from conf import USE_COLORED_NICKNAME, DEFAULT_NICKNAME_COLOR

class Colorspace:
    def __init__(self):
        with open("colorspace/mc_colors.json", "r") as mc_colors:
            self.color_list = []
            buffer = json.loads(mc_colors.read())
            for item in buffer:
                self.color_list.append(Color(buffer[item], item))

    def get_mc_color(self, color):
        if not USE_COLORED_NICKNAME or len(color) < 7:
            return DEFAULT_NICKNAME_COLOR
        color_16 = Color(color)
        results = {}
        for color in self.color_list:
            results[color.name] = color.compare(color_16)
        results = sorted(results.items(), key=lambda kv:kv[1])
        return results[0][0]


class Color:
    def __init__(self, hex_value, name=None):
        self.Red = int(hex_value[1:3], 16)
        self.Green = int(hex_value[3:5], 16)
        self.Blue = int(hex_value[5:7], 16)
        self.name = name
        return

    def compare(self, color):
        return math.sqrt((color.Red - self.Red) ** 2 + (color.Green - self.Green) ** 2 + (color.Blue - self.Blue) ** 2)

