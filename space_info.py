import random


# function that creates 40020 points
def create_space():
    print("Creating Space...")
    space_dict = {}

    # first 20 points
    i = 0
    while i != 20:
        i += 1

        x = random.randint(-5000, 5000)
        y = random.randint(-5000, 5000)

        if (x, y) not in space_dict.keys():
            space_dict.update({(x, y): "red"})
        else:
            i -= 1
            continue

    # next 40000 points
    j = 0
    while j != 40000:
        j += 1

        x_offset = 0
        y_offset = 0

        random_point_x, random_point_y = random.choice(list(space_dict))

        if random_point_x > 4900 or random_point_x < -4900 or random_point_y > 4900 or random_point_y < -4900:
            if random_point_x > 4900:
                x_offset = random.randint(-100, 5000 - random_point_x)
            if random_point_x < -4900:
                x_offset = random.randint(-(5000 + random_point_x), 100)
            if random_point_y > 4900:
                y_offset = random.randint(-100, 5000 - random_point_y)
            if random_point_y < -4900:
                y_offset = random.randint(-(5000 + random_point_y), 100)
        else:
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)

        new_x = random_point_x + x_offset
        new_y = random_point_y + y_offset

        if (new_x, new_y) not in space_dict.keys():
            space_dict.update({(new_x, new_y): "red"})
        else:
            j -= 1
            continue

    print("Space created")
    return space_dict
