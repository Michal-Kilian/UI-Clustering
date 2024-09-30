from math import dist
from matplotlib import pyplot as plt


# function to calculate the euclidean
# distance between 2 points
def calc_distance(x1, x2, y1, y2):
    return dist((x1, x2), (y1, y2))


# function that visualizes the given dictionary of points
# using their x, y coordinates and color
def visualize(dictionary):
    print("Visualizing...")
    ctx = plt

    for (x, y) in dictionary:
        ctx.plot(x, y, marker=".", color=dictionary.get((x, y)))

    ctx.show()
    print("Visualization complete")
