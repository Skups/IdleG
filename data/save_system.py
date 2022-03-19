import json

def load_file():
    try:
        with open("savefile.json", "r") as savefile:
            data = json.load(savefile)
        savefile.close()
    except FileNotFoundError:
        data = {
    "money": 0,
    "time" : 0,

    "0" : 0,
    "1" : 0,
    "2" : 0,
    "3" : 0,
    "4" : 0,
    "5" : 0}
        with open("savefile.json", "x") as savefile:
            json.dump(data, savefile)
    return data

def save_file(data):
    with open("savefile.json", "w") as savefile:
        json.dump(data, savefile)
    savefile.close()