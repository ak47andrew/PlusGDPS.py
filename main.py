import level
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["test"]
mycol = mydb["test"]


def do_things(string: str):
    lev = level.Level.from_string(string)
    lev.levelString = ""
    mycol.insert_one(lev.to_json())
    print(f"Level {lev.levelName} was dumped")


with open("levels.txt") as f:
    for line in f.readlines():
        do_things(line)
