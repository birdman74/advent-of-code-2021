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
HOMES = {AMBER: [11, 12, 13, 14],
         BRONZE: [15, 16, 17, 18],
         COPPER: [19, 20, 21, 22],
         DESERT: [23, 24, 25, 26]}

OPEN = "."
HALL_STOPS = [0, 1, 3, 5, 7, 9, 10]
HALL_NONOS = [2, 4, 6, 8]
TOP_DOORS = {11: 2, 15: 4, 19: 6, 23: 8}
VALUE_POSITIONS = {AMBER: [14, 13, 12, 11, 1, 3, 0, 5, 7, 9, 10],
                   BRONZE: [18, 17, 16, 15, 3, 5, 1, 7, 0, 9, 10],
                   COPPER: [22, 21, 20, 19, 7, 5, 9, 3, 10, 1, 0],
                   DESERT: [26, 25, 24, 23, 9, 7, 10, 5, 3, 1, 0]}

MIN_TOTAL_COST = -1
GOAL = "...........AAAABBBBCCCCDDDD"

OPEN_PATH = re.compile(r"[^\.]")


def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def is_home(hall_map: str, location: int):
    critter = hall_map[location]
    home = HOMES[critter]
    if location not in home:
        return False
    else:
        home_stack = hall_map[location: home[3] + 1]
        filled = re.compile(r"[^" + critter + "]")
        return not bool(filled.search(home_stack))


def is_move_allowed(hall_map: str, start: int, end: int):
    i = start
    j = end
    critter = hall_map[start]
    homes = HOMES[critter]
    if start in HALL_STOPS:
        if end in HALL_STOPS or end not in homes:
            return False
        elif end != homes[3]:
            home_below = hall_map[end + 1: homes[3] + 1]
            filled = re.compile(r"[^" + critter + "]")
            if bool(filled.search(home_below)):
                return False
    else:
        if end not in HALL_STOPS:
            return False
        i = end
        j = start

    for item in HOMES.items():
        if j in item[1]:
            room_top = item[1][0]
            threshold = TOP_DOORS[room_top]
            break

    path = hall_map[end]
    path += hall_map[room_top: j]

    if i < threshold:
        path += hall_map[i + 1: threshold + 1]
    else:
        path += hall_map[threshold: i]

    return not bool(OPEN_PATH.search(path))


def move_length(hall_map: str, start: int, end: int):
    critter = hall_map[start]
    i = start
    j = end
    if start not in HALL_STOPS:
        i = end
        j = start

    for item in HOMES.items():
        if j in item[1]:
            room = item[1]
            break

    threshold = TOP_DOORS[room[0]]

    return abs(i - threshold) + abs(j - room[0]) + 1


def move(hall_map: str, start: int, end: int):
    critter = hall_map[start]
    # print(f"Moving {critter} at {start} to {end}")
    cost = COST[critter] * move_length(hall_map, start, end)

    # print("before:")
    # print_map(hall_map)
    map_list = list(hall_map)
    map_list[end] = critter
    map_list[start] = OPEN
    new_map = "".join(map_list)
    # print("after:")
    # print_map(new_map)

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


def print_map(hall_map: str):
    print(hall_map[0: 11])
    for i in range(4):
        print(f"##{hall_map[11 + i]} {hall_map[15 + i]} {hall_map[19 + i]} {hall_map[23 + i]}")


def make_next_moves(hall_map: str, cost: int, level=0):
    destinations = open_spaces(hall_map)
    # for location in range(len(hall_map)):
    for location in range(26, -1, -1):
        if hall_map[location] in COST:
            if is_home(hall_map, location):
                continue

            value_destinations = list(filter(lambda pos: pos in destinations, VALUE_POSITIONS[hall_map[location]]))
            for destination in value_destinations:
                if (location in HALL_STOPS and destination in HALL_STOPS) or (
                        location not in HALL_STOPS and destination not in HALL_STOPS):
                    continue

                if level < 1:
                    print(f"Recursion level = {level}, trying to move {location} to {destination}")

                if is_move_allowed(hall_map, location, destination):
                    global MIN_TOTAL_COST
                    new_map, additional_cost = move(copy.deepcopy(hall_map), location, destination)
                    new_cost = cost + additional_cost
                    if new_cost > MIN_TOTAL_COST > 0:
                        return
                    if new_map == GOAL:
                        set_minimum_score(new_cost)
                        return

                    make_next_moves(new_map, new_cost, level=level + 1)


def do_the_thing(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    hall = data_lines[1][1: 12]
    room_tops = data_lines[2]
    room_mid_tops = data_lines[3]
    room_mid_bottoms = data_lines[4]
    room_bottoms = data_lines[5]
    hall_map = hall + \
               room_tops[3] + room_mid_tops[3] + room_mid_bottoms[3] + room_bottoms[3] + \
               room_tops[5] + room_mid_tops[5] + room_mid_bottoms[5] + room_bottoms[5] + \
               room_tops[7] + room_mid_tops[7] + room_mid_bottoms[7] + room_bottoms[7] + \
               room_tops[9] + room_mid_tops[9] + room_mid_bottoms[9] + room_bottoms[9]

    print(f"Goal:    {GOAL}\nInitial: {hall_map}")

    make_next_moves(hall_map, 0)

    print(f"Lowest possible score: {MIN_TOTAL_COST}\n#################################\n")


def day_0_do(input_file_name: str):
    do_the_thing(input_file_name)


day_0_do("day23-part2.txt")
