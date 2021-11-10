from Board.board import Board
import unittest


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.test_board = Board(10, 10)

    def test_board_creation(self):
        for line in range(10):
            for column in range(10):
                assert self.test_board.is_empty(line, column) is True

    def test_board_modification(self):
        self.test_board.set_cell_status(0, 0, 1)
        self.test_board.set_cell_status(1, 1, 1)
        self.test_board.set_cell_status(2, 2, 1)
        self.test_board.set_cell_status(3, 3, 1)
        self.test_board.set_cell_status(4, 4, 1)
        self.test_board.set_cell_status(5, 5, 1)
        aux_board = self.test_board.get_grid_board_status_as_list_of_lists_of_cells()
        for line in range(10):
            for column in range(10):
                if line == column and line <= 5:
                    assert self.test_board.is_empty(line, column) is False
                else:
                    assert self.test_board.is_empty(line, column) is True

    def test_lines_columns_getters(self):

        assert self.test_board.lines == 10
        assert self.test_board.columns == 10

    def test_get_cell_status(self):
        assert self.test_board.get_cell_status(2, 2) == ""
        assert self.test_board.get_cell_status(-20, 2) == None

    def test_create_plane_on_board(self):
        self.test_board.create_plane_on_board(8, 6, 8, 9, 1)
        assert self.test_board.get_cell_status(8, 6) == "head"
        assert self.test_board.get_cell_status(8, 7) == "body"

        self.test_board.create_plane_on_board(5, 4, 8, 4, 2)
        assert self.test_board.get_cell_status(5, 4) == "head"
        assert self.test_board.get_cell_status(6, 4) == "body"

        self.test_board.create_plane_on_board(1, 9, 1, 6, 3)
        assert self.test_board.get_cell_status(1, 9) == "head"
        assert self.test_board.get_cell_status(1, 8) == "body"

        self.test_board.create_plane_on_board(4, 1, 0, 1, 4)
        assert self.test_board.get_cell_status(4, 1) == "head"
        assert self.test_board.get_cell_status(3, 1) == "body"
        assert self.test_board.get_cell_plane_id(4, 1) == 4