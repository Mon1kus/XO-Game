import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Крестики-нолики")

        self.current_player = "X"
        self.computer_player = None
        self.board = [[" " for _ in range(3)] for _ in range(3)]

        self.create_widgets()
        self.show_start_menu()

    def create_widgets(self):
        # Создание игрового поля
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(self.master, text=" ", font=('Arial', 20), width=5, height=2,
                              command=lambda i=i, j=j: self.on_click(i, j))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

        # Панель управления
        self.control_frame = tk.Frame(self.master)
        self.control_frame.grid(row=3, column=0, columnspan=3, pady=10)

        self.status_label = tk.Label(self.control_frame, text="", font=('Arial', 12))
        self.status_label.pack()

        self.restart_btn = tk.Button(self.control_frame, text="Новая игра", command=self.show_start_menu)
        self.restart_btn.pack(pady=5)

    def show_start_menu(self):
        # Меню выбора режима игры
        self.clear_board()

        start_window = tk.Toplevel(self.master)
        start_window.title("Выбор режима")

        tk.Label(start_window, text="Выберите режим игры:").pack(pady=10)

        tk.Button(start_window, text="Два игрока",
                 command=lambda: self.start_game(start_window, False)).pack(pady=5)
        tk.Button(start_window, text="Против компьютера",
                 command=lambda: self.start_game(start_window, True)).pack(pady=5)

    def start_game(self, start_window, vs_computer):
        start_window.destroy()
        self.clear_board()
        self.computer_player = "O" if vs_computer else None
        self.update_status()

        if vs_computer and self.current_player == self.computer_player:
            self.computer_move()

    def on_click(self, row, col):
        if self.board[row][col] == " " and not self.check_game_over():
            self.make_move(row, col)

            if not self.check_game_over() and self.computer_player:
                self.master.after(500, self.computer_move)

    def computer_move(self):
        # Простой ИИ: сначала пытается победить, потом блокирует игрока, потом случайный ход
        best_move = self.find_winning_move("O") or self.find_winning_move("X") or self.random_move()
        if best_move:
            self.make_move(*best_move)

    def find_winning_move(self, player):
        # Проверяет возможные выигрышные ходы
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = player
                    if self.check_winner() == player:
                        self.board[i][j] = " "
                        return (i, j)
                    self.board[i][j] = " "
        return None

    def random_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
        return random.choice(empty_cells) if empty_cells else None

    def make_move(self, row, col):
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(text=self.current_player)

        if self.check_game_over():
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_status()

    def check_winner(self):
        # Проверка строк
        for row in self.board:
            if row[0] == row[1] == row[2] != " ":
                return row[0]

        # Проверка столбцов
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                return self.board[0][col]

        # Проверка диагоналей
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]

        return None

    def check_draw(self):
        return all(cell != " " for row in self.board for cell in row)

    def check_game_over(self):
        winner = self.check_winner()
        if winner:
            messagebox.showinfo("Игра окончена", f"Победитель: {winner}!")
            return True
        elif self.check_draw():
            messagebox.showinfo("Игра окончена", "Ничья!")
            return True
        return False

    def clear_board(self):
        self.current_player = "X"
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ")
        self.update_status()

    def update_status(self):
        status = f"Ход игрока: {self.current_player}"
        if self.computer_player and self.current_player == self.computer_player:
            status = "Ход компьютера..."
        self.status_label.config(text=status)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()