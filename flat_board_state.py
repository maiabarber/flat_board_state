# you can add global params

import numpy as np
import enum

class PositionState(enum.IntEnum):
    HOLE = 0
    FLOOR = 1
    WALL = 2
    CUBE = 3

class flat_board_state:
    def __init__(self, instance_map=None, *args, **kwargs):
        self.board = np.array(instance_map, dtype=int, copy=True)

    @staticmethod
    def is_goal_state(_flat_board_state):
        """
        This function checks if the given flat_board_state is a goal state.
        :param _flat_board_state: a flat_board_state object
        :return: True if the given flat_board_state is a goal state, False otherwise
        """
        for row in _flat_board_state.board:
            for cell in row:
                if cell == PositionState.HOLE:
                    return False
        return True

    
    def get_neighbors(self):
        """
        Returns a list of tuples containing neighboring states
        and the cost of reaching each state.
        """
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        board = np.array(self.board)

        for dr, dc in directions:
            cubes = self.get_sorted_cubes(board, dr, dc)

            if not cubes:
                continue

            can_move = self.check_cubes_movement(
                board, cubes, dr, dc
            )

            new_board, changed = self.move_cubes(
                board, cubes, can_move, dr, dc
            )

            if changed and not np.array_equal(board, new_board):
                neighbor_state = flat_board_state(new_board)
                neighbors.append((neighbor_state, 1))

        return neighbors


    def get_sorted_cubes(self, board, dr, dc):
        """
        (helper function)
        Finds all cubes (3) on the board and sorts them based on
        the movement direction to ensure the correct movement order.

        :param board: The current game board.
        :param dr: The row movement direction (-1 for up, 1 for down, 0 for no vertical movement).
        :param dc: The column movement direction (-1 for left, 1 for right, 0 for no horizontal movement).
        :return: A sorted list of tuples representing the positions
                (row, col) of all cubes on the board.
        """
        cubes = list(zip(*np.where(board == 3)))

        if dr == -1:  # up
            cubes.sort(key=lambda x: x[0])
        elif dr == 1:  # down
            cubes.sort(key=lambda x: x[0], reverse=True)
        elif dc == -1:  # left
            cubes.sort(key=lambda x: x[1])
        elif dc == 1:  # right
            cubes.sort(key=lambda x: x[1], reverse=True)

        return cubes


    def check_cubes_movement(self, board, cubes, dr, dc):
        """
        (helper function)
        Checks whether each cube can move in the direction 
        if there is a cube (3) in front of it, it can move only if that cube can move.
        if there is an empty space (0) or a floor (1), it can move.
        if there is a board edge or a wall (2), it cannot move.
        returns a dictionary with the cube positions as keys and a boolean indicating whether they can move as values.
        """
        rows, cols = board.shape
        can_move = {}

        for r, c in cubes:
            new_row, new_col = r + dr, c + dc
            # Check if the new position is out of bounds
            if not (0 <= new_row < rows and 0 <= new_col < cols):
                can_move[(r, c)] = False
            # Check if the new position is a wall (2)
            elif board[new_row, new_col] == 2:
                can_move[(r, c)] = False

            # Check if the new position is a cube (3)
            elif board[new_row, new_col] == 3:
                can_move[(r, c)] = can_move.get(
                    (new_row, new_col), False
                )

            else:
                can_move[(r, c)] = True

        return can_move


    def move_cubes(self, board, cubes, can_move, dr, dc):
        """
        (helper function)
        Moves cubes in the specified direction if they can move.
        returns the updated board.
        """
        temp_board = board.copy()

        for r, c in cubes:
            temp_board[r, c] = 1

        changed = False

        for r, c in cubes:
            # If the cube can move, update its position on the board and change the 'changed' flag to True.
            if can_move[(r, c)]:
                new_row, new_col = r + dr, c + dc
                changed = True
                # If the new position is a hole (0), move the cube there and mark it as floor.
                if board[new_row, new_col] == PositionState.HOLE:
                    temp_board[new_row, new_col] = PositionState.FLOOR
                # If the new position is a floor (1), move the cube there and mark it as cube.
                else:
                    temp_board[new_row, new_col] = PositionState.CUBE                
            # If the cube cannot move, it remains in its original position.
            else:
                temp_board[r, c] = PositionState.CUBE
        return temp_board, changed

    # you can change the body of the function if you want
    def __hash__(self):
        return hash(tuple(map(tuple, self.board)))

    # you can change the body of the function if you want
    def __eq__(self, other):
        if not isinstance(other, flat_board_state):
            return False
        return np.array_equal(self.board, other.board)

    def get_state_board(self):
        return self.board.tolist()

    def get_state_str(self):
        return str(self.board.tolist())

    # you can add helper functions
