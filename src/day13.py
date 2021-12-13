import os
from typing import List
import numpy as np

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")


def get_data_lines(input_file_name):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def fold_at(coordinates: List[List[int]], axis: str, mark: int):
    for coordinate in coordinates:
        x = coordinate[0]
        y = coordinate[1]

        if axis == "x":
            if x > mark:
                coordinate[0] = mark - (x - mark)
        else:
            if y > mark:
                coordinate[1] = mark - (y - mark)


def unique_coordinate_count(coordinates: List[List[int]]):
    return len(set([",".join([str(i) for i in coordinate]) for coordinate in coordinates]))


def print_the_thing(coordinates: List[List[int]]):
    maxes = np.max(coordinates, 0)
    max_x = maxes[0]
    max_y = maxes[1]

    print("")
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if [x, y] in coordinates:
                print("#", end="")
            else:
                print(" ", end="")
        print("")
    print("")


def do_the_thing(input_file_name: str, folds_to_complete: int = -1, display_output: bool = False):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    coordinates = []
    record_folds = False
    for data_line in data_lines:
        if data_line.strip() == "":
            record_folds = True
            continue

        if not record_folds:
            coordinates.append(list(map(int, data_line.split(","))))
        elif folds_to_complete != 0:
            fold_instruction = data_line.split()[2].split("=")
            fold_at(coordinates, fold_instruction[0], int(fold_instruction[1]))
            folds_to_complete -= 1

    print(f"Number of unique coordinates after folds: {unique_coordinate_count(coordinates)}")

    if display_output:
        print_the_thing(coordinates)

    print(f"#################################\n")


def day_13_do(input_file_name):
    do_the_thing(input_file_name, 1)


def day_13_do_2(input_file_name):
    do_the_thing(input_file_name, -1, True)


day_13_do("day13.txt")
day_13_do_2("day13.txt")
