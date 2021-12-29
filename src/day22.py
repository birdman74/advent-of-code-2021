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

    def get_size(self):
        return (self.x2 - self.x1 + 1) * \
               (self.y2 - self.y1 + 1) * \
               (self.z2 - self.z1 + 1)

    def __sub__(self, other):
        def axis_segments(axis: str):
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

            if e1 < s2 or e2 < s1:
                return {"this": [[s1, e1]]}
            elif (s2 <= s1 and e1 <= e2) or (s1 == s2 and e1 < e2) or (s2 < s1 and e1 == e2):
                return {"overlap": [[s1, e1]]}
            elif s1 < s2 < e1 < e2:
                return {"this": [[s1, s2 - 1]], "overlap": [[s2, e1]]}
            elif s2 < s1 < e2 < e1:
                return {"overlap": [[s1, e2]], "this": [[e2 + 1, e1]]}
            elif s1 < s2 < e2 < e1:
                return {"overlap": [[s2, e2]], "this": [[s1, s2 - 1], [e2 + 1, e1]]}
            elif e1 == s2:
                return {"this": [[s1, e1 - 1]], "overlap": [[e1, e1]]}
            elif s1 == s2 and e2 < e1:
                return {"overlap": [[s2, e2]], "this": [[e2 + 1, e1]]}
            elif s1 < s2 and e1 == e2:
                return {"this": [[s1, s2 - 1]], "overlap": [[s2, e2]]}
            elif s1 == e2:
                return {"overlap": [[s1, s1]], "this": [[s1 + 1, e1]]}

        x_segments = axis_segments("x")
        y_segments = axis_segments("y")
        z_segments = axis_segments("z")

        if (len(x_segments) == 1 and "this" in x_segments) or \
                (len(y_segments) == 1 and "this" in y_segments) or \
                (len(z_segments) == 1 and "this" in z_segments):
            return [self]
        elif 1 == len(x_segments) == len(y_segments) == len(z_segments) and \
                "overlap" in x_segments and "overlap" in y_segments and "overlap" in z_segments:
            return None
        else:
            leftovers = []
            if x_segments.get("this") is not None:
                leftovers.extend([Prism(x_range,
                                        [self.y1, self.y2],
                                        [self.z1, self.z2]) for x_range in x_segments.get("this")])
            if x_segments.get("overlap") is not None and z_segments.get("this") is not None:
                leftovers.extend([Prism(x_range, [self.y1, self.y2], z_range)
                                  for x_range in x_segments.get("overlap")
                                  for z_range in z_segments.get("this")])
            if x_segments.get("overlap") is not None and \
                    y_segments.get("this") is not None and \
                    z_segments.get("overlap") is not None:
                leftovers.extend([Prism(x_range, y_range, z_range)
                                  for x_range in x_segments.get("overlap")
                                  for y_range in y_segments.get("this")
                                  for z_range in z_segments.get("overlap")])
            return leftovers

    size = property(get_size)


def do_the_thing_2(input_file_name: str, stay_within_init_bounds: bool = True):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    prisms = []

    for data_line in data_lines:
        ranges = {}
        instruction, coord = data_line.split(" ")
        axis_specs = coord.split(",")

        for axis_spec in axis_specs:
            axis_data = axis_spec.split("=")
            axis = axis_data[0]
            ranges[axis] = list(map(int, axis_data[1].split("..")))

            if stay_within_init_bounds:
                if ranges[axis][0] > MAX or ranges[axis][1] < MIN:
                    del ranges[axis]
                else:
                    ranges[axis] = [bound_num(num) for num in ranges[axis]]

        if len(ranges) < 3:
            continue

        p = Prism(ranges["x"], ranges["y"], ranges["z"])

        new_prisms = []

        for prism in prisms:
            leftovers = prism - p

            if leftovers is not None:
                if len(new_prisms) == 0:
                    new_prisms = leftovers
                else:
                    new_prisms.extend(leftovers)

        prisms = new_prisms

        if instruction == "on":
            prisms.append(p)

    on_cubes = sum([prism.size for prism in prisms])
    print(f"Total # of cubes turned on: {on_cubes}\n#################################\n")


def day_22_do(input_file_name: str):
    do_the_thing(input_file_name)


def day_22_do_2(input_file_name: str, stay_within_init_bounds: bool = True):
    do_the_thing_2(input_file_name, stay_within_init_bounds)


day_22_do("day22.txt")
day_22_do_2("day22.txt", False)

