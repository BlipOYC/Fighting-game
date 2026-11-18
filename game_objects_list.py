from json import JSONDecodeError

import manual_move_list_reset
from objects import Archetype, Character, Platform, Ground, Attack, Hitbox
import json
import get_move_list
move_list = []
for file in ["brawlers_moves.json", "rushdown_moves.json", "zoners_moves.json"]:
    #MUST UN-JSON LATER
    with open(file) as json_file:
        move_list.append(json.load(json_file))

def convert_to_attack(*params):
    try:
        associated_hitboxes = []
        for hitbox in params:
            try:
                associated_hitboxes.append(Hitbox(*hitbox))
            except ValueError, AttributeError, KeyError, TypeError:
                pass
            except JSONDecodeError:
                raise Exception("JSON format error: try rebooting the game or restoring the move list to its default state if modded")
        return Attack(associated_hitboxes)
    except AttributeError:
        raise Exception("PARAMETERS MISSING")

move_names = ["nLight", "fLight", "dLight", "grab", "throw", "nAir", "fAir", "uAir", "dAir"]

moves = {
    "Rushdown": {
        move_name: convert_to_attack(move_list[1][move_name]) for move_name in move_names
    },
    "Brawler": {
        move_name: convert_to_attack(move_list[0][move_name]) for move_name in move_names
    },
    "Zoner": {
        move_name: convert_to_attack(move_list[2][move_name]) for move_name in move_names
    },
}

rushdown = Archetype("Rushdown", moves["Rushdown"], 40,3,  3)
brawler = Archetype("Brawler", moves["Brawler"], 30, 3, 3)
zoner = Archetype("Zoner", moves["Zoner"], 25, 5, 5)

chara1_sigs = {}
chara2_sigs = {}
chara3_sigs = {}
chara4_sigs = {}
chara5_sigs = {}
chara6_sigs = {}

character_list = {
    "chara1": Character(
        brawler, "1", (255, 0, 0), chara1_sigs, 30, 300, 25, 100, 2, 5, 2, 20, 5, 30, 1, 10, 12),
    "chara2":Character(
        brawler, "2", (0, 0, 255), chara2_sigs, 570, 300, 25, 100, 0.5, 1, 3, 3, 10, 15, 2, 20, 12),
    "chara3":Character(
        zoner, "3", (0, 255, 0), chara3_sigs,  300, 300, 25, 100, 1, 2, 2, 2, 5, 15, 1, 10, 15),
    "chara4":Character(
        zoner, "4", (255, 255, 0), chara4_sigs,  300, 300, 25, 100, 0.5, 2, 2, 2, 5, 15, 1, 10, 15),
    "chara5":Character(
        rushdown, "5", (0, 255, 255), chara5_sigs,  300, 300, 25, 100, 2, 2, 3, 3, 10, 35, 1, 10, 15),
    "chara6":Character(
        rushdown, "6", (255, 0, 255), chara5_sigs,  300, 300, 25, 100, 2, 2, 3, 3, 10, 35, 1, 10, 15),
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
            ],
            "background": [
                None #Pass in an image from the assets tab
            ]
        }
}

platforms = [
    Platform(10, 550, 780, 10, False),
    Platform(50, 450, 250, 10, True),
    Platform(500, 450, 250, 10, True),
]

ground = Ground(10, 400, 700, 10, False)