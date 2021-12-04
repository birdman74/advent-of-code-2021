import os

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")

ZEROS_INDEX = 0
ONES_INDEX = 1


def day_3_do(input_file_name):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    binary_values = data_file.read().split("\n")

    binary_value_length = len(binary_values[0])

    zero_one_counts = [[0 for _ in range(2)] for _ in range(binary_value_length)]
    for i in range(len(binary_values)):
        binary_value = binary_values[i]

        for j in range(binary_value_length):
            if binary_value[j] == "0":
                zero_one_counts[j][ZEROS_INDEX] += 1
            else:
                zero_one_counts[j][ONES_INDEX] += 1

    print(f"zero_one_counts: {zero_one_counts}")

    gamma_rate_string = ""
    epsilon_rate_string = ""

    for counts in zero_one_counts:
        if counts[ZEROS_INDEX] > counts[ONES_INDEX]:
            gamma_rate_string += "0"
            epsilon_rate_string += "1"
        else:
            gamma_rate_string += "1"
            epsilon_rate_string += "0"

    print(f"gamma_rate: {gamma_rate_string}")
    print(f"epsilon_rate :{epsilon_rate_string}")

    gamma_rate = int(gamma_rate_string, 2)
    epsilon_rate = int(epsilon_rate_string, 2)

    power_consumption = gamma_rate * epsilon_rate

    print(f"power_consumption: {power_consumption}\n############################\n")


def day_3_do_2(input_file_name):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    binary_values = data_file.read().split("\n")

    oxygen_generator_rating = filter_binary_values(binary_values, 0, "most")
    c02_scrubber_rating = filter_binary_values(binary_values, 0, "least")
    
    print(f"oxygen generator rating: {oxygen_generator_rating}")
    print(f"C02 scrubber rating: {c02_scrubber_rating}")

    life_support_rating = int(oxygen_generator_rating, 2) * int(c02_scrubber_rating, 2)

    print(f"life support rating: {life_support_rating}\n############################\n")


def filter_binary_values(binary_values, position, bit_criteria):
    most_common_bit = find_most_common_bit_value(binary_values, position)

    if bit_criteria == "most":
        binary_values = list(filter(lambda binary_value: binary_value[position] == most_common_bit, binary_values))
    else:
        binary_values = list(filter(lambda binary_value: binary_value[position] != most_common_bit, binary_values))

    if len(binary_values) == 1:
        return binary_values[0]
    else:
        return filter_binary_values(binary_values, position+1, bit_criteria)


def find_most_common_bit_value(binary_values, position):
    zero_count = len(list(filter(lambda binary_value: binary_value[position] == "0", binary_values)))

    if zero_count > (len(binary_values) / 2):
        return "0"
    else:
        return "1"


day_3_do("day03.txt")
day_3_do_2("day03.txt")
