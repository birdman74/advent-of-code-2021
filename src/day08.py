import os
from collections import Counter
from typing import List

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")

UNIQUE_SIGNAL_PATTERNS_LENGTH_DICT = {
    2: 1,
    4: 4,
    3: 7,
    7: 8
}


class MyDigit:
    def is_signal_pattern_possible(self, signal_pattern):
        if len(signal_pattern) == self.signal_count:
            return True

    def __init__(self, numeral: int, signal_pattern: str):
        self.numeral_string = str(numeral)
        self.mapped_signal_pattern = ""
        self.signal_pattern = signal_pattern
        self.signal_count = len(self.signal_pattern)


def create_digits():
    digits = []
    for i in range(10):
        if i == 0:
            signal_pattern = "abcefg"
        elif i == 1:
            signal_pattern = "cf"
        elif i == 2:
            signal_pattern = "acdeg"
        elif i == 3:
            signal_pattern = "acdfg"
        elif i == 4:
            signal_pattern = "bcdf"
        elif i == 5:
            signal_pattern = "abdfg"
        elif i == 6:
            signal_pattern = "abdefg"
        elif i == 7:
            signal_pattern = "acf"
        elif i == 8:
            signal_pattern = "abcdefg"
        else:
            signal_pattern = "abcdfg"

        digits.append(MyDigit(i, signal_pattern))

    return digits


def get_data_lines(input_file_name):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def do_the_thing(input_file_name):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    identifiable_digit_count = 0

    # 1 : 2, 4: 4, 7: 3, 8: 7

    for data_line in data_lines:
        in_out = data_line.split("|")
        ov = in_out[1].strip().split()

        identifiable_digit_count += len(list(filter(lambda output_signal: len(output_signal) in {2, 4, 3, 7}, ov)))

    print(f"Identifiable output digits: {identifiable_digit_count}\n#################################\n")


def do_the_thing_2(input_file_name):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    output_value_total = 0
    for data_line in data_lines:
        digits = create_digits()
        signal_mapping = {
            "a": "",
            "b": "",
            "c": "",
            "d": "",
            "e": "",
            "f": "",
            "g": ""
        }

        identified_digits = [False] * 10

        in_out = data_line.split("|")
        signal_patterns = in_out[0].strip().split()
        output_values = in_out[1].strip().split()

        for signal_pattern in signal_patterns:
            if len(signal_pattern) in UNIQUE_SIGNAL_PATTERNS_LENGTH_DICT.keys():
                digit = UNIQUE_SIGNAL_PATTERNS_LENGTH_DICT[len(signal_pattern)]
                digits[digit].mapped_signal_pattern = signal_pattern
                identified_digits[digit] = True
                if found_all_unique_pattern_mappings(identified_digits):
                    break

        signal_mapping_for_a(signal_mapping, digits)
        signal_mapping_for_bcef(signal_mapping, signal_patterns)
        signal_mapping_for_dg(signal_mapping, digits)

        [set_mapped_signal(digit, signal_mapping, signal_patterns) for digit in digits]

        altered_signal_numeral_dict = \
            {"".join(sorted(digit.mapped_signal_pattern)): digit.numeral_string for digit in digits}

        output_value_total += int("".join([altered_signal_numeral_dict[
                                               "".join(sorted(output_signal))] for output_signal in output_values
                                           ]))

    print(f"Total of all output values: {output_value_total}")


def set_mapped_signal(digit: MyDigit, signal_mapping: dict, signals: List[str]):
    digit.mapped_signal_pattern = list(
        filter(lambda signal: sorted(signal) == sorted("".join([signal_mapping[c] for c in digit.signal_pattern])),
               signals))[0]


def signal_mapping_for_dg(signal_mapping: dict, digits: List[MyDigit]):
    bcf_signal = "".join([signal_mapping[x] for x in "bcf"])

    signal_mapping["d"] = "".join(c for c in digits[4].mapped_signal_pattern if c not in bcf_signal)
    signal_mapping["g"] = "".join(c for c in "abcdefg" if c not in "".join(signal_mapping.values()))


def signal_mapping_for_bcef(signal_mapping: dict, unique_signals: List[str]):
    signal_union = "".join(unique_signals)
    signal_counter = Counter(signal_union)

    for signal, count in signal_counter.most_common():
        if count == 4:
            signal_mapping["e"] = signal
        elif count == 6:
            signal_mapping["b"] = signal
        elif count == 8 and signal != signal_mapping["a"]:
            signal_mapping["c"] = signal
        elif count == 9:
            signal_mapping["f"] = signal


def find_unique_signal_counts(signal_sets, unique_signals):
    for signal_set in signal_sets:
        unique_signals.extend(signal_set)
        unique_signals = {i: unique_signals.count(i) for i in unique_signals}.keys()
        if len(unique_signals) == 10:
            break


def signal_mapping_for_a(signal_mapping: dict, digits: List[MyDigit]):
    one_mapping = digits[1].mapped_signal_pattern
    seven_mapping = digits[7].mapped_signal_pattern

    signal_mapping["a"] = "".join(c for c in seven_mapping if c not in one_mapping)


def found_all_unique_pattern_mappings(identified_digits):
    return len(UNIQUE_SIGNAL_PATTERNS_LENGTH_DICT) == len(list(filter(lambda pattern: pattern, identified_digits)))


def day_8_do(input_file_name):
    do_the_thing(input_file_name)


def day_8_do_2(input_file_name):
    do_the_thing_2(input_file_name)


day_8_do("day08.txt")
day_8_do_2("day08.txt")
