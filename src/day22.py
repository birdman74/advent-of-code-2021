import os
from typing import List

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")

MIN = -50
MAX = 50


def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def bound_num(num: int):
    return max(MIN, min(MAX, num))


def do_the_thing(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    on_cubes = {}

    for data_line in data_lines:
        ranges = {}
        instruction, coord = data_line.split(" ")
        axis_specs = coord.split(",")

        for axis_spec in axis_specs:
            axis_data = axis_spec.split("=")
            axis = axis_data[0]
            ranges[axis] = list((map(int, axis_data[1].split(".."))))

            if ranges[axis][0] > MAX or ranges[axis][1] < MIN:
                del ranges[axis]
            else:
                ranges[axis] = [bound_num(num) for num in ranges[axis]]

        if len(ranges) < 3:
            continue

        for x in range(ranges["x"][0], ranges["x"][1] + 1):
            for y in range(ranges["y"][0], ranges["y"][1] + 1):
                for z in range(ranges["z"][0], ranges["z"][1] + 1):
                    key = (x, y, z)
                    if instruction == "on":
                        on_cubes[key] = True
                    elif key in on_cubes:
                        del on_cubes[key]

    print(f"Number of cubes turned on: {len(on_cubes)}\n#################################\n")


class Prism():
    def __init__(self, x_range, y_range, z_range):
        self.x1 = x_range[0]
        self.x2 = x_range[1]
        self.y1 = y_range[0]
        self.y2 = y_range[1]
        self.z1 = z_range[0]
        self.z2 = z_range[1]

    def size(self):
        return (self.x2 - self.x1) * \
               (self.y2 - self.y1) * \
               (self.z2 - self.z1)

    def __sub__(self, other):
        def remaining_ranges(axis: str):
            ranges = []

            if axis == "x":
                s1 = self.x1
                e1 = self.x2
                s2 = other.x1
                e2 = other.x2
            elif axis == "y":
                s1 = self.y1
                e1 = self.y2
                s2 = other.y1
                e2 = other.y2
            else:
                s1 = self.z1
                e1 = self.z2
                s2 = other.z1
                e2 = other.z2

            # calculate left-over ranges
            ordered = sorted([s1, e1, s2, e2])
            if s1 == ordered[0]:
                if e1 == ordered[1]:
                    ranges.append([ordered[0], ordered[1]])
                else:
                    ranges.append([ordered[0], ordered[1] - 1])

            if e1 == ordered[3]:
                if s1 == ordered[2]:
                    ranges.append([ordered[2], ordered[3]])
                else:
                    ranges.append([ordered[2] + 1, ordered[3]])

            return ranges

        x_fragments = remaining_ranges("x")
        y_fragments = remaining_ranges("y")
        z_fragments = remaining_ranges("z")

        if x_fragments == [self.x1, self.x2] or \
                y_fragments == [self.y1, self.y2] or \
                z_fragments == [self.z1, self.z2]:
            return [self]

        elif x_fragments == [] and y_fragments == [] and z_fragments == []
            return []
        elif
        else:



def do_the_thing_2(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    prisms = []

    for data_line in data_lines:
        print(f"dimensions: {data_line}")
        ranges = {}
        instruction, coord = data_line.split(" ")
        axis_specs = coord.split(",")

        for axis_spec in axis_specs:
            axis_data = axis_spec.split("=")
            axis = axis_data[0]
            ranges[axis] = list(map(bound_num, map(int, axis_data[1].split(".."))))

        p = Prism(ranges["x"], ranges["y"], ranges["z"])

        new_prisms = []
        for prism in prisms:
            new_prisms.extend(prism - p)
        if instruction == "on":
            new_prisms.append(p)

        if isinstance(prisms, Prism):
            prisms = [new_prisms]
        else:
            prisms = new_prisms

    on_cubes = sum(prism.size() for prism in prisms)
    print(f"Total # of cubes turned on: {on_cubes}\n#################################\n")


def day_0_do(input_file_name: str):
    do_the_thing(input_file_name)


def day_0_do_2(input_file_name: str):
    do_the_thing_2(input_file_name)


day_0_do("day22-sample1.txt")
day_0_do_2("day22-sample1.txt")
