from objects import Character, Platform, Ground

character_list = {
    "chara1": Character("1", (255, 0, 0), (), 30, 300, 25, 100, 2, 3, 2, 10, 5, 20, 2, 20),
    "chara2":Character("2", (0, 0, 255), (), 570, 300, 25, 100, 0.5, 1, 3, 3, 10, 15, 3, 20),
}


maps = {
    "map1":
        {
            "platforms": [
                Platform(10, 550, 780, 10, False),
                Platform(50, 450, 250, 10, True),
                Platform(500, 450, 250, 10, True),
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