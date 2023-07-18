# Haram Yoon, 4/16/23, assign10, CSCI 051


import copy
import time


class SudokuState:
    def __init__(self):
        """
        constructor for our class
        declares size, numbers placed on board, and creates our board
        """
        self.size = 9
        self.num_placed = 0
        self.board = [[SudokuEntry() for i in range(self.size)] for i in range(self.size)]

    def remove_conflict(self, row, column, number):
        """
        remove number from the list of possible values at this entry
        :param row:  x coordinate
        :param column: y coordinate
        :param number: number we're putting on our x-y coordinate
        :return: updates list of possible value
        """
        # eleimate number row, col of board
        self.board[row][column].eliminate(number)

    def remove_all_conflicts(self, row, column, number):
        """
         removes number options in the board after placing a number down
        :param row:  x coordinate
        :param column: y coordinate
        :param number: number we're putting on our x-y coordinate
        :return: update all of the other unfilled entries that are in the same row, column or subgrid
        """
        # get current grid square
        grid_number = self.get_subgrid_number(row, column)
        # nested for loop to check if number placed is same row , col, or grid number as input coordinate
        for i in range(self.size):
            for j in range(self.size):
                # make sure to not do anything at input coordinate
                if i == row and j == column:
                    continue
                # remove possibility if overlapping row, col, or grid number
                if i == row or j == column or self.get_subgrid_number(i, j) == grid_number:
                    self.remove_conflict(i, j, number)

    def add_number(self, row, column, number):
        """
        adds number at certain coordinate at board
        :param row:  x coordinate
        :param column: y coordinate
        :param number: number we're putting on our x-y coordinate
        :return: modifies the receiver by adding number at row, column
        """
        # add num to board
        self.board[row][column].fix(number)
        # updates num placed
        self.num_placed += 1
        # removes conflicts to added board
        self.remove_all_conflicts(row,column, number)

    def get_most_constrained_cell(self):
        """
        entry that is not filled in yet that has the fewest possible options remaining
        :return: tuple containing the row and column of the most constrained entry in the board
        """
        width = self.size
        cell = (0, 0)
        # checks if input isn't already filled and if length of domain is smaller than current width
        for i in range(self.size):
            for j in range(self.size):
                if not self.board[i][j].is_fixed() and self.board[i][j].width() <= width:
                    # update current width
                    width = self.board[i][j].width()
                    # update most constrained cell
                    cell = (i, j)
        return cell

    def solution_is_possible(self):
        """
        if all entries on the board still have at least one possible value
        :return: bool expression
        """
        # nested loop to check if any there are any remaining possibilities per grid square
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].width() == 0:
                    return False
        return True

    def next_states(self):
        """
        get next states after the most contrained cell
        :return: a list of the next states that can be reached from this current state by trying to put a number in the most constrained cell
        """
        next_states_list = []
        i, j = self.get_most_constrained_cell()
        # loops through domain
        for value in self.board[i][j].values():
            # make copy and add number in value
            new_state = copy.deepcopy(self)
            new_state.add_number(i, j, value)
            # new_state.propagate()
            # append deepcopy if solutions still available
            if new_state.solution_is_possible():
                next_states_list.append(new_state)
        return next_states_list

    def is_goal(self):
        """
        check if goal is met
        :return: bool if state is our goal state
        """
        return self.size**2 == self.num_placed

    def get_subgrid_number(self, row, col):
        """
        Returns a number between 1 and 9 representing the subgrid
        that this row, col is in.  The top left subgrid is 1, then
        2 to the right, then 3 in the upper right, etc.
        """
        row_q = int(row / 3)
        col_q = int(col / 3)
        return row_q * 3 + col_q + 1

    def get_any_available_cell(self):
        """
        An uninformed cell finding variant.  If you use
        this instead of find_most_constrained_cell
        the search will perform a depth first search.
        """
        for r in range(self.size):
            for c in range(self.size):
                if not self.board[r][c].is_fixed():
                    return (r, c)
        return None

    def propagate(self):
        for ri in range(self.size):
            for ci in range(self.size):
                if not self.board[ri][ci].is_fixed() and \
                   self.board[ri][ci].width() == 1:
                    self.add_number(ri, ci, self.board[ri][ci].values()[0])
                    if self.solution_is_possible():
                        self.propagate()
                        return

    def get_raw_string(self):
        board_str = ""

        for r in self.board:
            board_str += str(r) + "\n"

        return "num placed: " + str(self.num_placed) + "\n" + board_str

    def __str__(self):
        """
        prints all numbers assigned to cells.  Unassigned cells (i.e.
        those with a list of options remaining are printed as blanks
        """
        board_string = ""

        for r in range(self.size):
            if r % 3 == 0:
                board_string += " " + "-" * (self.size * 2 + 5) + "\n"

            for c in range(self.size):
                entry = self.board[r][c]

                if c % 3 == 0:
                    board_string += "| "

                board_string += str(entry) + " "

            board_string += "|\n"

        board_string += " " + "-" * (self.size * 2 + 5) + "\n"

        return "num placed: " + str(self.num_placed) + "\n" + board_string


# -----------------------------------
# SudokuEntry class
# -----------------------------------

