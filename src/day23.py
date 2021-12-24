import copy
import os
import re
from typing import List

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")

AMBER = "A"
BRONZE = "B"
COPPER = "C"
DESERT = "D"

COST = {AMBER: 1, BRONZE: 10, COPPER: 100, DESERT: 1000}
HOMES = {AMBER: [11, 12],
         BRONZE: [13, 14],
         COPPER: [15, 16],
         DESERT: [17, 18]}

OPEN = "."
HALL_STOPS = [0, 1, 3, 5, 7, 9, 10]
HALL_NONOS = [2, 4, 6, 8]
TOPS = [11, 13, 15, 17]
BOTTOMS = [12, 14, 16, 18]
TOP_DOORS = {11: 2, 13: 4, 15: 6, 17: 8}
BOTTOM_DOORS = {12: 2, 14: 4, 16: 6, 18: 8}
VALUE_POSITIONS = {AMBER: [12, 11, 1, 3, 0, 5, 7, 9, 10],
                   BRONZE: [14, 13, 3, 5, 1, 7, 0, 9, 10],
                   COPPER: [16, 15, 7, 5, 9, 3, 10, 1, 0],
                   DESERT: [18, 17, 9, 7, 10, 5, 3, 1, 0]}

MIN_TOTAL_COST = -1
GOAL = "...........AABBCCDD"

OPEN_PATH = re.compile(r"[^\.]")


def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def is_home(hall_map: str, location: int):
    critter = hall_map[location]
    home = HOMES[critter]
    if location == home[1] or (location == home[0] and critter == hall_map[home[1]]):
        return True
    else:
        return False


def is_move_allowed(hall_map: str, start: int, end: int):
    i = start
    j = end
    if start in HALL_STOPS:
        if end in HALL_STOPS or (end in TOPS and hall_map[end + 1] == OPEN):
            return False
        critter = hall_map[start]
        if end not in HOMES[critter] or (end in TOPS and hall_map[end + 1] != critter):
            return False
    else:
        if end not in HALL_STOPS:
            return False
        i = end
        j = start

    path = hall_map[end]
    if j in TOP_DOORS:
        if i < TOP_DOORS[j]:
            path += hall_map[i + 1: TOP_DOORS[j] + 1]
        else:
            path += hall_map[TOP_DOORS[j]: i]
    elif j in BOTTOM_DOORS:
        if i < BOTTOM_DOORS[j]:
            path += hall_map[i + 1: BOTTOM_DOORS[j] + 1] + hall_map[j - 1]
        else:
            path += hall_map[BOTTOM_DOORS[j]: i] + hall_map[j - 1]
    else:
        return False

    return not bool(OPEN_PATH.search(path))


def move_length(start: int, end: int):
    if start in HALL_STOPS:
        if end in TOP_DOORS:
            length = abs(start - TOP_DOORS[end]) + 1
        else:
            length = abs(start - BOTTOM_DOORS[end]) + 2
    else:
        if start in TOPS:
            length = abs(end - TOP_DOORS[start]) + 1
        else:
            length = abs(end - BOTTOM_DOORS[start]) + 2
    return length


def move(hall_map: str, start: int, end: int):
    critter = hall_map[start]
    # print(f"Moving {critter} at {start} to {end}")
    cost = COST[critter] * move_length(start, end)

    # print(f"Before: {hall_map}")
    map_list = list(hall_map)
    map_list[end] = critter
    map_list[start] = OPEN
    new_map = "".join(map_list)
    # print(f"After:  {new_map}, move cost: {cost}\n")

    return new_map, cost


def open_spaces(hall_map: str):
    return list(filter(lambda spot: spot not in HALL_NONOS, [i for i, ltr in enumerate(hall_map) if ltr == OPEN]))


def set_minimum_score(new_cost: int):
    global MIN_TOTAL_COST
    new_minimum = False
    if MIN_TOTAL_COST == -1:
        MIN_TOTAL_COST = new_cost
        new_minimum = True
    else:
        if new_cost < MIN_TOTAL_COST:
            MIN_TOTAL_COST = new_cost
            new_minimum = True

    if new_minimum:
        print(f"New minimum cost: {MIN_TOTAL_COST}")


def make_next_moves(hall_map: str, cost: int):
    destinations = open_spaces(hall_map)
    for location in range(len(hall_map)):
        if hall_map[location] in COST:
            if is_home(hall_map, location):
                continue

            value_destinations = list(filter(lambda pos: pos in destinations, VALUE_POSITIONS[hall_map[location]]))
            for destination in value_destinations:
                if is_move_allowed(hall_map, location, destination):
                    global MIN_TOTAL_COST
                    new_map, additional_cost = move(copy.deepcopy(hall_map), location, destination)
                    new_cost = cost + additional_cost
                    if new_cost > MIN_TOTAL_COST > 0:
                        return
                    if new_map == GOAL:
                        set_minimum_score(new_cost)
                        return

                    make_next_moves(new_map, new_cost)


def do_the_thing(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    room_tops = data_lines[2]
    room_bottoms = data_lines[3]
    hall_map = "..........." + \
               room_tops[3] + room_bottoms[3] + \
               room_tops[5] + room_bottoms[5] + \
               room_tops[7] + room_bottoms[7] + \
               room_tops[9] + room_bottoms[9]

    print(f"Goal:    {GOAL}\nInitial: {hall_map}")

    make_next_moves(hall_map, 0)

    print(f"Lowest possible score: {MIN_TOTAL_COST}\n#################################\n")


def day_0_do(input_file_name: str):
    do_the_thing(input_file_name)


day_0_do("day23-part1.txt")
