from objects import Character, Platform, Ground, Attack, Hitbox
import move_list


moves = {
    "Rushdown": {
        "nLight": move_list,
        "fLight": move_list,
        "dLight": move_list,
        "grab": move_list,
        "throw": move_list,
        "nAir": move_list,
        "fAir": move_list,
        "uAir": move_list,
        "dAir": move_list,
    },
    "Brawler": {
        "nLight": move_list,
        "fLight": move_list,
        "dLight": move_list,
        "grab": move_list,
        "throw": move_list,
        "nAir": move_list,
        "fAir": move_list,
        "uAir": move_list,
        "dAir": move_list,
    },
    "Zoner": {
        "nLight": move_list,
        "fLight": move_list,
        "dLight": move_list,
        "grab": move_list,
        "throw": move_list,
        "nAir": move_list,
        "fAir": move_list,
        "uAir": move_list,
        "dAir": move_list,
    },
} #Implement l8r

character_list = {
    "chara1": Character("Brawler", "1", (255, 0, 0), moves["Brawler"], 30, 300, 25, 100, 2, 5, 2, 20, 5, 30, 1, 10),
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