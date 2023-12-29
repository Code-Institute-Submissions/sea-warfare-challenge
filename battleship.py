import random
from flask import Flask, render_template, request

app = Flask(__name__)

class GameBoard:
    def __init__(self, board):
        self.board = board

    @staticmethod
    def get_letters_to_numbers():
        letters_to_numbers = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
        return letters_to_numbers

    def print_board(self):
        board_str = "  A B C D E F G H\n  +-+-+-+-+-+-+-+"
        for i, row in enumerate(self.board, start=1):
            board_str += f"\n{i}|{'|'.join(row)}|"
        return board_str

class Battleship:
    def __init__(self, board):
        self.board = board

    def create_ships(self):
        for i in range(5):
            x_row, y_column = random.randint(0, 7), random.randint(0, 7)
            while self.board[x_row][y_column] == "X":
                x_row, y_column = random.randint(0, 7), random.randint(0, 7)
            self.board[x_row][y_column] = "X"
        return self.board

    @staticmethod
    def get_user_input():
        try:
            x_row = request.form.get("row")
            while x_row not in '12345678':
                print('Not an appropriate choice, please select a valid row')
                x_row = request.form.get("row")

            y_column = request.form.get("column").upper()
            while y_column not in "ABCDEFGH":
                print('Not an appropriate choice, please select a valid column')
                y_column = request.form.get("column").upper()
            return int(x_row) - 1, GameBoard.get_letters_to_numbers()[y_column]

        except (ValueError, KeyError):
            print("Not a valid input")
            return Battleship.get_user_input()

    def computer_guess(self):
        x_row = random.randint(0, 7)
        y_column = random.randint(0, 7)
        return x_row, y_column

    def count_hit_ships(self):
        hit_ships = sum(row.count("X") for row in self.board)
        return hit_ships

@app.route('/', methods=['GET', 'POST'])
def run_game():
    if request.method == 'POST':
        user_guess_board.print_board()
        user_x_row, user_y_column = Battleship.get_user_input()

        while user_guess_board.board[user_x_row][user_y_column] in {"-", "X"}:
            print("You guessed that one already")
            user_x_row, user_y_column = Battleship.get_user_input()

        if computer_board.board[user_x_row][user_y_column] == "X":
            print("You sunk 1 of my battleships!")
            user_guess_board.board[user_x_row][user_y_column] = "X"
        else:
            print("You missed my battleship!")
            user_guess_board.board[user_x_row][user_y_column] = "-"

        if Battleship(user_guess_board.board).count_hit_ships() == 5:
            print("You hit all 5 battleships!")
            return "You hit all 5 battleships!"
        else:
            turns -= 1
            print(f"You have {turns} turns remaining")

            # Computer's turn
            computer_x_row, computer_y_column = Battleship(computer_board.board).computer_guess()
            print(f"The computer guessed: {chr(computer_y_column + ord('A'))}{computer_x_row + 1}")

            if user_guess_board.board[computer_x_row][computer_y_column] == "X":
                print("The computer sunk one of your battleships!")
            else:
                print("The computer missed your battleship!")

    return render_template('index.html', board=user_guess_board.print_board())

if __name__ == '__main__':
    computer_board = GameBoard([[" "] * 8 for _ in range(8)])
    user_guess_board = GameBoard([[" "] * 8 for _ in range(8)])
    Battleship(computer_board.board).create_ships()

    app.run(debug=True)
