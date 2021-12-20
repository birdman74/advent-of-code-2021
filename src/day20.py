import copy
import os
from typing import List

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")

DARK = "."
LIGHT = "#"
OPPOSITE_OF = {DARK: LIGHT, LIGHT: DARK}
BINARY_MAPPING = {LIGHT: "1", DARK: "0"}


def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def get_3_x_3(image: List[str], x: int, y: int, space_char: str):
    width = len(image[0])
    height = len(image)

    pixel_str = ""
    if x == 0:
        pixel_str += space(3, space_char)
    elif y == 0:
        pixel_str += space_char + image[x - 1][y: y + 2]
    elif y == width - 1:
        pixel_str += image[x - 1][y - 1: y + 1] + space_char
    else:
        pixel_str += image[x - 1][y - 1: y + 2]

    if y == 0:
        pixel_str += space_char + image[x][y: y + 2]
    elif y == width - 1:
        pixel_str += image[x][y - 1: y + 1] + space_char
    else:
        pixel_str += image[x][y - 1: y + 2]

    if x == height - 1:
        pixel_str += space(3, space_char)
    elif y == 0:
        pixel_str += space_char + image[x + 1][y: y + 2]
    elif y == width - 1:
        pixel_str += image[x + 1][y - 1: y + 1] + space_char
    else:
        pixel_str += image[x + 1][y - 1: y + 2]

    return pixel_str


def convert_pixel(image: List[str], algorithm: str, x: int, y: int, space_char: str):
    pixel_str = get_3_x_3(image, x, y, space_char)
    return algorithm[int(pixel_str.replace(DARK, BINARY_MAPPING[DARK]).replace(LIGHT, BINARY_MAPPING[LIGHT]), 2)]


def calc_new_space_char(current: str, algorithm: str):
    if current == DARK:
        return algorithm[0]
    else:
        return algorithm[int(space(9, "1"), 2)]


def apply_algorithm(image: List[str], algorithm: str, iterations: int):
    image_copy = copy.deepcopy(image)

    for iteration in range(iterations):
        width = len(image_copy[0])
        height = len(image_copy)

        space_char = image_copy[0][0]
        new_space_char = calc_new_space_char(space_char, algorithm)

        new_image = []
        for x in range(height):
            new_line = ""
            for y in range(width):
                new_line += convert_pixel(image_copy, algorithm, x, y, space_char)

            new_image.append(new_line)

        image_copy = buffer_image_with_space(new_image, new_space_char, 3)

    return image_copy


def needed_buffer(min_buffer: int, current_buffer: int):
    return max(0, min(min_buffer, min_buffer - current_buffer))


def buffer_image_with_space(image: List[str], space_char: str, min_buffer: int):
    width = len(image[0])

    empty_space_top = empty_space_bottom = 0
    empty_space_left = empty_space_right = 4
    image_detected_top = False

    for line in image:
        if width == line.count(space_char):
            empty_space_bottom += 1

            if not image_detected_top:
                empty_space_top += 1
        else:
            if not image_detected_top:
                image_detected_top = True

            empty_space_bottom = 0

            empty_space_left = min(empty_space_left,
                                   line.index(OPPOSITE_OF[space_char]))
            empty_space_right = min(empty_space_right,
                                    len(line) - line.rindex(OPPOSITE_OF[space_char]) - 1)

    buffer_top = needed_buffer(min_buffer, empty_space_top)
    buffer_bottom = needed_buffer(min_buffer, empty_space_bottom)
    buffer_left = needed_buffer(min_buffer, empty_space_left)
    buffer_right = needed_buffer(min_buffer, empty_space_right)

    width = width + buffer_left + buffer_right

    new_image = [space(width, space_char) for _ in range(buffer_top)]
    for line in image:
        new_image.append(space(buffer_left, space_char) +
                         line +
                         space(buffer_right, space_char))
    new_image.extend([space(width, space_char) for _ in range(buffer_bottom)])

    return new_image


def print_image(image: List[str]):
    print("Image:")
    [print(s) for s in image]


def space(width: int, space_char: str):
    return "".ljust(width, space_char)


def do_the_thing(input_file_name: str, enhancement_count: int):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    algorithm = data_lines[0]

    space_char = DARK
    image = []
    for i in range(2, len(data_lines)):
        image.append(data_lines[i])

    image = buffer_image_with_space(image, space_char, 3)

    image = apply_algorithm(image, algorithm, enhancement_count)

    print("Final image:")
    print_image(image)

    light_pixel_count = "".join(image).count(LIGHT)

    print(f"Light pixel count after enhancements: {light_pixel_count}\n#################################\n")


def day_20_do(input_file_name: str):
    do_the_thing(input_file_name, 2)
    do_the_thing(input_file_name, 50)


day_20_do("day20.txt")
