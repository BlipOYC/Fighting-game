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

brawlers = {
    "nLight": ((20, 20, 20, 20, [4, 10], 10, 10, 0, "forward", 4, 0, False)),
    "fLight": (),
    "dLight": (),
    "grab": (),
    "throw": (),
    "nAir": (),
    "fAir": (),
    "uAir": (),
    "dAir": (),
}

zoners = {
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
    with open("rushdown_moves.json", mode="w", encoding="utf-8") as write_file:
        json.dump(rushdowns, write_file)

    with open("brawlers_moves.json", mode="w", encoding="utf-8") as write_file:
        json.dump(brawlers, write_file)

    with open("zoners_moves.json", mode="w", encoding="utf-8") as write_file:
        json.dump(zoners, write_file)