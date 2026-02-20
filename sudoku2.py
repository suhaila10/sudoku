import random
import copy
import tkinter as tk
from tkinter import messagebox
import time

# ==============================
# SUDOKU GENERATOR + SOLVER
# ==============================

def generate_sudoku():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    fill_diagonal(grid)
    solve_sudoku(grid)
    remove_elements(grid, random.randint(35, 50))
    return grid


def fill_diagonal(grid):
    for i in range(0, 9, 3):
        fill_box(grid, i, i)


def fill_box(grid, row, col):
    nums = list(range(1, 10))
    random.shuffle(nums)
    idx = 0
    for i in range(3):
        for j in range(3):
            grid[row + i][col + j] = nums[idx]
            idx += 1


def is_safe(grid, row, col, num):
    return (
        num not in grid[row] and
        num not in [grid[i][col] for i in range(9)] and
        num not in [
            grid[row - row % 3 + i][col - col % 3 + j]
            for i in range(3)
            for j in range(3)
        ]
    )


def find_empty(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None


def solve_sudoku(grid):
    empty = find_empty(grid)
    if not empty:
        return True

    row, col = empty

    for num in range(1, 10):
        if is_safe(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0
    return False


def remove_elements(grid, count):
    removed = 0
    while removed < count:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if grid[i][j] != 0:
            grid[i][j] = 0
            removed += 1


# ==============================
# GUI GAME
# ==============================

class SudokuGame:

    def __init__(self, root):
        self.root = root
        self.root.title("AI Sudoku Game")
        
        # Make window a bit larger for better visibility
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.original = None
        self.solution = None
        self.start_time = None

        # Timer and title frame
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)
        
        title_label = tk.Label(top_frame, text="SUDOKU", font=("Arial", 24, "bold"))
        title_label.pack()
        
        self.timer_label = tk.Label(top_frame, text="Time: 0s", font=("Arial", 12))
        self.timer_label.pack()

        # Create main grid frame with border
        main_grid_frame = tk.Frame(root, bg="black", bd=3)
        main_grid_frame.pack(pady=10)

        # Create 3x3 blocks
        for block_row in range(3):
            for block_col in range(3):
                # Create frame for each 3x3 block
                block_frame = tk.Frame(
                    main_grid_frame, 
                    bg="black",
                    highlightbackground="black",
                    highlightthickness=1,
                    bd=2,
                    relief="solid"
                )
                block_frame.grid(
                    row=block_row, 
                    column=block_col, 
                    padx=(0 if block_col == 2 else 2, 0),
                    pady=(0 if block_row == 2 else 2, 0)
                )
                
                # Create entries for this block
                for i in range(3):
                    for j in range(3):
                        # Calculate global position
                        global_row = block_row * 3 + i
                        global_col = block_col * 3 + j
                        
                        entry = tk.Entry(
                            block_frame, 
                            width=2, 
                            font=("Arial", 24, "bold"),
                            justify="center",
                            bd=1,
                            relief="solid"
                        )
                        entry.grid(row=i, column=j, padx=1, pady=1)
                        
                        # Bind events
                        entry.bind("<KeyRelease>", self.on_key_release)
                        entry.bind("<FocusIn>", self.on_focus_in)
                        entry.bind("<FocusOut>", self.on_focus_out)
                        
                        self.entries[global_row][global_col] = entry

        # Button frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)

        # Buttons with better styling
        button_style = {
            "font": ("Arial", 11, "bold"),
            "bg": "#4a7a9c",
            "fg": "white",
            "padx": 15,
            "pady": 5,
            "bd": 0,
            "cursor": "hand2"
        }
        
        # New Game button
        tk.Button(btn_frame, text="New Game", command=self.new_game, **button_style).grid(row=0, column=0, padx=5)
        
        # Check button
        tk.Button(btn_frame, text="Check", command=self.check_solution, **button_style).grid(row=0, column=1, padx=5)
        
        # Hint button
        tk.Button(btn_frame, text="Hint", command=self.hint, **button_style).grid(row=0, column=2, padx=5)
        
        # Solve (AI) button - using backtracking
        tk.Button(btn_frame, text="Solve (AI)", command=self.solve_ai, **button_style).grid(row=0, column=3, padx=5)
        
        # Clear button
        tk.Button(btn_frame, text="Clear", command=self.clear, **button_style).grid(row=0, column=4, padx=5)

        # Status bar
        self.status_label = tk.Label(
            root, 
            text="Click 'New Game' to start", 
            font=("Arial", 10),
            bd=1,
            relief="sunken",
            anchor="w"
        )
        self.status_label.pack(fill="x", padx=10, pady=5)

        # Bind keyboard navigation
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        
        self.current_row = 0
        self.current_col = 0

        self.update_timer()

    def update_timer(self):
        """Update the timer display"""
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.update_timer)

    def on_focus_in(self, event):
        """Highlight the focused cell"""
        row, col = self.find_cell(event.widget)
        if row is not None and col is not None:
            self.current_row = row
            self.current_col = col
            event.widget.config(bg="#e6f3ff")

    def on_focus_out(self, event):
        """Remove highlight from unfocused cell"""
        event.widget.config(bg="white")

    def move_up(self, event):
        """Move focus up"""
        if self.current_row > 0:
            self.current_row -= 1
            self.entries[self.current_row][self.current_col].focus()

    def move_down(self, event):
        """Move focus down"""
        if self.current_row < 8:
            self.current_row += 1
            self.entries[self.current_row][self.current_col].focus()

    def move_left(self, event):
        """Move focus left"""
        if self.current_col > 0:
            self.current_col -= 1
            self.entries[self.current_row][self.current_col].focus()

    def move_right(self, event):
        """Move focus right"""
        if self.current_col < 8:
            self.current_col += 1
            self.entries[self.current_row][self.current_col].focus()

    def get_grid(self):
        """Get current grid values"""
        grid = [[0]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                if val.isdigit():
                    grid[i][j] = int(val)
        return grid

    def set_grid(self, grid):
        """Set grid values"""
        self.clear()
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    self.entries[i][j].insert(0, str(grid[i][j]))

    def clear(self):
        """Clear all entries (except original locked cells)"""
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.config(state="normal", fg="black", bg="white")
                entry.delete(0, tk.END)
        
        # Restore original locked cells if they exist
        if self.original:
            for i in range(9):
                for j in range(9):
                    if self.original[i][j] != 0:
                        self.entries[i][j].insert(0, str(self.original[i][j]))
                        self.entries[i][j].config(
                            state="disabled",
                            disabledforeground="#2c3e50",
                            bg="#f0f0f0"
                        )
            self.status_label.config(text="Cleared your entries. Original puzzle restored.")

    def new_game(self):
        """Start a new game"""
        puzzle = generate_sudoku()
        self.original = copy.deepcopy(puzzle)

        solved = copy.deepcopy(puzzle)
        solve_sudoku(solved)
        self.solution = solved

        self.set_grid(puzzle)

        # Lock original numbers and style them
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    self.entries[i][j].config(
                        state="disabled",
                        disabledforeground="#2c3e50",
                        bg="#f0f0f0",
                        font=("Arial", 24, "bold")
                    )
                else:
                    self.entries[i][j].config(
                        state="normal",
                        bg="white",
                        font=("Arial", 24)
                    )

        self.start_time = time.time()
        self.status_label.config(text="Game started! Fill in the empty cells.")

    def on_key_release(self, event):
        """Handle key release events - color codes:
        - Green: Correct cell
        - Red: Wrong cell
        """
        row, col = self.find_cell(event.widget)
        if row is None:
            return

        val = event.widget.get()

        # Validate input
        if val == "":
            event.widget.config(fg="black")
            return
            
        if not val.isdigit() or not (1 <= int(val) <= 9):
            event.widget.delete(0, tk.END)
            self.status_label.config(text="Please enter a number between 1-9")
            return

        # Check if correct - Green for correct, Red for wrong
        if self.solution and int(val) != self.solution[row][col]:
            event.widget.config(fg="red")  # Wrong cell highlighted in red
            self.status_label.config(text="Wrong number! Try again.")
        else:
            event.widget.config(fg="green")  # Correct cell highlighted in green
            self.status_label.config(text="Correct!")

    def find_cell(self, widget):
        """Find cell coordinates from widget"""
        for i in range(9):
            for j in range(9):
                if self.entries[i][j] == widget:
                    return i, j
        return None, None

    def check_solution(self):
        """Check if the solution is correct - shows warning if incomplete"""
        grid = self.get_grid()

        # Check for incomplete cells
        if any(0 in row for row in grid):
            messagebox.showwarning("Incomplete", "Please fill all cells first!")
            self.status_label.config(text="Fill all empty cells before checking.")
            return

        # Check if solution matches
        if grid == self.solution:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            messagebox.showinfo(
                "🎉 Congratulations!", 
                f"You solved the puzzle!\nTime: {minutes:02d}:{seconds:02d}"
            )
            self.status_label.config(text="Great job! You solved it!")
        else:
            messagebox.showerror("Wrong Solution", "Some numbers are incorrect. Keep trying!")
            self.status_label.config(text="Keep going! You can do it!")

    def hint(self):
        """Provide a hint by filling one empty cell - highlighted in blue"""
        grid = self.get_grid()
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0 and self.entries[i][j]['state'] != 'disabled':
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, str(self.solution[i][j]))
                    self.entries[i][j].config(fg="blue")  # Hint cell highlighted in blue
                    self.status_label.config(text="Here's a hint for you!")
                    return
        self.status_label.config(text="No empty cells left!")

    def solve_ai(self):
        """Solve the puzzle using AI (backtracking algorithm)"""
        if messagebox.askyesno("AI Solve", "Do you want the AI to solve the puzzle using backtracking?"):
            self.set_grid(self.solution)
            for i in range(9):
                for j in range(9):
                    self.entries[i][j].config(fg="purple")
            self.status_label.config(text="AI solved the puzzle using backtracking!")
            messagebox.showinfo("AI Solved", "Puzzle solved using Backtracking Algorithm!")


# ==============================
# RUN GAME
# ==============================

if __name__ == "__main__":
    root = tk.Tk()
    
    # Set application icon (optional)
    try:
        root.iconbitmap(default='sudoku.ico')
    except:
        pass
    
    game = SudokuGame(root)
    root.mainloop()