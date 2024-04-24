import requests

headers = {
    "User-Agent": ""
}

data = {
    "gameVersion": 22,
    "type": 4,
    "page": 2,
    "total": 2995
}

req = requests.post("https://gmd.plusgdps.dev/database/getGJLevels21.php", data=data, headers=headers, verify=False)
data = req.text.split("#")

for l in data[0].split("|"):
    print(l)
print()
for l in data[1].split("|"):
    print(l)
print()
print(data[2])
print()
print(data[3])
