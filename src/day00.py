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


def do_the_thing(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    for data_line in data_lines:
        print(f"data line: {data_line}")

    print(f"\n#################################\n")


def do_the_thing_2(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    for data_line in data_lines:
        print(f"data line: {data_line}")

    print(f"\n#################################\n")


def day_0_do(input_file_name: str):
    do_the_thing(input_file_name)


def day_0_do_2(input_file_name: str):
    do_the_thing_2(input_file_name)


day_0_do("day00.txt")
day_0_do_2("day00.txt")
