import os
import statistics

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")

DELIMS = {"{": "}", "(": ")", "[": "]", "<": ">"}
DELIM_SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}
AUTO_COMPLETE_SCORES = {")": 1, "]": 2, "}": 3, ">": 4}


def get_data_lines(input_file_name):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def start_chunk(line: str, ch: str, chunk_start_index: int):
    i = chunk_start_index + 1
    complete_with_composite = ""
    while i < len(line):
        new_ch = line[i]
        # end a chunk legally
        if new_ch == DELIMS[ch]:
            return new_ch, i, False, None
        # start a new chunk
        elif new_ch in DELIMS.keys():
            chunk_end_ch, chunk_end_index, illegal, complete_with = start_chunk(line, new_ch, i)

            if complete_with is not None:
                complete_with_composite += complete_with

            if illegal is not None and illegal:
                return chunk_end_ch, chunk_end_index, illegal, None
            else:
                i = chunk_end_index
        # line is illegal
        elif new_ch in DELIMS.values():
            return new_ch, i, True, None
        # line runs out, calculate autocomplete for this chunk
        else:
            return new_ch, i, None, DELIMS[ch]

        i += 1

    # ran off the end of the line (there be dragons here)
    return "", i, None, complete_with_composite + DELIMS[ch]


def line_corrupted_score(line: str):
    i = 0
    while i < len(line):
        ch = line[i]
        if ch in DELIMS.keys():
            chunk_end_ch, chunk_end_index, illegal, complete_with = start_chunk(line, ch, i)
            if illegal is not None and illegal:
                return DELIM_SCORES[chunk_end_ch], None
            else:
                i = chunk_end_index

        i += 1

    return 0, complete_with


def do_the_thing(input_file_name):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    syntax_error_score = 0
    for data_line in data_lines:
        line_syntax_error_score, _ = line_corrupted_score(data_line)
        syntax_error_score += line_syntax_error_score

    print(f"Syntax error score: {syntax_error_score}\n#################################\n")


def auto_complete_score(line: str):
    illegal_score, complete_with = line_corrupted_score(line)

    score = 0
    if complete_with is not None:
        for ch in complete_with:
            score = score * 5 + AUTO_COMPLETE_SCORES[ch]

    return score


def do_the_thing_2(input_file_name):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    auto_complete_line_scores = []
    for data_line in data_lines:
        auto_complete_line_score = auto_complete_score(data_line)
        if auto_complete_line_score > 0:
            auto_complete_line_scores.append(auto_complete_line_score)

    print(f"Auto complete score: {statistics.median(sorted(auto_complete_line_scores))}")


def day_10_do(input_file_name):
    do_the_thing(input_file_name)


def day_10_do_2(input_file_name):
    do_the_thing_2(input_file_name)


day_10_do("day10.txt")
day_10_do_2("day10.txt")
