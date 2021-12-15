import os
from typing import List

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")

movements = [[-1, 0], [1, 0], [0, -1], [0, 1]]
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


class MinScoreToPosition:
    coordinates = [-1, -1]
    score = None
    visited = False

    def __init__(self, x: int, y: int):
        self.coordinates = [x, y]


def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def move(position: List[int], movement: List[int], max_position: int):
    return [max(0, min(max_position, position[0] + movement[0])),
            max(0, min(max_position, position[1] + movement[1]))]


def reached_destination(path: List[List[int]], destination: List[int]):
    return path[len(path) - 1] == destination


def visit_position(position: List[int],
                   min_score_to_path_matrix: List[List[MinScoreToPosition]],
                   risks: List[List[int]],
                   max_position: int):
    min_score_to_current_position = min_score_to_path_matrix[position[0]][position[1]]

    for movement in movements:
        new_position = move(position, movement, max_position)
        current_min_score_to_new_position = min_score_to_path_matrix[new_position[0]][new_position[1]]

        if new_position == position or current_min_score_to_new_position.visited:  # illegal movement disallowed
            continue

        new_score = min_score_to_current_position.score + risks[new_position[0]][new_position[1]]
        if current_min_score_to_new_position.score is None or current_min_score_to_new_position.score > new_score:
            current_min_score_to_new_position.score = new_score

            # print(f"Score: {new_score}, point: {new_position}")

    min_score_to_current_position.visited = True


def position_to_visit(min_score_to_path_matrix: List[List[MinScoreToPosition]]):
    possible_positions = \
        [pos for row in min_score_to_path_matrix for pos in row if pos.score is not None and not pos.visited]

    return min(possible_positions, key=lambda pos: pos.score).coordinates


def destination_not_visited(destination: List[int], min_score_to_path_matrix: List[List[MinScoreToPosition]]):
    return not min_score_to_path_matrix[destination[0]][destination[1]].visited


def do_the_thing(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    risks = []
    square_side_length = len(data_lines[0])
    for data_line in data_lines:
        risks.append([int(char) for char in data_line])

    starting_position = [0, 0]
    min_score_to_path_matrix = [[MinScoreToPosition(x, y) for y in range(square_side_length)] for x in
                                range(square_side_length)]
    min_score_to_path_matrix[0][0].score = 0
    destination = [square_side_length - 1, square_side_length - 1]

    field_positions = square_side_length * square_side_length
    visit_position(starting_position, min_score_to_path_matrix, risks, square_side_length - 1)
    positions_visited = 1
    while destination_not_visited(destination, min_score_to_path_matrix):
        visit_position(position_to_visit(min_score_to_path_matrix),
                       min_score_to_path_matrix,
                       risks,
                       square_side_length - 1)
        print(f"{positions_visited} of {field_positions} positions visited")
        positions_visited += 1

    min_score_to_destination = min_score_to_path_matrix[square_side_length - 1][square_side_length - 1]
    print(
        f"Minimum score to destination ({destination}): {min_score_to_destination.score}\n#################################\n")


def do_the_thing_2(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    risks = []
    for data_line in data_lines:
        risks.append([int(char) for char in data_line])

    # expand risks table (x5)
    expansion_factor = 5
    risks = [[x + i + k if x + i + k < 10 else (x + i + k) % 10 + 1 for i in range(expansion_factor) for x in
              risks[j % len(risks)]]
             for k in range(expansion_factor)
             for j in range(len(risks))]

    square_side_length = len(risks)
    starting_position = [0, 0]
    min_score_to_path_matrix = [[MinScoreToPosition(x, y) for y in range(square_side_length)] for x in
                                range(square_side_length)]
    min_score_to_path_matrix[0][0].score = 0
    destination = [square_side_length - 1, square_side_length - 1]

    field_positions = square_side_length * square_side_length
    visit_position(starting_position, min_score_to_path_matrix, risks, square_side_length - 1)
    positions_visited = 1
    while destination_not_visited(destination, min_score_to_path_matrix):
        visit_position(position_to_visit(min_score_to_path_matrix),
                       min_score_to_path_matrix,
                       risks,
                       square_side_length - 1)
        print(f"{positions_visited} of {field_positions} positions visited")
        positions_visited += 1

    min_score_to_destination = min_score_to_path_matrix[square_side_length - 1][square_side_length - 1]
    print(
        f"Minimum score to destination ({destination}): {min_score_to_destination.score}\n#################################\n")


def day_15_do(input_file_name: str):
    do_the_thing(input_file_name)


def day_15_do_2(input_file_name: str):
    do_the_thing_2(input_file_name)


day_15_do("day15.txt")
day_15_do_2("day15.txt")
