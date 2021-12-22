import os
import numpy as np
from typing import List

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")


class Die:
    def __init__(self):
        self.last_roll = 0
        self.roll_count = 0

    def roll(self):
        self.roll_count += 1
        self.last_roll += 1
        return self.last_roll


class Player:
    def __init__(self, initial_position: int, winning_score: int):
        self.score = 0
        self.position = initial_position
        self.winning_score = winning_score

    def take_turn(self, die: Die):
        new_position = (self.position + sum([die.roll() for _ in range(3)])) % 10
        self.position = new_position if new_position != 0 else 10
        self.score += self.position

    def is_a_winner(self):
        return self.score >= self.winning_score


def get_data_lines(input_file_name: str):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    return data_file.read().split("\n")


def do_the_thing(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    winning_score = 1000

    players = [Player(int(data_lines[0].split(": ")[1]), winning_score),
               Player(int(data_lines[1].split(": ")[1]), winning_score)]
    die = Die()

    turn_count = 0
    while len(list(filter(lambda p: p.is_a_winner(), players))) == 0:
        players[turn_count % 2].take_turn(die)
        turn_count += 1

    losers_score = list(filter(lambda p: not p.is_a_winner(), players))[0].score
    result = losers_score * die.roll_count

    print(f"Losing score {losers_score} * die rolls {die.roll_count} = {result}\n#################################\n")


UNIVERSES_PER_ROLL_TOTAL = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
MOVES = {}
P1 = 0
P2 = 1
WINNING_SCORE = 21


class QuantumBoard:
    @staticmethod
    def new_position(old_position: int, roll: int):
        new_position = (old_position + roll) % 10
        return new_position if new_position != 0 else 10


class Game:
    def __init__(self, p1_position: int, p2_position: int, initial_player: int):
        self.initial_positions = [p1_position, p2_position]
        self.player_scores = [0, 0]
        self.initial_player = initial_player
        self.wins = [0, 0]

    def execute_turn(self, universes, p1_pos, p2_pos, p1_score, p2_score, acting_player):
        if acting_player == P1:
            pos = p1_pos
            score = p1_score
        else:
            pos = p2_pos
            score = p2_score

        new_moves = MOVES[pos]
        for new_position, universes_for_roll in new_moves.items():
            new_universes = universes * universes_for_roll
            new_score = score + new_position
            if new_score >= WINNING_SCORE:
                self.wins[acting_player] += new_universes
            elif acting_player == P1:
                self.execute_turn(new_universes, new_position, p2_pos, new_score, p2_score, abs(acting_player - 1))
            else:
                self.execute_turn(new_universes, p1_pos, new_position, p1_score, new_score, abs(acting_player - 1))

    def play_game(self):
        self.execute_turn(1,
                          self.initial_positions[0], self.initial_positions[1],
                          0, 0,
                          self.initial_player)

        return self.wins


def do_the_thing_2(input_file_name: str):
    data_lines = get_data_lines(input_file_name)
    print(f"Number of data lines: {len(data_lines)}")

    for pos in range(1, 11):
        MOVES[pos] = {}
        for roll, universes in UNIVERSES_PER_ROLL_TOTAL.items():
            new_position = QuantumBoard.new_position(pos, roll)
            MOVES[pos][new_position] = universes

    player_1_position = int(data_lines[0].split(": ")[1])
    player_2_position = int(data_lines[1].split(": ")[1])

    wins = Game(player_1_position, player_2_position, P1).play_game()

    print(f"Win Totals: {wins}\n#################################\n")


def day_21_do(input_file_name: str):
    do_the_thing(input_file_name)


def day_21_do_2(input_file_name: str):
    do_the_thing_2(input_file_name)


day_21_do("day21.txt")
day_21_do_2("day21.txt")
