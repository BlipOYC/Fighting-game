import json
rushdowns = {
    "nLight": (),
    "fLight": (),
    "dLight": (),
    "grab": (),
    "throw": (),
    "nAir": (),
    "fAir": (),
    "uAir": (),
    "dAir": (),
}

def create_files():
    brawlers = zoners = rushdowns.copy()
    with open("rushdown_moves.json", mode="w", encoding="utf-8") as write_file:
        json.dump(rushdowns, write_file)

    with open("brawlers_moves.json", mode="w", encoding="utf-8") as write_file:
        json.dump(brawlers, write_file)

    with open("zoners_moves.json", mode="w", encoding="utf-8") as write_file:
        json.dump(zoners, write_file)