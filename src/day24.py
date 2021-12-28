import os

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")


def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def inp(registers: dict, var_1: str, var_2: int):
    registers[var_1] = var_2


def add(registers: dict, var_1: str, var_2: str):
    if var_2.strip("-").isnumeric():
        registers[var_1] += int(var_2)
    else:
        registers[var_1] += registers[var_2]


def mul(registers: dict, var_1: str, var_2: str):
    if var_2.strip("-").isnumeric():
        registers[var_1] *= int(var_2)
    else:
        registers[var_1] *= registers[var_2]

def div(registers: dict, var_1: str, var_2: str):
    if var_2.strip("-").isnumeric():
        registers[var_1] //= int(var_2)
    else:
        registers[var_1] //= registers[var_2]


def mod(registers: dict, var_1: str, var_2: str):
    if var_2.strip("-").isnumeric():
        registers[var_1] %= int(var_2)
    else:
        registers[var_1] %= registers[var_2]


def eql(registers: dict, var_1: str, var_2: str):
    if var_2.strip("-").isnumeric():
        comparator = int(var_2)
    else:
        comparator = registers[var_2]

    if registers[var_1] == comparator:
        registers[var_1] = 1
    else:
        registers[var_1] = 0


INSTRUCTIONS = {"inp": inp, "add": add, "mul": mul, "div": div, "mod": mod, "eql": eql}
INPUT_SERIAL_NUMBER = "INPUT NUMBER"

ZDIV = []
XADD = []
YADD = []

VISITED_STATES = {}


def find_serial_number(level_count: int, level: int = 1, serial_num: str = "", z: int = 0):
    if level not in VISITED_STATES:
        VISITED_STATES[level] = []

    for w in range(9, 0, -1):
        new_serial_num = serial_num + str(w)

        x = (z % 26) + XADD[level - 1] != w
        new_z = z // ZDIV[level - 1]

        new_z = (26 * new_z) + w + YADD[level - 1] if x else new_z

        if new_z in VISITED_STATES[level]:
            continue
        else:
            VISITED_STATES[level].append(new_z)

        if level < level_count:
            find_serial_number(level_count, level + 1, new_serial_num, new_z)
        elif new_z == 0:
            print(f" Serial Number: {new_serial_num}")
            exit()
        else:
            print(f"{new_serial_num}")


def do_the_thing(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    for i in range(len(data_lines)):
        data_line = data_lines[i]
        data = data_line.split()
        if 3 == len(data):
            input_2 = data[2]
        else:
            input_2 = INPUT_SERIAL_NUMBER

        if i % 18 == 4:
            ZDIV.append(int(input_2))
        elif i % 18 == 5:
            XADD.append(int(input_2))
        elif i % 18 == 15:
            YADD.append(int(input_2))

    find_serial_number(14)


def day_24_do(input_file_name: str):
    do_the_thing(input_file_name)


day_24_do("day24.txt")

# This was never going to finish for MAX (part 1), but could have found MIN with some adjusting
# Instead, used base 26 math to match up input values to solve manually
#  1/ 15/13  w0 + 13
#  1/ 10/16  w1 + 16
#  1/ 12/ 2  w2 +  2
#  1/ 10/ 8  w3 +  8
#  1/ 14/11  w4 + 11
# 26/-11/ 6  w5 + 11 - 11   (w4 = w5)
#  1/ 10/12  w6 + 12
# 26/-16/ 2  w7 + 16 - 12   (w6 = w7 + 4)
# 26/ -9/ 2  w8 +  9 - 8    (w3 = w8 + 1)
#  1/ 11/15  w9 + 15
# 26/ -8/ 1  w10 + 8 - 15   (w9 = w10 - 7)
# 26/ -8/10  w11 + 8 - 2    (w2 = w11 + 6)
# 26/-10/14  w12 + 10 - 16  (w1 = w12 - 6)
# 26/ -9/10  w13 + 9 - 13   (w0 = w13 - 4)

# 01234567890123
# 53999995829399 (MAX)
# 11721151118175 (MIN)