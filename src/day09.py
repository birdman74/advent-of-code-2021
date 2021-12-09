import os
import math
from typing import List

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")


def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def is_low_point(top_map: List[List[int]], x: int, y: int, x_len: int, y_len: int):
    height = top_map[x][y]
    # print(f"x: {x}, y: {y}, height: {height}")
    if (x > 0 and top_map[x-1][y] <= height) or \
            (y > 0 and top_map[x][y-1] <= height) or \
            (x < x_len - 1 and top_map[x+1][y] <= height) or \
            (y < y_len - 1 and top_map[x][y+1] <= height):
        return False

    return True


def do_the_thing(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    top_map = []
    [top_map.append([int(heights[i]) for i in range(len(heights))]) for heights in data_lines]

    x_length = len(top_map)
    y_length = len(top_map[0])

    low_point_risk_levels = sum(
        [sum([1 + top_map[x][y] if is_low_point(top_map, x, y, x_length, y_length) else 0 for y in range(y_length)])
         for x in range(x_length)])

    print(f"Low points total risk level: {low_point_risk_levels}\n#################################\n")


def higher_adjacent_point_count(top_map: List[List[int]], current_point: List[int], x_len: int, y_len: int,
                                counted_points: List[List[int]]):

    total_adjacent_higher_points = 0
    x = current_point[0]
    y = current_point[1]
    height = top_map[x][y]

    # Above
    if x > 0 and [x-1, y] not in counted_points and 9 > top_map[x-1][y] > height:
        counted_points.append([x-1, y])
        total_adjacent_higher_points += 1 + higher_adjacent_point_count(top_map, [x-1, y], x_len, y_len, counted_points)

    # Left
    if y > 0 and [x, y-1] not in counted_points and 9 > top_map[x][y-1] > height:
        counted_points.append([x, y-1])
        total_adjacent_higher_points += 1 + higher_adjacent_point_count(top_map, [x, y-1], x_len, y_len, counted_points)

    # Below
    if x < x_len - 1 and [x+1, y] not in counted_points and 9 > top_map[x+1][y] > height:
        counted_points.append([x+1, y])
        total_adjacent_higher_points += 1 + higher_adjacent_point_count(top_map, [x+1, y], x_len, y_len, counted_points)

    # Right
    if y < y_len - 1 and [x, y+1] not in counted_points and 9 > top_map[x][y+1] > height:
        counted_points.append([x, y+1])
        total_adjacent_higher_points += 1 + higher_adjacent_point_count(top_map, [x, y+1], x_len, y_len, counted_points)

    return total_adjacent_higher_points


def size_of_basin(top_map: List[List[int]], low_point: List[int], x_len: int, y_len: int):
    return 1 + higher_adjacent_point_count(top_map, low_point, x_len, y_len, [])


def do_the_thing_2(input_file_name):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    top_map = []
    [top_map.append([int(heights[i]) for i in range(len(heights))]) for heights in data_lines]

    x_length = len(top_map)
    y_length = len(top_map[0])

    low_points = []

    [[low_points.append([x, y]) if is_low_point(top_map, x, y, x_length, y_length) else 0 for y in range(y_length)]
     for x in range(x_length)]

    top_3_basin_product = math.prod(
        sorted([size_of_basin(top_map, low_point, x_length, y_length) for low_point in low_points], reverse=True)[0:3])

    print(f"Top 3 basin size product: {top_3_basin_product}")


def day_9_do(input_file_name):
    do_the_thing(input_file_name)


def day_9_do_2(input_file_name):
    do_the_thing_2(input_file_name)


day_9_do("day09.txt")
day_9_do_2("day09.txt")
