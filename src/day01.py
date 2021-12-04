import os

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, 'input')


def day_1_depths(input_file_name):
    compare_array_ints(input_file_name, 1)


def day_1_depth_triplets(input_file_name):
    compare_array_ints(input_file_name, 3)


def compare_array_ints(input_file_name, offset):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    s_depths = data_file.read().split("\n")
    depths_array = list(map(int, s_depths))

    num_increases = 0

    for i in range(len(depths_array) - offset):
        if depths_array[i] < depths_array[i + offset]:
            num_increases += 1

    print(f"Number of increases: {num_increases}\n############################\n")


day_1_depths("day01.txt")
day_1_depth_triplets("day01.txt")
