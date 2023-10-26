import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../Engine'))

from precomputed_move_data import PrecomputedMoveData


def test_precomputed_move_data():
    precomputed = PrecomputedMoveData()
    assert precomputed.num_squares_to_edge[0] == [7, 0, 7, 0, 0, 0, 7, 0]
    assert precomputed.num_squares_to_edge[1] == [7, 0, 6, 1, 1, 0, 6, 0]
    assert precomputed.num_squares_to_edge[50] == [1, 6, 5, 2, 1, 5, 1, 2]
