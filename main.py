import time
from clusterer import Clusterer
from space_info import create_space


# setting point of values
NUMBER_OF_CLUSTERS = 15
ALGORITHM_TYPE = 1


# main function that calls the space creating and clustering class
def main():
    space = create_space()
    Clusterer(space, NUMBER_OF_CLUSTERS, ALGORITHM_TYPE)


# testing function that repeats the clustering process on the same space for n number of times
def testing():
    space = create_space()
    NUMBER_OF_TESTING_ITERATIONS = 10
    total_iterations = 0
    total_time = 0
    total_successes = 0

    for i in range(NUMBER_OF_TESTING_ITERATIONS):
        start_time = time.time()
        clustering_done = Clusterer(space, NUMBER_OF_CLUSTERS, ALGORITHM_TYPE)
        end_time = time.time()
        total_iterations += clustering_done.final_iteration
        total_time += end_time - start_time
        if clustering_done.success:
            total_successes += 1

    print("Average iterations needed:", total_iterations / NUMBER_OF_TESTING_ITERATIONS)
    print("Average time needed:", total_time / NUMBER_OF_TESTING_ITERATIONS)
    print("Average success rate:", str(total_successes / NUMBER_OF_TESTING_ITERATIONS) + "%")


if __name__ == '__main__':
    main()
    # testing()
