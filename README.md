**Sudoku Solver**
This is a Python program that solves Sudoku puzzles. It uses a backtracking algorithm to find the solution.

**Usage**
To use the solver, simply run the solve function in the assign10.py file. The solve function takes a SudokuState object as input, which represents the initial state of the puzzle.

use the code below to try to create your own board state to solve  ↓

_state = SudokuState()
# set up the initial state of the puzzle
# ...
solution = solve(state)

The solve function returns a SudokuState object representing the solved puzzle.



**Implementation**
The solver uses a backtracking algorithm to find the solution. The backtracking algorithm is a recursive algorithm that tries to solve the Sudoku puzzle by filling in each cell with a number, one at a time. It starts by finding the first empty cell in the puzzle, and then tries each possible number in that cell. If a number leads to a conflict, it tries the next number. If all numbers lead to conflicts, it backtracks to the previous cell and tries the next number there. It continues in this way until it finds a solution or determines that no solution exists.

Here's a step-by-step explanation of how the algorithm works:

Find the first empty cell in the puzzle.
Try each possible number in that cell.
If a number leads to a conflict (i.e., it violates the rules of Sudoku), try the next number.
If all numbers lead to conflicts, backtrack to the previous cell and try the next number there.
Repeat steps 2-4 until a solution is found or it is determined that no solution exists.
The algorithm uses recursion to keep track of the current state of the puzzle and to backtrack when necessary. When the algorithm reaches a dead end (i.e., it cannot find a valid number for a cell), it backtracks to the previous cell and tries the next number there. This process continues until a solution is found or it is determined that no solution exists.

