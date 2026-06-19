import json
for file in ["brawlers_moves.json", "rushdown_moves.json", "zoners_moves.json"]:
    try:
        opened_file = open(file, "r")
    except FileNotFoundError:
        print("File not found, remaking")
        import make_move_list
