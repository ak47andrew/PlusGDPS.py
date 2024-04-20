import json
import matplotlib.pyplot as plt

levels = json.load(open("levels.json"))["levels"]


def bubble_sort(a, b):
    running = True
    while running:
        running = False
        for i in range(len(a) - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                b[i], b[i + 1] = b[i + 1], b[i]
                running = True
    return a, b


def plot_levels(metric: str, filename: str):
    data = list(map(lambda x: x[metric], levels))

    labels = tuple(set(data))
    sizes = [data.count(x) for x in labels]
    sizes, labels = bubble_sort(sizes, list(labels))
    labels = tuple(map(str, labels))

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.savefig(filename)


for key in levels[0].keys():
    print(f"Starting {key}")
    plot_levels(key, f"output\\{key}.png")
    print(f"Done {key}")
