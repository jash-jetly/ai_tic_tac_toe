import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe")

        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"  # Player X starts
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.scoreboard = {"X": 0, "O": 0}

        self.create_widgets()
        self.update_scoreboard()

    def create_widgets(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.master, text=" ", font=('Arial', 40), width=5, height=2,
                                   command=lambda r=row, c=col: self.player_move(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

        self.status_label = tk.Label(self.master, text="Player X's turn")
        self.status_label.grid(row=3, column=0, columnspan=3)

    def player_move(self, row, col):
        if self.board[row][col] == " " and self.current_player == "X":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)

            if self.check_winner():
                self.update_score(self.current_player)
                self.end_game(f"Player {self.current_player} wins!")
                return
            elif self.is_board_full():
                self.end_game("It's a tie!")
                return

            self.current_player = "O"  # Switch to AI
            self.status_label.config(text="AI's turn")
            self.master.after(500, self.ai_move)  # Delay AI's move

    def ai_move(self):
        # AI first tries to win
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == " ":
                    self.board[r][c] = "O"  # Simulate the move
                    if self.check_winner():
                        self.buttons[r][c].config(text="O")
                        self.update_score("O")
                        self.end_game("Player O wins!")
                        return
                    self.board[r][c] = " "  # Reset if it doesn't lead to a win

        # AI then tries to block player X from winning
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == " ":
                    self.board[r][c] = "X"  # Simulate the player's move
                    if self.check_winner():
                        self.board[r][c] = "O"  # Block the winning move
                        self.buttons[r][c].config(text="O")
                        break  # Break out of the loop to prevent multiple AI moves
                    self.board[r][c] = " "  # Reset if it doesn't lead to a win
            else:
                continue
            break  # Break outer loop if the AI has made a move
        else:
            # If neither winning nor blocking, take any available space
            row, col = self.get_ai_move()
            if row is not None and col is not None:
                self.board[row][col] = "O"
                self.buttons[row][col].config(text="O")

        # Check for win or tie after AI move
        if self.check_winner():
            self.update_score("O")
            self.end_game("Player O wins!")
            return
        elif self.is_board_full():
            self.end_game("It's a tie!")
            return

        self.current_player = "X"  # Switch back to player
        self.status_label.config(text="Player X's turn")

    def get_ai_move(self):
        available_moves = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "]
        return random.choice(available_moves) if available_moves else (None, None)

    def check_winner(self):
        # Check rows, columns, and diagonals for a win
        for row in self.board:
            if row[0] == row[1] == row[2] != " ":
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return True
        return False

    def is_board_full(self):
        return all(cell != " " for row in self.board for cell in row)

    def update_score(self, winner):
        self.scoreboard[winner] += 1
        self.update_scoreboard()

    def update_scoreboard(self):
        self.status_label.config(text=f"Score - Player X: {self.scoreboard['X']} | Player O: {self.scoreboard['O']} | Turn: {'X' if self.current_player == 'X' else 'O'}")

    def end_game(self, message):
        if messagebox.askyesno("Game Over", f"{message}\nDo you want to play again?"):
            self.reset_game()
        else:
            self.master.quit()

    def reset_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=" ")
        self.status_label.config(text="Player X's turn")
        self.update_scoreboard()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
