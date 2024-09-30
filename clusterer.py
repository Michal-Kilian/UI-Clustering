import random
from collections import defaultdict
from copy import deepcopy
from functions import calc_distance, visualize


# list of 30 colors
color_list = ["gray", "silver", "rosybrown", "firebrick", "red", "sienna", "gold", "darkkhaki", "darkgreen",
              "lightseagreen", "paleturquoise", "deepskyblue", "royalblue", "navy", "mediumpurple", "darkorchid",
              "crimson", "orange", "coral", "maroon", "y", "aquamarine", "brown", "tomato", "cyan", "b", "indigo",
              "lightslategray", "lightsalmon", "pink"]


# clustering class
class Clusterer:
    space: dict
    number_of_clusters: int
    algorithm_type: int
    success: bool
    final_iteration: int

    # initialize function that stores important values
    # and starts the process
    def __init__(self, space, number_of_clusters, algorithm_type):
        self.space = space
        self.number_of_clusters = number_of_clusters
        self.algorithm_type = algorithm_type
        self.success = False
        self.final_iteration = 0
        self.process()

    # function that picks which algorithm
    # are we going to use
    def process(self):
        if self.algorithm_type == 1:
            self.kmeans_centroid()
        elif self.algorithm_type == 2:
            self.kmeans_medoid()

    # function that picks the initial selection based on randomness
    def initial_random_point_selection(self):
        centroid_dict = {}
        for i in range(self.number_of_clusters):
            random_point = random.choice(list(self.space))
            random_unused_color = random.choice(color_list)
            color_list.remove(random_unused_color)
            centroid_dict.update({random_point: random_unused_color})

        return centroid_dict

    # function that paints the points
    # based off of their closest colored centroid/medoid
    def find_closest_points(self, centroids):
        for (x1, x2) in self.space.keys():
            min_distance = 100000

            for (y1, y2) in centroids.keys():
                if calc_distance(x1, x2, y1, y2) < min_distance:
                    min_distance = calc_distance(x1, x2, y1, y2)
                    self.space[(x1, x2)] = centroids.get((y1, y2))

    # function that calculates the average distance in each cluster
    def compute_avg_cluster_distance(self, centroids):
        total_color_lengths = {}
        points_colored = {}

        for (x, y), color in self.space.items():
            a, b = list(centroids.keys())[list(centroids.values()).index(color)]
            dist = calc_distance(x, y, a, b)
            if color not in total_color_lengths.keys():
                total_color_lengths.update({color: dist})
            else:
                length = total_color_lengths.get(color)
                total_color_lengths.update({color: length + dist})

            if color not in points_colored.keys():
                points_colored.update({color: 1})
            else:
                points_colored.update({color: points_colored.get(color) + 1})

        average_color_lengths = {}
        for color in total_color_lengths.keys():
            average_color_lengths.update({color: total_color_lengths.get(color) / points_colored.get(color)})

        if all(average_dist <= 500 for average_dist in average_color_lengths.values()):
            self.success = True
            print("Success!\nAll distances are 500 or below")

        return average_color_lengths

    # function that calculates the averages of
    # clusters' coordinates and creates new centroids
    def recompute_centroids(self):
        sorted_by_color = defaultdict(list)
        for (x, y) in self.space:
            sorted_by_color[self.space.get((x, y))].append((x, y))

        new_centroids = {}

        for color in sorted_by_color.keys():
            total_x = 0
            total_y = 0
            for (x, y) in sorted_by_color[color]:
                total_x += x
                total_y += y

            new_x, new_y = total_x // len(sorted_by_color[color]), total_y // len(sorted_by_color[color])
            new_centroids[(new_x, new_y)] = color

        return new_centroids

    # function that calculates the averages of clusters' coordinates
    # and picks the closest existing points as a new medoids
    def recompute_medoids(self):
        sorted_by_color = defaultdict(list)
        for (x, y) in self.space:
            sorted_by_color[self.space.get((x, y))].append((x, y))

        new_medoids = {}
        differences_to_average = {}

        for color in sorted_by_color.keys():
            total_x = 0
            total_y = 0
            for (x, y) in sorted_by_color[color]:
                total_x += x
                total_y += y

            average_x, average_y = total_x // len(sorted_by_color[color]), total_y // len(sorted_by_color[color])

            for (x, y) in sorted_by_color[color]:
                diff = abs(average_x - x) + abs(average_y - y)
                differences_to_average[(x, y)] = diff

            new_medoid = min(differences_to_average, key=differences_to_average.get)
            new_medoids.update({new_medoid: color})
            differences_to_average.clear()

        return new_medoids

    # the body of kmeans algorithm with centroid as a centre
    def kmeans_centroid(self):
        centroids = self.initial_random_point_selection()

        self.find_closest_points(centroids)
        self.compute_avg_cluster_distance(centroids)
        visualize(self.space)
        previous_centroids = []
        centroids_changed = True

        i = 0
        print("Clustering...")
        while not self.success and centroids_changed:
            i += 1

            new_centroids = self.recompute_centroids()

            if new_centroids == previous_centroids:
                centroids_changed = False
                self.final_iteration = i - 1
                print("The centroids have not changed in " + str(self.final_iteration) + "th iteration")
                print("Average distances of clusters:", list(self.compute_avg_cluster_distance(new_centroids).values()))

            self.find_closest_points(new_centroids)
            self.compute_avg_cluster_distance(new_centroids)

            previous_centroids = deepcopy(new_centroids)

        print("Clustering complete")
        visualize(self.space)

    # the body of kmeans algorithm with medoid as a centre
    def kmeans_medoid(self):
        medoids = self.initial_random_point_selection()

        self.find_closest_points(medoids)
        self.compute_avg_cluster_distance(medoids)
        visualize(self.space)
        previous_medoids = []
        medoids_changed = True

        i = 0
        print("Clustering...")
        while not self.success and medoids_changed:
            i += 1

            new_medoids = self.recompute_medoids()

            if new_medoids == previous_medoids:
                medoids_changed = False
                self.final_iteration = i - 1
                print("The medoids have not changed in " + str(self.final_iteration) + "th iteration")
                print("Average distances of clusters:", list(self.compute_avg_cluster_distance(new_medoids).values()))

            self.find_closest_points(new_medoids)
            self.compute_avg_cluster_distance(new_medoids)

            previous_medoids = deepcopy(new_medoids)

        print("Clustering complete")
        visualize(self.space)
