import os
from collections import Counter


MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")


# class Coordinate:
# 6,5,4,3,2,1,0 -> 6 + new 8

def process_fish(day: int):
    if day == 0:
        return 6
    else:
        return day - 1


def get_data_lines(input_file_name):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def do_the_thing(input_file_name, num_days):
    data_lines = get_data_lines(input_file_name)

    # fish_counters = list(map(int, data_lines[0].split(",")))
    fish_counters = [3, 4, 3, 1, 2]
    # print(f"Initial state: {fish_counters}")

    for i in range(num_days):
        num_new_fish = Counter(fish_counters).get(0)
        fish_counters = [process_fish(fish) for fish in fish_counters]
        if num_new_fish is not None:
            fish_counters.extend([8 for _ in range(num_new_fish)])
        # print(f"After {i+1} days: {fish_counters}")

    print(f"Total number of fish after {num_days} days: {len(fish_counters)}\n#################################\n")


def day_6_do(input_file_name):
    do_the_thing(input_file_name, 80)


def do_the_thing_2(input_file_name, num_days):
    NEWBORN_FISH_DAYS = 8

    data_lines = get_data_lines(input_file_name)

    initial_fish_counters = list(map(int, data_lines[0].split(",")))
    # initial_fish_counters = [3, 4, 3, 1, 2]
    fish_day_counts = Counter(initial_fish_counters)
    fish_day_count_tracker = [fish_day_counts.get(i) if fish_day_counts.get(i) is not None else 0 for i in range(NEWBORN_FISH_DAYS + 1)]
    print(f"Initial state: {fish_day_count_tracker}")

    for i in range(num_days):
        new_fish_count = fish_day_count_tracker[0]
        for j in range(NEWBORN_FISH_DAYS):
            fish_day_count_tracker[j] = fish_day_count_tracker[j + 1]
        fish_day_count_tracker[6] = fish_day_count_tracker[6] + new_fish_count
        fish_day_count_tracker[NEWBORN_FISH_DAYS] = new_fish_count
        print(f"After {i+1} days: {fish_day_count_tracker}")

    print(f"Total number of fish after {num_days} days: {sum(fish_day_count_tracker)}\n#################################\n")


def day_6_do_2(input_file_name):
    do_the_thing_2(input_file_name, 256)


day_6_do("day06.txt")
day_6_do_2("day06.txt")
