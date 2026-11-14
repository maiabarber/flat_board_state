import unittest
import numpy as np
from flat_board_state import flat_board_state


class TestFlatBoardState(unittest.TestCase):
    def make_state(self, board):
        return flat_board_state(board)

    def assert_board_equal(self, actual, expected):
        np.testing.assert_array_equal(actual.board, np.array(expected))

    def test_goal_no_holes(self):
        state = self.make_state([[2, 2, 2], [2, 1, 2], [2, 2, 2]])
        self.assertTrue(flat_board_state.is_goal_state(state))

    def test_goal_with_hole(self):
        state = self.make_state([[2, 3, 2], [2, 0, 2], [2, 2, 2]])
        self.assertFalse(flat_board_state.is_goal_state(state))

    def test_single_cube_four_directions(self):
        board = [[2,2,2,2,2], [2,1,1,1,2], [2,1,3,1,2], [2,1,1,1,2], [2,2,2,2,2]]
        state = self.make_state(board)
        neighbors = state.get_neighbors()
        self.assertEqual(len(neighbors), 4)
        expected_positions = {(1,2), (3,2), (2,1), (2,3)}
        observed_positions = set()
        for next_state, cost in neighbors:
            self.assertEqual(cost, 1)
            positions = np.argwhere(next_state.board == 3)
            self.assertEqual(len(positions), 1)
            observed_positions.add(tuple(positions[0]))
        self.assertEqual(observed_positions, expected_positions)

    def test_cube_fills_hole(self):
        state = self.make_state([[2,2,2,2,2], [2,3,0,1,2], [2,2,2,2,2]])
        neighbors = state.get_neighbors()
        self.assertEqual(len(neighbors), 1)
        next_state, cost = neighbors[0]
        self.assertEqual(cost, 1)
        self.assert_board_equal(next_state, [[2,2,2,2,2], [2,1,1,1,2], [2,2,2,2,2]])
        self.assertTrue(flat_board_state.is_goal_state(next_state))

    def test_two_adjacent_cubes_right_into_hole(self):
        state = self.make_state([[2,2,2,2,2], [2,3,3,0,2], [2,1,1,1,2], [2,2,2,2,2]])
        neighbors = state.get_neighbors()
        expected = [[2,2,2,2,2], [2,1,3,1,2], [2,1,1,1,2], [2,2,2,2,2]]
        self.assertTrue(any(np.array_equal(n.board, expected) and cost == 1 for n,cost in neighbors))

    def test_cube_blocked_by_wall(self):
        state = self.make_state([[2,2,2], [2,3,2], [2,2,2]])
        self.assertEqual(state.get_neighbors(), [])

    def test_chain_blocked_by_wall(self):
        state = self.make_state([[2,2,2,2,2], [2,3,3,2,2], [2,2,2,2,2]])
        self.assertEqual(state.get_neighbors(), [])

    def test_no_mutation_of_original(self):
        board = [[2,2,2,2,2], [2,1,3,0,2], [2,1,1,1,2], [2,2,2,2,2]]
        state = self.make_state(board)
        before = state.board.copy()
        state.get_neighbors()
        np.testing.assert_array_equal(state.board, before)
        self.assertEqual(board, [[2,2,2,2,2], [2,1,3,0,2], [2,1,1,1,2], [2,2,2,2,2]])

    def test_no_hole_overwritten_when_cube_moves_elsewhere(self):
        state = self.make_state([[2,2,2,2,2,2], [2,3,1,0,1,2], [2,2,2,2,2,2]])
        expected = [[2,2,2,2,2,2], [2,1,3,0,1,2], [2,2,2,2,2,2]]
        self.assertTrue(any(np.array_equal(n.board, expected) for n,_ in state.get_neighbors()))

    def test_state_board_list_of_lists(self):
        board = [[2,2,2], [2,3,2], [2,0,2]]
        state = self.make_state(board)
        result = state.get_state_board()
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(row, list) for row in result))
        self.assertEqual(result, board)

    def test_equal_states_same_hash(self):
        board = [[2,2,2], [2,3,2], [2,0,2]]
        a = self.make_state(board)
        b = self.make_state(board)
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))
        self.assertEqual(len({a, b}), 1)

    def test_different_states(self):
        a = self.make_state([[2,2,2], [2,3,2], [2,0,2]])
        b = self.make_state([[2,2,2], [2,0,2], [2,3,2]])
        self.assertNotEqual(a, b)

    def test_new_state_does_not_share_board(self):
        board = [[2,2,2], [2,3,2], [2,0,2]]
        state = self.make_state(board)
        board[1][1] = 1
        self.assertEqual(state.board[1,1], 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
