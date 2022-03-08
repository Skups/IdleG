import json

def load_file():
    with open("savefile.json", "r") as savefile:
        data = json.load(savefile)
    savefile.close()
    return data

def save_file(data):
    with open("savefile.json", "w") as savefile:
        json.dump(data, savefile)
    savefile.close()