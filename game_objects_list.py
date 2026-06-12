from objects import Character, Platform, Ground, Attack, Hitbox


moves = {
    "Rushdown": {
        "nLight": None,
        "fLight": None,
        "dLight": None,
        "grab": None,
        "throw": None,
        "nAir": None,
        "fAir": None,
        "uAir": None,
        "dAir": None,
    },
    "Brawler": {
        "nLight": None,
        "fLight": None,
        "dLight": None,
        "grab": None,
        "throw": None,
        "nAir": None,
        "fAir": None,
        "uAir": None,
        "dAir": None,
    },
    "Zoner": {
        "nLight": None,
        "fLight": None,
        "dLight": None,
        "grab": None,
        "throw": None,
        "nAir": None,
        "fAir": None,
        "uAir": None,
        "dAir": None,
    },
} #Implement l8r

character_list = {
    "chara1": Character("Brawler", "1", (255, 0, 0), moves["Brawler"], 30, 300, 25, 100, 2, 5, 2, 20, 5, 20, 1, 10),
    "chara2":Character("Brawler", "2", (0, 0, 255), moves["Brawler"], 570, 300, 25, 100, 0.5, 1, 3, 3, 10, 15, 2, 20),
}


maps = {
    "map1":
        {
            "platforms": [
                Platform(10, 550, 780, 10, False),
                Platform(50, 400, 250, 10, True),
                Platform(500, 400, 250, 10, True),
            ],
            "ground": [
                Ground(10, 400, 700, 10, False)
            ]
        }
}

platforms = [
    Platform(10, 550, 780, 10, False),
    Platform(50, 450, 250, 10, True),
    Platform(500, 450, 250, 10, True),
]

ground = Ground(10, 400, 700, 10, False)