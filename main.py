import requests
import itertools

headers = {
    "User-Agent": ""
}

data = {
    "levelID": 3915,
    "secret": "Wmfd2893gb7"
}

req = requests.post("https://gmd.plusgdps.dev/database/downloadGJLevel22.php", data=data, headers=headers)
data = sorted(itertools.batched(req.text.split(":"), n=2), key=lambda x: int(x[0]))
dict_data = {int(x[0]): x[1] for x in data}
for i in dict_data:
    if i == 4:
        continue
    print(i, dict_data[i])
