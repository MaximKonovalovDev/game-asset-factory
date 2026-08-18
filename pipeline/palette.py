"""Color palettes for the built-in themes. All colors are RGB tuples."""

GRASS = {
    "grass": (86, 140, 58), "grass_light": (120, 182, 86), "grass_dark": (62, 104, 42),
    "grass_deep": (42, 74, 30),
    "dirt": (124, 86, 56), "dirt_light": (148, 108, 74), "dirt_dark": (92, 62, 42),
    "water": (52, 104, 172), "water_light": (98, 160, 214), "water_deep": (26, 60, 112),
    "rock": (112, 112, 116), "rock_light": (152, 152, 156), "rock_dark": (74, 74, 80),
    "wood": (112, 76, 48), "wood_light": (140, 98, 64), "wood_dark": (76, 52, 34),
    "flower_yellow": (255, 236, 120), "flower_red": (232, 116, 104), "white": (244, 244, 248),
    "leaf_dark": (56, 100, 46), "leaf": (76, 128, 60),
}

CAVE = {
    "stone": (86, 82, 98), "stone_light": (120, 114, 132), "stone_dark": (54, 52, 66),
    "stone_deep": (32, 30, 42),
    "water": (36, 80, 140), "water_light": (70, 128, 196), "water_deep": (18, 44, 86),
    "moss": (70, 110, 70), "moss_light": (100, 150, 96),
    "gem_teal": (120, 220, 200), "gem_pink": (255, 120, 160), "gem_violet": (140, 120, 255),
}

SEASIDE = {
    "sand": (214, 190, 140), "sand_light": (232, 214, 168), "sand_dark": (178, 154, 108),
    "shallow": (96, 164, 208), "water": (58, 128, 190), "water_light": (110, 176, 228),
    "water_deep": (26, 76, 146), "foam": (232, 244, 250),
    "rock": (140, 120, 110), "rock_light": (180, 160, 150), "rock_dark": (96, 80, 74),
    "wood": (120, 82, 52), "wood_light": (148, 106, 70), "wood_dark": (82, 56, 36),
    "shell": (232, 180, 180),
}

DESERT = {
    "sand": (206, 170, 110), "sand_light": (228, 198, 140), "sand_dark": (166, 132, 84),
    "cactus": (58, 110, 64), "cactus_light": (88, 152, 96), "cactus_dark": (38, 76, 46),
    "rock": (168, 120, 92), "rock_light": (210, 166, 128), "rock_dark": (118, 80, 58),
    "water": (66, 124, 192), "water_light": (110, 170, 220),
    "bush": (150, 110, 66), "bush_dark": (112, 80, 48),
}

THEMES = {"grass": GRASS, "cave": CAVE, "water": SEASIDE, "desert": DESERT}
