import requests
import itertools

headers = {
    "User-Agent": ""
}

data = {
    "levelID": 1,
    "secret": "Wmfd2893gb7"
}

while data["levelID"] <= 3924:
    print(f"Loading level with ID: {data['levelID']}...")
    req = requests.post("https://gmd.plusgdps.dev/database/downloadGJLevel22.php", data=data, headers=headers)
    if not req:
        print("Request error!")
        print(f"{req.status_code=}\n{req.text=}")
        break
    if req.text == "-1":
        print("404: Level not found")
    else:
        with open("levels.txt", "a") as f:
            f.write(req.text)
            f.write("\n")
        print(f"Level found and saved! Name: {req.text.split(':')[3]}")
    print("Done!")
    data["levelID"] += 1
