import os
from typing import List

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")


def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def find_range(raw_range: str):
    return list(map(int, raw_range.split("=")[1].split("..")))


def min_max_x_vel(num_range):
    range_min = min(num_range)
    range_max = max(num_range)

    min_vel = None

    steps = 0
    position = 0
    while min_vel is None:
        steps += 1
        position += steps

        if min_vel is None and position > range_min:
            min_vel = steps

    return min_vel, range_max


def max_height(init_y_vel: int):
    return sum(range(init_y_vel + 1))


def min_max_y_vel(y_range: List[int]):
    return min(y_range), abs(min(y_range)) - 1


def do_the_thing(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    ranges = data_lines[0].split(": ")[1].split(", ")

    y_range = find_range(ranges[1])
    min_y_vel, max_y_vel = min_max_y_vel(y_range)

    print(f"Highest y position: {max_height(max_y_vel)}\n#################################\n")


def span_in_range(num_range: List[int]):
    return abs(num_range[0] - num_range[1]) + 1


def steps_for_vel(x_range: List[int], x_vel: int):
    steps = []

    min_x = min(x_range)
    max_x = max(x_range)

    step = 0
    dist = 0
    while x_vel > -1:
        if min_x <= dist <= max_x:
            steps.append(step)
        elif max_x < dist:
            break

        step += 1
        dist += x_vel
        x_vel -= 1

    # does our x velocity stall in the range
    if min_x <= dist <= max_x:
        steps.append(-1)

    return steps


def valid_vel(x_range: List[int], y_range: List[int], x_vel: int, y_vel: int):
    x = 0
    y = 0

    while x <= x_range[1] and y >= y_range[0]:
        x += x_vel
        y += y_vel

        if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
            return True

        x_vel = max(0, x_vel - 1)
        y_vel -= 1

    return False


def num_valid_init_vel(x_range: List[int], y_range: List[int]):
    min_x_vel, max_x_vel = min_max_x_vel(x_range)
    min_y_vel, max_y_vel = min_max_y_vel(y_range)

    num_valid_vel = 0 # span_in_range(x_range) * span_in_range(y_range)

    for x_vel in range(min_x_vel, max_x_vel + 1):
        if x_range[0] <= x_vel <= x_range[1]:
            num_valid_vel += (abs(y_range[0] - y_range[1]) + 1)
            continue
        elif len(steps_for_vel(x_range, x_vel)) == 0:
            continue

        for y_vel in range(min_y_vel, max_y_vel + 1):
            if valid_vel(x_range, y_range, x_vel, y_vel):
                num_valid_vel += 1

    return num_valid_vel


def do_the_thing_2(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    ranges = data_lines[0].split(": ")[1].split(", ")

    x_range = find_range(ranges[0])
    y_range = find_range(ranges[1])

    print(f"Number of total possible initial velocities: {num_valid_init_vel(x_range, y_range)}")


def day_17_do(input_file_name: str):
    do_the_thing(input_file_name)


def day_17_do_2(input_file_name: str):
    do_the_thing_2(input_file_name)


day_17_do("day17.txt")
day_17_do_2("day17.txt")
