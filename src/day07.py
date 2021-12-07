import os
from collections import Counter


MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")


def get_data_lines(input_file_name):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def do_the_thing(input_file_name, part_num):
    data_lines = get_data_lines(input_file_name)

    # hp = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    hp = list(map(int, data_lines[0].split(",")))

    left = min(hp)
    right = max(hp)
    span = right - left + 1

    if part_num == 1:
        gas_totals = [sum([abs(x-y) for x in hp]) for y in range(left, right + 1)]
    else:
        gas_totals = [sum([sum(range(abs(x-y) + 1)) for x in hp]) for y in range(left, right + 1)]


    optimal_position = gas_totals.index(min(gas_totals))

    print(f"Optimal position: {optimal_position}\nGas expended: {min(gas_totals)}\n#################################\n")


def day_7_do(input_file_name):
    do_the_thing(input_file_name, 1)


def day_7_do_2(input_file_name):
    do_the_thing(input_file_name, 2)


day_7_do("day07.txt")
day_7_do_2("day07.txt")
