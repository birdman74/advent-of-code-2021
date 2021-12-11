import os
from typing import List

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")


def get_data_lines(input_file_name):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def gain_energy(octopi: List[List[int]], x: int, y: int):
    energy = octopi[x][y]
    if energy == 10:
        return

    octopi[x][y] = new_energy = energy + 1
    if new_energy == 10:
        [[gain_energy(octopi, new_x, new_y) for new_y in range(max(0, y - 1), min(y + 2, 10))]
         for new_x in range(max(0, x - 1), min(x + 2, 10))]


def perform_steps(octopi: List[List[int]], steps: int):
    flasher_count = 0

    for _ in range(steps):
        for x in range(len(octopi)):
            for y in range(len(octopi[0])):
                gain_energy(octopi, x, y)

        for x in range(len(octopi)):
            for y in range(len(octopi[0])):
                octopi[x][y] = octopi[x][y] % 10

        iteration_flasher_count = sum(x.count(0) for x in octopi)
        flasher_count += iteration_flasher_count

    return flasher_count


def do_the_thing(input_file_name):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    octopi = []
    for data_line in data_lines:
        octopi.append(list(map(int, data_line)))

    flasher_count = perform_steps(octopi, 100)

    print(f"Total flashers after 100 steps: {flasher_count}\n#################################\n")


def do_the_thing_2(input_file_name):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    octopi = []
    for data_line in data_lines:
        octopi.append(list(map(int, data_line)))

    iteration = flasher_count = 0
    while flasher_count < 100:
        iteration += 1
        flasher_count = perform_steps(octopi, 1)

    print(f"First all flash event on iteration: {iteration}\n#################################\n")


def day_11_do(input_file_name):
    do_the_thing(input_file_name)


def day_11_do_2(input_file_name):
    do_the_thing_2(input_file_name)


day_11_do("day11.txt")
day_11_do_2("day11.txt")
