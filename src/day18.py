import copy
import os
from typing import List

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")


def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


class SnailNumber:
    left = right = None

    @staticmethod
    def from_string(num_str: str):
        l_val = r_val = None

        l_str, r_str = SnailNumber.find_left_right(num_str)
        if l_str.isnumeric():
            l_val = int(l_str)
        else:
            l_val = SnailNumber.from_string(l_str)

        if r_str.isnumeric():
            r_val = int(r_str)
        else:
            r_val = SnailNumber.from_string(r_str)

        return SnailNumber(l_val, r_val)

    @staticmethod
    def find_left_right(num_str):
        num_str = num_str[1: len(num_str) - 1]

        end_index = 1
        num_levels = 1 if num_str[0] == "[" else 0
        while num_levels > 0:
            if num_str[end_index] == "[":
                num_levels += 1
            elif num_str[end_index] == "]":
                num_levels -= 1

            end_index += 1

        return num_str[0: end_index], num_str[end_index + 1:]

    def __init__(self, left: "SnailNumber", right: "SnailNumber"):
        self.left = left
        self.right = right

    def __add__(self, other):
        new_snail_num = SnailNumber(copy.deepcopy(self), copy.deepcopy(other))
        # print(f"Current unreduced SnailNum: {new_snail_num}")

        new_snail_num.reduce()
        return new_snail_num

    def reduce(self):
        reducing = True
        while reducing:
            # print(f"Reduced SnailNum: {self}")
            explosion, left_bubble, right_bubble = self.explode_inners(1)
            if explosion:
                continue
            split = self.split_inners()
            if split:
                continue

            reducing = False

    def explode_inners(self, this_nest_level: int):
        if self.is_regular_number_pair():
            return False, 0, 0

        exploded = False
        left_bubble = 0
        right_bubble = 0
        if isinstance(self.left, SnailNumber):
            if this_nest_level == 4:
                left_val = self.left.left
                right_val = self.left.right
                self.left = 0
                if isinstance(self.right, int):
                    self.right += right_val
                else:
                    self.right.add_to_left(right_val)

                return True, left_val, 0
            else:
                exploded, left_bubble, right_bubble = self.left.explode_inners(this_nest_level + 1)
                if exploded:
                    if isinstance(self.right, int):
                        self.right += right_bubble
                    else:
                        self.right.add_to_left(right_bubble)
                    right_bubble = 0

        if not exploded and isinstance(self.right, SnailNumber):
            if this_nest_level == 4:
                left_val = self.right.left
                right_val = self.right.right
                self.right = 0
                if isinstance(self.left, int):
                    self.left += left_val
                else:
                    self.left.add_to_right(left_val)

                return True, 0, right_val
            else:
                exploded, left_bubble, right_bubble = self.right.explode_inners(this_nest_level + 1)
                if exploded:
                    if isinstance(self.left, int):
                        self.left += left_bubble
                    else:
                        self.left.add_to_right(left_bubble)
                    left_bubble = 0

        return exploded, left_bubble, right_bubble

    def split_inners(self):
        # new left = num // 2
        # new right = -(num // -2)
        split = False
        if isinstance(self.left, int) and self.left > 9:
            numeric = self.left
            self.left = SnailNumber(numeric // 2, -(numeric // -2))
            return True
        elif isinstance(self.left, SnailNumber):
            split = self.left.split_inners()

        if not split:
            if isinstance(self.right, int) and self.right > 9:
                numeric = self.right
                self.right = SnailNumber(numeric // 2, -(numeric // -2))
                return True
            elif isinstance(self.right, SnailNumber):
                split = self.right.split_inners()

        return split

    def add_to_left(self, addend: int):
        if isinstance(self.left, int):
            self.left += addend
        else:
            self.left.add_to_left(addend)

    def add_to_right(self, addend: int):
        if isinstance(self.right, int):
            self.right += addend
        else:
            self.right.add_to_right(addend)

    def is_regular_number_pair(self):
        return isinstance(self.left, int) and isinstance(self.right, int)

    def __str__(self):
        return "[" + str(self.left) + "," + str(self.right) + "]"

    def magnitude(self):
        l_mag = self.left if isinstance(self.left, int) else self.left.magnitude()
        r_mag = self.right if isinstance(self.right, int) else self.right.magnitude()
        return (3 * l_mag) + (2 * r_mag)


def do_the_thing(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    final_result = None
    for data_line in data_lines:
        if final_result is None:
            final_result = SnailNumber.from_string(data_line)
        else:
            final_result += SnailNumber.from_string(data_line)

    print(f"Addition results: {final_result}")
    print(f"Resulting magnitude: {final_result.magnitude()}\n#################################\n")


def do_the_thing_2(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    sn_array = []
    for data_line in data_lines:
        sn_array.append(SnailNumber.from_string(data_line))

    max_magnitude = 0
    for i in range(len(sn_array) - 1):
        for j in range(i + 1, len(sn_array)):
            max_magnitude = max(max_magnitude, (sn_array[i] + sn_array[j]).magnitude())
            max_magnitude = max(max_magnitude, (sn_array[j] + sn_array[i]).magnitude())

    print(f"Maximum magnitude from adding any two snail numbers in set: {max_magnitude}\n#################################\n")


def day_18_do(input_file_name: str):
    do_the_thing(input_file_name)


def day_18_do_2(input_file_name: str):
    do_the_thing_2(input_file_name)


day_18_do("day18.txt")
day_18_do_2("day18.txt")
