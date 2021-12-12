import os
from collections import Counter
from typing import List

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")


def get_data_lines(input_file_name):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def find_cave_index(caves: List[str], name: str):
    try:
        return caves.index(name)
    except ValueError:
        return -1


def add_path_to_dict(path_dict, first, second):
    zero_cave = path_dict.get(first)
    if zero_cave is None:
        path_dict[first] = [second]
    else:
        path_dict[first].append(second)


def dupe_small_caves_count(path: List[str]):
    cave_counter = Counter(path)
    dupe_count = 0
    for x, count in cave_counter.items():
        if x.islower() and count > 1:
            dupe_count += 1

    return dupe_count


def create_paths(current_path, current_cave, path_dict, max_dupe_small_caves: int = 0):
    if current_cave == "end":
        # print(current_path)
        return 1

    current_cave_path = current_path.split(",")
    next_caves = path_dict[current_cave]

    num_end_paths = 0
    for cave in next_caves:
        if cave.islower() and \
                cave in current_cave_path and \
                max_dupe_small_caves == dupe_small_caves_count(current_cave_path):
            continue

        num_end_paths += create_paths(",".join(current_cave_path) + "," + cave, cave, path_dict, max_dupe_small_caves)

    return num_end_paths


def do_the_thing(input_file_name, max_dupe_small_caves: int = 0):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    path_dict = {}
    for data_line in data_lines:
        caves = data_line.split("-")
        start_index = find_cave_index(caves, "start")
        end_index = find_cave_index(caves, "end")

        if start_index == -1 and end_index == -1:
            add_path_to_dict(path_dict, caves[0], caves[1])
            add_path_to_dict(path_dict, caves[1], caves[0])
        elif start_index == -1:
            add_path_to_dict(path_dict, caves[abs(end_index - 1)], caves[end_index])
        else:
            add_path_to_dict(path_dict, caves[start_index], caves[abs(start_index - 1)])

    num_paths = create_paths("start", "start", path_dict, max_dupe_small_caves)

    print(f"Number of paths: {num_paths}\n#################################\n")


def day_12_do(input_file_name):
    do_the_thing(input_file_name)


def day_12_do_2(input_file_name):
    do_the_thing(input_file_name, 1)


day_12_do("day12-sample1.txt")
day_12_do("day12-sample2.txt")
day_12_do("day12-sample3.txt")
day_12_do("day12.txt")

day_12_do_2("day12-sample1.txt")
day_12_do_2("day12-sample2.txt")
day_12_do_2("day12-sample3.txt")
day_12_do_2("day12.txt")
