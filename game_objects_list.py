from objects import Archetype, Character, Platform, Ground, Attack, Hitbox
import get_move_list
move_list = []
for file in ["brawlers_moves.json", "rushdown_moves.json", "zoners_moves.json"]:
    #MUST UN-JSON LATER
    opened_file = open(file, "r")
    move_list.append(opened_file.read())

def convert_to_attack(*params):
    try:
        return Attack(*params)
    except AttributeError:
        raise Exception("PARAMETERS MISSING")

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

rushdown = Archetype("Rushdown", moves["Rushdown"], 40)
brawler = Archetype("Brawler", moves["Brawler"], 30)
zoner = Archetype("Zoner", moves["Zoner"], 25)

chara1_sigs = {}
chara2_sigs = {}

character_list = {
    "chara1": Character(
        brawler, "1", (255, 0, 0), chara1_sigs, 30, 300, 25, 100, 2, 5, 2, 20, 5, 30, 1, 10),
    "chara2":Character(
        brawler, "2", (0, 0, 255), chara2_sigs, 570, 300, 25, 100, 0.5, 1, 3, 3, 10, 15, 2, 20),
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