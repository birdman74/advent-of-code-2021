import os

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, 'input')


def day_2_do(input_file_name):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    directions = data_file.read().split("\n")

    horizontal_position = 0
    depth = 0

    for direction in directions:
        pieces = direction.split(" ")
        command = pieces[0]
        unit = int(pieces[1])

        if command == 'forward':
            horizontal_position += unit
        elif command == 'down':
            depth += unit
        elif command == 'up':
            depth -= unit

    print(f"Final horizontal position: {horizontal_position}")
    print(f"Final depth: {depth}")

    print(f"Answer: {horizontal_position * depth}\n############################\n")


def day_2_do_2(input_file_name):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    input_file = open(input_file)
    directions = input_file.read().split("\n")

    aim = 0
    horizontal_position = 0
    depth = 0

    for direction in directions:
        pieces = direction.split(" ")
        command = pieces[0]
        unit = int(pieces[1])

        if command == 'forward':
            horizontal_position += unit
            depth = depth + (aim * unit)
        elif command == 'down':
            aim += unit
        elif command == 'up':
            aim -= unit

    print(f"Final horizontal position: {horizontal_position}")
    print(f"Final depth: {depth}")

    print(f"Answer: {horizontal_position * depth}\n############################\n")


day_2_do("day02.txt")
day_2_do_2("day02.txt")
