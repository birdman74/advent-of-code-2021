import copy
import os
from typing import List
import numpy as np

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")

Z_ROTATION = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
Y_ROTATION = [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]
X_ROTATION = [[1, 0, 0], [0, 0, -1], [0, 1, 0]]


def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


class Scanner:
    def __init__(self):
        self.rotation = 0
        self.beacons = []
        self.beacon_rotations = []
        self.normalized_beacons = []
        self.matched = False
        self.used_for_normalization = False
        self.position = [0, 0, 0]

    def normalize_rotation(self, rotation_index: int, beacon_index: int):
        positions = copy.deepcopy(self.beacon_rotations[rotation_index])
        normalizer = self.offsets(positions, beacon_index)

        for i in range(len(positions)):
            positions[i] = tuple(np.add(positions[i], normalizer))

        return positions

    @staticmethod
    def offsets(positions: List[List[int]], beacon_index: int):
        return [-1 * i for i in positions[beacon_index]]

    def populate_new_beacon_rotations_entry_with_turn(self, positions: List[List[int]], axis: str, skips: int = 0):
        def ninety(p, ninety_axis):
            if "Z" == ninety_axis:
                return tuple(np.dot(Z_ROTATION, p))
            elif "Y" == ninety_axis:
                return tuple(np.dot(Y_ROTATION, p))
            else:
                return tuple(np.dot(X_ROTATION, p))

        self.beacon_rotations.append([])
        new_pos_list = self.beacon_rotations[len(self.beacon_rotations) - 1]
        for position in positions:
            new_pos = ninety(position, axis)
            for _ in range(skips):
                new_pos = ninety(new_pos, axis)

            new_pos_list.append(new_pos)

    def calculate_all_rotations(self):
        def cartwheel(axis: str):
            [self.populate_new_beacon_rotations_entry_with_turn(
                self.beacon_rotations[len(self.beacon_rotations) - 1], axis) for _ in range(3)]

        def last_beacon_rotation():
            return self.beacon_rotations[len(self.beacon_rotations) - 1]

        # 1 / 24
        self.beacon_rotations.append(copy.deepcopy(self.beacons))
        # 3/4 cartwheel pointing down Z axis : 4 / 24
        cartwheel("Z")
        # turn 90 degrees to point down X axis 5 / 24
        self.populate_new_beacon_rotations_entry_with_turn(last_beacon_rotation(), "Y")
        # 3/4 cartwheel pointing down X axis : 8 / 24
        cartwheel("X")
        # turn 90 degrees to point down Z axis: 9 / 24
        self.populate_new_beacon_rotations_entry_with_turn(last_beacon_rotation(), "Y")
        # 3/4 cartwheel pointing down Z axis : 12 / 24
        cartwheel("Z")
        # turn 90 degrees to point down Z axis : 13 / 24
        self.populate_new_beacon_rotations_entry_with_turn(last_beacon_rotation(), "Y")
        # 3/4 cartwheel pointing down Z axis : 16 / 24
        cartwheel("X")
        # turn 90 degrees to point down Y axis : 17 / 24
        self.populate_new_beacon_rotations_entry_with_turn(last_beacon_rotation(), "Z")
        # 3/4 cartwheel pointing down Y axis : 20 / 24
        cartwheel("Y")
        # turn 180 degrees to point down Y axis 21 / 24
        self.populate_new_beacon_rotations_entry_with_turn(last_beacon_rotation(), "Z", skips=1)
        # 3/4 cartwheel pointing down Y axis : 24 sets
        cartwheel("Y")

    def find_n_matches(self, other: "Scanner", match_count: int):
        for my_rotation_index in range(len(self.beacon_rotations)):
            for other_rotation_index in range(len(other.beacon_rotations)):
                for my_norm_index in range(len(self.beacon_rotations[my_rotation_index])):
                    my_norms = self.normalize_rotation(my_rotation_index, my_norm_index)
                    for other_norm_index in range(len(other.beacon_rotations[other_rotation_index])):
                        other_norms = other.normalize_rotation(other_rotation_index, other_norm_index)
                        common_beacons = list(set(my_norms).intersection(set(other_norms)))
                        if len(common_beacons) >= match_count:
                            other.position = list(np.add(self.position,
                                                         list(np.subtract(
                                                             self.beacon_rotations[my_rotation_index][my_norm_index],
                                                             other.beacon_rotations[other_rotation_index][
                                                                 other_norm_index]))))

                            return True, [my_rotation_index, my_norm_index, other_rotation_index, other_norm_index]

        return False, None


def do_the_thing(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    scanners: List[Scanner] = []
    scanner_overlap_map = {}
    for data_line in data_lines:
        if data_line.strip() == "":
            continue
        elif data_line[0:3] == "---":
            scanners.append(Scanner())
        else:
            scanners[len(scanners) - 1].beacons.append(tuple(map(int, data_line.split(","))))
            scanner_overlap_map[len(scanners) - 1] = []

    scanners[0].beacon_rotations = [copy.deepcopy(scanners[0].beacons)]
    scanners[0].normalized_beacons = [list(x) for x in scanners[0].beacons]
    scanners[0].matched = True
    while len(list(filter(lambda s: not s.matched, scanners))) > 0:
        for i in range(len(scanners)):
            if scanners[i].matched and not scanners[i].used_for_normalization:
                scanners[i].used_for_normalization = True
                for j in range(len(scanners)):
                    if not scanners[j].matched:
                        if len(scanners[j].beacon_rotations) == 0:
                            scanners[j].calculate_all_rotations()

                        print(f"Comparing scanners {i} and {j}")
                        found_match, indices = scanners[i].find_n_matches(scanners[j], 12)
                        if found_match:
                            print("Matching criteria met, processing beacon positions")
                            scanners[j].matched = True
                            scanners[j].beacon_rotations[0] = scanners[j].beacon_rotations[indices[2]]
                            scanners[j].beacon_rotations = [scanners[j].beacon_rotations[indices[2]]]

                            scanners[j].normalized_beacons = copy.deepcopy(scanners[j].beacon_rotations[0])
                            shift = np.subtract(scanners[i].normalized_beacons[indices[1]],
                                                scanners[j].normalized_beacons[indices[3]]).tolist()

                            scanners[j].normalized_beacons = \
                                np.add(scanners[j].normalized_beacons, shift).tolist()
                        else:
                            print("Matching criteria not met")

    total_beacons = [tuple(b) for s in scanners for b in s.normalized_beacons]

    print(f"Number of beacons: {len(set(total_beacons))}\n#################################\n")

    max_manhattan = 0
    for i in range(len(scanners)):
        for j in range(i + 1, len(scanners)):
            max_manhattan = max(max_manhattan,
                                sum([abs(v1-v2) for v1, v2 in zip(scanners[i].position, scanners[j].position)]))

    print(f"Max manhattan distance between scanners: {max_manhattan}\n#################################\n")


def day_19_do(input_file_name: str):
    do_the_thing(input_file_name)


day_19_do("day19.txt")
