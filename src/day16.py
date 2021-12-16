import math
import os
from typing import List

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")

HEX_TO_BITS = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}

SUM = 0
PRODUCT = 1
MINIMUM = 2
MAXIMUM = 3
LITERAL = 4
GREATER_THAN = 5
LESS_THAN = 6
EQUAL_TO = 7


def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def binary_from_hex(hex_input: str):
    return "".join([HEX_TO_BITS[hex_char] for hex_char in hex_input])


def extract_headers(binary_input: str):
    return int(binary_input[0: 3], 2), int(binary_input[3: 6], 2), binary_input[6:]


def perform_operation(operation: int, numbers: List[int]):
    result = 0
    if operation == SUM:
        result = sum(numbers)
    elif operation == PRODUCT:
        result = math.prod(numbers)
    elif operation == MINIMUM:
        result = min(numbers)
    elif operation == MAXIMUM:
        result = max(numbers)
    elif operation == GREATER_THAN:
        if numbers[0] > numbers[1]:
            result = 1
        else:
            result = 0
    elif operation == LESS_THAN:
        if numbers[0] < numbers[1]:
            result = 1
        else:
            result = 0
    elif operation == EQUAL_TO:
        if numbers[0] == numbers[1]:
            result = 1
        else:
            result = 0

    print(f"Operation result: {result}")
    return result


def process_packet(packet_type_id: str, version: str, binary_data: str):
    version_sum = version
    result = 0

    if LITERAL == packet_type_id:
        binary_groups = []
        last_group_processed = False
        index = 0
        while not last_group_processed:
            group = binary_data[index: index + 5]
            binary_groups.append(group[1:])
            if "0" == group[0]:
                last_group_processed = True
                binary_data = binary_data[index + 5:]
            index += 5

        result = int("".join(binary_groups), 2)
        print(f"literal (in decimal): {result}")
    else:
        results = []
        if "0" == binary_data[0]:
            packet_length = int(binary_data[1: 16], 2)
            print(f"Bit length of sub-packets: {packet_length}")
            binary_data = binary_data[16:]

            processed_binary_data_length = len(binary_data) - packet_length
            while len(binary_data) > processed_binary_data_length:
                version, sub_packet_type_id, binary_data = extract_headers(binary_data)
                binary_data, sub_version_sum, sub_result = process_packet(sub_packet_type_id, version, binary_data)
                results.append(sub_result)
                version_sum += sub_version_sum
        else:
            packet_count = int(binary_data[1: 12], 2)
            print(f"Number of sub-packets: {packet_count}")
            binary_data = binary_data[12:]

            results = []
            while packet_count > 0:
                new_version, sub_packet_type_id, binary_data = extract_headers(binary_data)
                version += new_version
                binary_data, sub_version_sum, sub_result = process_packet(sub_packet_type_id, new_version, binary_data)
                results.append(sub_result)
                version_sum += sub_version_sum
                packet_count -= 1

        result = perform_operation(packet_type_id, results)

    return binary_data, version_sum, result


def do_the_thing(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    hex_input = data_lines[0]
    # hex_input = "D2FE28"
    # hex_input = "38006F45291200"
    # hex_input = "EE00D40C823060"
    # hex_input = "8A004A801A8002F478"
    # hex_input = "620080001611562C8802118E34"
    # hex_input = "C0015000016115A2E0802F182340"
    # hex_input = "A0016C880162017C3686B18A3D4780"
    # hex_input = "C200B40A82"
    # hex_input = "04005AC33890"
    # hex_input = "880086C3E88112"
    # hex_input = "CE00C43D881120"
    # hex_input = "D8005AC2A8F0"
    # hex_input = "F600BC2D8F"
    # hex_input = "9C005AC2F8F0"
    # hex_input = "9C0141080250320F1802104A08"

    version, packet_type_id, binary_data = extract_headers(binary_from_hex(hex_input))

    binary_data, version_sum, result = process_packet(packet_type_id, version, binary_data)

    print(f"Version sum: {version_sum}\n#################################\n")


def do_the_thing_2(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    print(f"place-output-here-2")


def day_16_do(input_file_name: str):
    do_the_thing(input_file_name)


day_16_do("day16.txt")
