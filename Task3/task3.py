import hashlib
import hmac
import random
import sys
from tabulate import tabulate


class MoveRules:
    def __init__(self, moves):
        self.moves = moves

    def determine_winner(self, player_move, computer_move):
        n = len(self.moves)
        idx_player = self.get_index(player_move)
        idx_computer = self.get_index(computer_move)
        if idx_player == idx_computer:
            return "Draw"
        elif idx_player in range((idx_computer + 1) % n, (idx_computer + n // 2 + 1) % n):
            return "Win"
        else:
            return "Lose"

    def get_index(self, move):
        try:
            return int(move)
        except ValueError:
            return self.moves.index(move) + 1


class KeyGenerator:
    @staticmethod
    def generate_key():
        key_length = 256
        return random.randbytes(key_length // 8)


class HMACGenerator:
    @staticmethod
    def generate_hmac(key, message):
        return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()


class Game:
    def __init__(self, moves):
        self.moves = moves
        self.rules = MoveRules(moves)
        self.key = KeyGenerator.generate_key()

    def show_help(self):
        help_table = self.generate_help_table()
        print("Help table:")
        print(tabulate(help_table, headers="firstrow"))

    def generate_help_table(self):
        n = len(self.moves)
        help_table = [["" for _ in range(n + 1)] for _ in range(n + 1)]
        help_table[0][0] = "PC \ User"
        for i in range(1, n + 1):
            help_table[0][i] = f"{self.moves[i - 1]} "
            help_table[i][0] = f"{self.moves[i - 1]} "

        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if i == j:
                    help_table[i][j] = "Draw"
                elif (j - i) % n <= n // 2:
                    help_table[i][j] = "Win"
                else:
                    help_table[i][j] = "Lose"

        return help_table

    def start_game(self):
        print("HMAC:", HMACGenerator.generate_hmac(self.key, "".join(self.moves)))
        print("Available moves:")
        for i, move in enumerate(self.moves, start=1):
            print(f"{i} - {move}")
        print("0 - exit")
        print("? - help")

        while True:
            try:
                choice = input("Enter your move: ")
                if choice == "0":
                    print("Exiting the game.")
                    break
                elif choice == "?":
                    self.show_help()
                    continue
                elif not choice.isdigit() or int(choice) < 0 or int(choice) > len(self.moves):
                    raise ValueError("Invalid move.")
                else:
                    player_move = self.moves[int(choice) - 1]
                    computer_move = random.choice(self.moves)
                    result = self.rules.determine_winner(player_move, computer_move)
                    print(f"Your move: {player_move}")
                    print(f"Computer move: {computer_move}")
                    if result == "Win":
                        print("You win!")
                    elif result == "Lose":
                        print("You lose!")
                    else:
                        print("It's a draw!")
                    print("HMAC key:", self.key.hex())
                    break
            except ValueError as e:
                print(e)


if __name__ == "__main__":
    if len(sys.argv) < 4 or len(set(sys.argv[1:])) != len(sys.argv[1:]):
        print("Error: Incorrect number of arguments or arguments are not unique.")
        print("Example usage: python task3.py 1 2 3")
    else:
        moves = sys.argv[1:]
        game = Game(moves)
        game.start_game()
