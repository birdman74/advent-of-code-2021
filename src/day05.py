import os
from collections import Counter


MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")


class Coordinate:
    x = 0
    y = 0

    def __init__(self, string_coordinates):
        coordinates = string_coordinates.split(",")
        self.x = int(coordinates[0])
        self.y = int(coordinates[1])

    def to_string(self):
        return "({}, {})".format(self.x, self.y)


class Line:
    def __init__(self, begin: Coordinate, end: Coordinate, draw_diagonals: bool):
        if begin.x == end.x:
            print(f"Line from {begin.to_string()} to {end.to_string()} is vertical")
            self.points = [(begin.x, y) for y in range(min(begin.y, end.y), max(begin.y, end.y) + 1)]
        elif begin.y == end.y:
            print(f"Line from {begin.to_string()} to {end.to_string()} is horizontal")
            self.points = [(x, begin.y) for x in range(min(begin.x, end.x), max(begin.x, end.x) + 1)]
        else:
            print(f"Line from {begin.to_string()} to {end.to_string()} is diagonal")
            self.points = []
            if draw_diagonals:
                x_increment = 1
                y_increment = 1
                if begin.x > end.x:
                    x_increment = -1
                if begin.y > end.y:
                    y_increment = -1

                x = begin.x
                y = begin.y
                while x != end.x:
                    self.points.append((x, y))
                    x += x_increment
                    y += y_increment
                self.points.append((end.x, end.y))


def calculate_overlapping_coordinate_count(input_file_name, include_diagonals: bool):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    data_lines = data_file.read().split("\n")

    lines = []

    for data_line in data_lines:
        pieces = data_line.split()
        lines.append(Line(Coordinate(pieces[0]), Coordinate(pieces[2]), include_diagonals))

    all_points = []
    for line in lines:
        all_points.extend(line.points)

    coordinate_counter = Counter(all_points)
    point_frequencies = coordinate_counter.most_common()
    overlap_point_count = len(list(filter(lambda x: x[1] > 1, point_frequencies)))

    print(f"Number of overlap points: {overlap_point_count}\n#################################\n")


def day_5_do(input_file_name):
    calculate_overlapping_coordinate_count(input_file_name, False)


def day_5_do_2(input_file_name):
    calculate_overlapping_coordinate_count(input_file_name, True)


day_5_do("day05.txt")
day_5_do_2("day05.txt")