class SudokuEntry:
    def __init__(self):
        self.fixed = False
        self.domain = list(range(1, 10))

    def is_fixed(self):
        return self.fixed

    def width(self):
        return len(self.domain)

    def values(self):
        return self.domain

    def has_conflict(self):
        return len(self.domain) == 0

    def __str__(self):
        if self.fixed:
            return str(self.domain[0])
        return "_"

    def __repr__(self):
        if self.fixed:
            return str(self.domain[0])
        return str(self.domain)

    def fix(self, n):
        assert n in self.domain
        self.domain = [n]
        self.fixed = True

    def eliminate(self, n):
        if n in self.domain:
            assert not self.fixed
            self.domain.remove(n)

# -----------------------------------
# Even though this is the same DFS code
# that we used last time, our next_states
# function is makeing an "informed" decision
# so this algorithm performs similarly to
# best first search.


def dfs(state):
    """
    Recursive depth first search implementation

    Input:
    Takes as input a state.  The state class MUST have the following
    methods implemented:
    - is_goal(): returns True if the state is a goal state, False otherwise
    - next_states(): returns a list of the VALID states that can be
    reached from the current state

    Output:
    Returns a list of ALL states that are solutions (i.e. is_goal
    returned True) that can be reached from the input state.
    """
    # if the current state is a goal state, then return it in a list
    if state.is_goal():
        return [state]
    else:
        # make a list to accumulate the solutions in
        result = []

        for s in state.next_states():
            result += dfs(s)

        return result

# ------------------------------------
# three different board configurations:


def problem1():
    b = SudokuState()
    b.add_number(0, 1, 7)
    b.add_number(0, 7, 1)
    b.add_number(1, 2, 9)
    b.add_number(1, 3, 7)
    b.add_number(1, 5, 4)
    b.add_number(1, 6, 2)
    b.add_number(2, 2, 8)
    b.add_number(2, 3, 9)
    b.add_number(2, 6, 3)
    b.add_number(3, 1, 4)
    b.add_number(3, 2, 3)
    b.add_number(3, 4, 6)
    b.add_number(4, 1, 9)
    b.add_number(4, 3, 1)
    b.add_number(4, 5, 8)
    b.add_number(4, 7, 7)
    b.add_number(5, 4, 2)
    b.add_number(5, 6, 1)
    b.add_number(5, 7, 5)
    b.add_number(6, 2, 4)
    b.add_number(6, 5, 5)
    b.add_number(6, 6, 7)
    b.add_number(7, 2, 7)
    b.add_number(7, 3, 4)
    b.add_number(7, 5, 1)
    b.add_number(7, 6, 9)
    b.add_number(8, 1, 3)
    b.add_number(8, 7, 8)
    return b


def problem2():
    b = SudokuState()
    b.add_number(0, 1, 2)
    b.add_number(0, 3, 3)
    b.add_number(0, 5, 5)
    b.add_number(0, 7, 4)
    b.add_number(1, 6, 9)
    b.add_number(2, 1, 7)
    b.add_number(2, 4, 4)
    b.add_number(2, 7, 8)
    b.add_number(3, 0, 1)
    b.add_number(3, 2, 7)
    b.add_number(3, 5, 9)
    b.add_number(3, 8, 2)
    b.add_number(4, 1, 9)
    b.add_number(4, 4, 3)
    b.add_number(4, 7, 6)
    b.add_number(5, 0, 6)
    b.add_number(5, 3, 7)
    b.add_number(5, 6, 5)
    b.add_number(5, 8, 8)
    b.add_number(6, 1, 1)
    b.add_number(6, 4, 9)
    b.add_number(6, 7, 2)
    b.add_number(7, 2, 6)
    b.add_number(8, 1, 4)
    b.add_number(8, 3, 8)
    b.add_number(8, 5, 7)
    b.add_number(8, 7, 5)
    return b


def heart():
    b = SudokuState()
    b.add_number(1, 1, 4)
    b.add_number(1, 2, 3)
    b.add_number(1, 6, 6)
    b.add_number(1, 7, 7)
    b.add_number(2, 0, 5)
    b.add_number(2, 3, 4)
    b.add_number(2, 5, 2)
    b.add_number(2, 8, 8)
    b.add_number(3, 0, 8)
    b.add_number(3, 4, 6)
    b.add_number(3, 8, 1)
    b.add_number(4, 0, 2)
    b.add_number(4, 8, 5)
    b.add_number(5, 1, 5)
    b.add_number(5, 7, 4)
    b.add_number(6, 2, 6)
    b.add_number(6, 6, 7)
    b.add_number(7, 3, 5)
    b.add_number(7, 5, 1)
    b.add_number(8, 4, 8)
    return b


# --------------------------------
# Code that actual runs a sudoku problem, times it
# and prints out the solution.
# You can vary which problem your running on between
# problem1(), problem2() and heart() by changing the line
# below
#
# Uncomment this code when you have everything implemented and you
# want to solve some of the sample problems!

problem = problem2()
print("Starting board:")
print(problem)

start_time = time.time()
solutions = dfs(problem)
search_time = time.time()-start_time

print("Search took " + str(round(search_time, 2)) + " seconds")
print("There was " + str(len(solutions)) + " solution.\n\n")
if len(solutions) > 0:
    print(solutions[0])
