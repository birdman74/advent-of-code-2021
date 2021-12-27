import os
from typing import List

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")

EAST = ">"
SOUTH = "v"
SPACE = "."

def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def move_east(cuke_map: List[List[str]]):
    map_width = len(cuke_map[0])

    movement = False
    for line in cuke_map:
        moves = [False] * map_width
        for i in range(map_width):
            if line[i] == EAST and line[(i + 1) % map_width] == SPACE:
                movement = True
                moves[i] = True
        for i in range(map_width):
            if moves[i]:
                line[i] = SPACE
                line[(i + 1) % map_width] = EAST

    return movement


def move_south(cuke_map: List[List[str]]):
    map_height = len(cuke_map)
    map_width = len(cuke_map[0])

    movement = False
    for i in range(map_width):
        moves = [False] * map_height
        for j in range(map_height):
            if cuke_map[j][i] == SOUTH and cuke_map[(j + 1) % map_height][i] == SPACE:
                movement = True
                moves[j] = True
        for j in range(map_height):
            if moves[j]:
                cuke_map[j][i] = SPACE
                cuke_map[(j + 1) % map_height][i] = SOUTH

    return movement


def print_map(cuke_map: List[List[str]]):
    for line in cuke_map:
        print("".join(line))
    print("")


def do_the_thing(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    cuke_map = []
    for data_line in data_lines:
        cuke_map.append(list(data_line))

    not_frozen = True
    steps = 1
    while not_frozen:
        moved_east = move_east(cuke_map)
        moved_south = move_south(cuke_map)

        # print_map(cuke_map_map)

        not_frozen = moved_east or moved_south
        if not_frozen:
            steps += 1

    print(f"Number of steps before lock-up: {steps}\n#################################\n")


def day_25_do(input_file_name: str):
    do_the_thing(input_file_name)


day_25_do("day25.txt")
