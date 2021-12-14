import os
from collections import Counter

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")


def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def alter_polymer(polymer: str, new_component: str, index: int):
    new_polymer = polymer[0: index] + new_component + polymer[index - len(polymer):]
    return new_polymer


def do_the_thing(input_file_name: str, iteration_count: int):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    rules = {}
    polymer = ""
    polymer_recorded = False

    for data_line in data_lines:
        if not polymer_recorded:
            polymer = data_line
            polymer_recorded = True
        else:
            if data_line.strip() != "":
                rule_parts = data_line.split(" -> ")
                rules[rule_parts[0]] = rule_parts[1]

    # print(f"Initial polymer: {polymer}")
    for step in range(iteration_count):
        polymer_length = len(polymer)
        for i in range(polymer_length - 1):
            duo_start = polymer_length - i - 2
            polymer = alter_polymer(polymer, rules[polymer[duo_start: duo_start + 2]], duo_start + 1)

        # print(f"New polymer after {step + 1} steps: {polymer}")

    c = Counter(polymer)

    print(f"Difference between most and least common elements: {c.most_common()[0][1] - c.most_common()[len(c) - 1][1]}\n#################################\n")


def update_new_duo_counts(new_duo_counts: {}, duo: str, new_count: int):
    old_duo_count = new_duo_counts.get(duo)
    if old_duo_count is None:
        new_duo_counts[duo] = new_count
    else:
        new_duo_counts[duo] = new_duo_counts[duo] + new_count


def update_element_counts(element_counts: {}, element: str, new_count: int):
    current_element_count = element_counts.get(element)
    if current_element_count is None:
        element_counts[element] = new_count
    else:
        element_counts[element] = element_counts[element] + new_count


def do_the_thing_2(input_file_name, iteration_count: int):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    rules = {}
    element_counts = {}
    polymer = ""
    polymer_recorded = False

    for data_line in data_lines:
        if not polymer_recorded:
            polymer = data_line
            polymer_recorded = True
            for ch in polymer:
                found_ch = element_counts.get(ch)
                if found_ch is None:
                    element_counts[ch] = 1
                else:
                    element_counts[ch] = element_counts[ch] + 1
        else:
            if data_line.strip() != "":
                rule_parts = data_line.split(" -> ")
                rules[rule_parts[0]] = [rule_parts[1], 0]

    # parse initial polymer for duo counts
    for i in range(len(polymer) - 1):
        duo = polymer[i: i+2]
        previous_duo_count = rules[duo][1]
        rules[duo] = [rules[duo][0], previous_duo_count + 1]

    # update duo counts for each iteration given insertion rules
    for i in range(iteration_count):
        new_duo_counts = {}
        for key in rules.keys():
            [new_single, new_count] = rules[key]
            if new_count > 0:
                new_duo_1 = key[0] + new_single
                new_duo_2 = new_single + key[1]

                update_new_duo_counts(new_duo_counts, key, -1 * new_count)
                update_new_duo_counts(new_duo_counts, new_duo_1, new_count)
                update_new_duo_counts(new_duo_counts, new_duo_2, new_count)

                update_element_counts(element_counts, new_single, new_count)

        for key in new_duo_counts.keys():
            rules[key] = [rules[key][0], rules[key][1] + new_duo_counts[key]]

    print(f"Difference between most and least common elements: {max(element_counts.values()) - min(element_counts.values())}\n#################################\n")


def day_14_do(input_file_name):
    do_the_thing(input_file_name, 10)


def day_14_do_2(input_file_name):
    do_the_thing_2(input_file_name, 40)


day_14_do("day14.txt")
day_14_do_2("day14.txt")
