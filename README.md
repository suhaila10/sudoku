1. Generator Module
generate_sudoku(): This function generates a new Sudoku puzzle. After creating an empty grid, random numbers are inserted into the diagonal boxes. It then solves the entire grid to make sure there is a legitimate solution. Lastly, it generates a playable Sudoku puzzle by randomly deleting a few numbers.
fill_diagonal(): The Sudoku grid's diagonal boxes are filled by this function. Diagonal boxes can be independently filled with random values because they have no effect on one another. This speeds up the creation of puzzles.
fill_box(): This function fills a 3×3 box with random numbers from 1 to 9. It ensures that each number appears only once inside the box.
remove_elements(): This function removes a certain number of values from the solved Sudoku grid. 


2. Solver Module
solve_sudoku:This function uses backtracking to solve the Sudoku puzzle. After locating an empty cell, it attempts to enter numbers 1 through 9. If a number is correct, it is entered and the remaining grid is solved recursively. It goes back and tries a different number if it can't find a solution.
is_safe: This function determines whether a number can be positioned in a particular way. It guarantees that the number hasn't been used in the same row, column, or 3x3 box before.
used_in_row: This function determines if a given number is already present in a row. It helps prevent row conflicts.
used_in_column: This function determines if a given number is already present in a column. It stops Sudoku rules from being broken by columns.
used_in_box: This function checks whether a number exists in a 3×3 subgrid. It ensures that each box contains unique numbers.
find_unassigned_location: This function searches the grid for an empty cell.
 It returns the position of the first unfilled cell, which is used by the solver to continue the search.
solve_sudoku_forward_checking:This function solves Sudoku using backtracking with forward checking. It keeps track of possible values (domains) for each empty cell. Invalid values are removed early, reducing unnecessary searching and making solving faster.

3. GUI Module
Class: SudokuGame: The Sudoku game's graphical user interface is managed by this class. It controls the game logic, buttons, user input, and board display.
create_grid: This function uses GUI elements to create the 9x9 input grid. The player can enter numbers in the input box that represents each cell.
new_game: This feature creates a brand-new Sudoku puzzle and shows it on the screen. It gets the game ready for a new round by resetting the board.
get_board: This function retrieves the user-inputted values from the grid. It transforms GUI inputs into a 2D list so the solver can process them.
update_board: This function uses a specified Sudoku board to update the GUI grid. It is used when showing solutions or hints.
highlight_errors: The function will highlight the incorrect cells in red by comparing them against the correct solution, very similar to what you would see in actual Sudoku apps.
Solve_with_ai: The function will automatically solve the Sudoku puzzle using the AI solver. The board will then be filled in with the correct solution and presented to you.
Show_hint: The function will provide the user with a hint. One number will be placed in an empty cell so they can continue solving their Sudoku puzzle.
