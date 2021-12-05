import os

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, "..")
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, "input")


class BingoCard:
    BLOT = -1

    def __init__(self, string_rows):
        self.num_values = []
        self.num_blots = 0
        for string_row in string_rows:
            string_array = string_row.split()
            self.num_values.append(list(map(int, string_array)))

    def cross_off(self, called_number):
        for row in self.num_values:
            if called_number in row:
                self.num_blots += 1
                row[row.index(called_number)] = self.BLOT
                return True

    def is_a_winner(self):
        for row in self.num_values:
            if sum(row) == 5 * self.BLOT:
                print(f"Bingo!!!")
                return True

        for i in range(len(self.num_values[0])):
            if sum(list(map(lambda j: self.num_values[j][i], range(len(self.num_values[0]))))) == 5 * self.BLOT:
                print(f"Bingo!!!")
                return True

    def score(self):
        score = self.num_blots
        for row in self.num_values:
            score += sum(row)

        return score

    def print_card(self):
        for row in self.num_values:
            print(row)


def score_for_winner_number(input_file_name, winner_num):
    input_file = os.path.join(INPUT_SOURCE_DIR, input_file_name)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    data_lines = data_file.read().split("\n")

    called_nums = list(map(int, data_lines[0].split(",")))

    cards = []

    for row_num in [x for x in range(1, len(data_lines)) if x % 6 == 2]:
        data_line = data_lines[row_num].strip()
        if data_line == "":
            continue

        cards.append(BingoCard(data_lines[row_num:row_num+5]))

    total_cards = non_winners_still_left = len(cards)

    print(f"number of bingo cards: {non_winners_still_left}")

    for called_num in called_nums:
        print(f"Calling for number: {called_num}")
        for card in cards:
            winning_cards_on_this_call = []
            if card.cross_off(called_num):
                if card.is_a_winner():
                    print(f"We have a winner: \n")
                    card.print_card()
                    winning_cards_on_this_call.append(card)
                    new_total_cards = len(cards) - len(winning_cards_on_this_call)
                    if total_cards - new_total_cards == winner_num:
                        print(f"\nWinning score: {card.score() * called_num}\n##############################\n")
                        return
            if len(winning_cards_on_this_call) > 0:
                cards = list(set(cards) - set(winning_cards_on_this_call))


def day_4_do(input_file_name):
    score_for_winner_number(input_file_name, 1)


def day_4_do_2(input_file_name):
    score_for_winner_number(input_file_name, 100)


day_4_do("day04.txt")
day_4_do_2("day04.txt")
