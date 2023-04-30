import tkinter as tk
import random

# Font and Colors
Label_font = ("Times New Roman", 24)
score_font = ("Times New Roman", 36, "bold")
Game_over_font = ("Times New Roman", 48, "bold")
grid_col = "#a39489"
Game_over_col = "#ffffff"
Cell_Bg = "#c2b3a9"
Win_Bg = "#ffcc00"
Lose_Bg = "#a39489"
Number_font = {
    2: ("Times New Roman", 55, "bold"),
    4: ("Times New Roman", 55, "bold"),
    8: ("Times New Roman", 55, "bold"),
    16: ("Times New Roman", 50, "bold"),
    32: ("Times New Roman", 50, "bold"),
    64: ("Times New Roman", 50, "bold"),
    128: ("Times New Roman", 45, "bold"),
    256: ("Times New Roman", 45, "bold"),
    512: ("Times New Roman", 45, "bold"),
    1024: ("Times New Roman", 40, "bold"),
    2048: ("Times New Roman", 40, "bold"),
}
Cell_col = {
    2: "#fcefe6",
    4: "#f2e8cb",
    8: "#f5b682",
    16: "#f29446",
    32: "#ff775c",
    64: "#e64c2e",
    128: "#ede291",
    256: "#fce130",
    512: "#ffdb4a",
    1024: "#f0b922",
    2048: "#fad74d"
}
Number_col = {
    2: "#695c57",
    4: "#695c57",
    8: "#ffffff",
    16: "#ffffff",
    32: "#ffffff",
    64: "#ffffff",
    128: "#ffffff",
    256: "#ffffff",
    512: "#ffffff",
    1024: "#ffffff",
    2048: "#ffffff",
}


# Main class for initializing game
class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('Default 2048. Enjoy!')
        self.main_grid = tk.Frame(self, bg=grid_col, bd=3, width=600, height=600)
        self.main_grid.grid(pady=(100, 0))
        self.make_GUI()
        self.start_game()
        # Binding arrows as gameplay buttons
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()

    # make the grid and frontend
    def make_GUI(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(self.main_grid, bg=Cell_Bg, width=150, height=150)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=Cell_Bg)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        # make score header
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.75, y=45, anchor="center")
        tk.Label(score_frame, text="Score", font=Label_font).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=score_font)
        self.score_label.grid(row=1)
        # make high score header
        high_score_frame = tk.Frame(self)
        high_score_frame.place(relx=0.25, y=45, anchor="center")
        tk.Label(high_score_frame, text="High score", font=Label_font).grid(row=0)
        # reading last high score from file
        file = open('high_score', 'r')
        init_high = int(file.readline())
        file.close()
        self.high_score_label = tk.Label(high_score_frame, text=init_high, font=score_font)
        self.high_score_label.grid(row=1)
        # bot button
        bot_button = tk.Button(self, height=2, width=1, bg="#ffff00", text="Bot", font=Label_font, command="bot")
        bot_button.place(relx=0.5, y=45, anchor="center")


    def start_game(self):
        # create matrix of zeroes
        self.matrix = [[0] * 4 for _ in range(4)]

        # fill 2 random cells with 2s
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=Cell_col[2])
        self.cells[row][col]["number"].configure(
            bg=Cell_col[2],
            fg=Number_col[2],
            font=Number_font[2],
            text="2"
        )
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=Cell_col[2])
        self.cells[row][col]["number"].configure(
            bg=Cell_col[2],
            fg=Number_col[2],
            font=Number_font[2],
            text="2"
        )
        # initialize attributes to update them later
        self.score = 0
        file = open('high_score', 'r')
        init_high = int(file.readline())
        file.close()
        self.high_score = init_high

    # Following 4 functions used to proceed matrix changes
    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0
                    # update score and high score values
                    self.score += self.matrix[i][j]
                    if self.score > self.high_score:
                        self.high_score = self.score
                    file = open('high_score', 'r')
                    init_high = int(file.readline())
                    file.close()
                    if self.high_score > init_high:
                        file = open('high_score', 'w')
                        file.write(f'{self.high_score}')
                        file.close()

    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3-j])
        self.matrix = new_matrix

    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    # Add a new 2 or 4 tile randomly to an empty cell
    def add_new_tile(self):
        if any(0 in row for row in self.matrix):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            while self.matrix[row][col] != 0:
                row = random.randint(0, 3)
                col = random.randint(0, 3)
            self.matrix[row][col] = random.choices([2, 4], weights = [9, 1], k =1)[0]

    # Update the GUI to match values in matrix
    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=Cell_Bg)
                    self.cells[i][j]["number"].configure(bg=Cell_Bg, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=Cell_col[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=Cell_col[cell_value],
                        fg=Number_col[cell_value],
                        font=Number_font[cell_value],
                        text=str(cell_value)
                    )
        self.score_label.configure(text=self.score)
        self.high_score_label.configure(text=self.high_score)
        self.update_idletasks()

    # Proceed Arrow press events
    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def bot(self):
        moves = [self.down, self.up, self.right, self.left]
        move = random.choice(moves)
        move


    # Check if any horizontal moves are available
    def horizontal_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False

    # Check if any vertical moves are available
    def vertical_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False

    # Check if game is over (Win Or Lose)
    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="You win!",
                bg=Win_Bg,
                fg=Game_over_col,
                font=Game_over_font).pack()
        elif not any(0 in row for row in self.matrix) and not self.horizontal_exists() and not self.vertical_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="Game Over",
                bg=Lose_Bg,
                fg=Game_over_col,
                font=Game_over_font).pack()


# Main function to init the game
def main():
    Game()


# Initializing program
if __name__ == "__main__":
    main()
