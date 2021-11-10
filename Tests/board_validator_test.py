import unittest
from Board.board import Board
from Board.board_validator import BoardValidator,  BoardValidationError


class TestBoardValidator(unittest.TestCase):
    def setUp(self):
        self.test_board = Board(10, 10)
        self.board_validator = BoardValidator(self.test_board)

    def test_validate_position(self):
        try:
            self.board_validator.validate_position('ads', 2)
        except BoardValidationError as error:
            assert error.msg == "This position is invalid"

        try:
            self.board_validator.validate_position(-5, 2)
        except BoardValidationError as error:
            assert error.msg == "This position is invalid"

        try:
            self.board_validator.validate_position(5, 'sadsad')
        except BoardValidationError as error:
            assert error.msg == "This position is invalid"

        try:
            self.board_validator.validate_position(5, -2)
        except BoardValidationError as error:
            assert error.msg == "This position is invalid"

    def test_validate_new_move(self):
        self.test_board.set_cell_status(2, 2, "hit")

        try:
            self.board_validator.validate_new_move(2, 2)
        except BoardValidationError as error:
            assert error.msg == "This cell has been already hit"

    def test_validate_new_plane(self):

        try:
            self.board_validator.validate_new_plane(5, 2, 5, 6)
        except BoardValidationError as error:
            assert error.msg == "The distance between the tail and the head should be exactly 3 squares"

        try:
            self.board_validator.validate_new_plane(-2, 2, -2, 5)
        except BoardValidationError as error:
            print(error.msg)
            assert error.msg == "You can't place a plane outside the map"

        try:
            self.board_validator.validate_new_plane(5, -2, 5, 1)
        except BoardValidationError as error:
            assert error.msg == "You can't place a plane outside the map"

        self.test_board.set_cell_status(5, 3, "head")

        # head_line == tail_line

        try:
            self.board_validator.validate_new_plane(5, 2, 5, 5)
        except BoardValidationError as error:
            assert error.msg == "There is another plane on this position"

        try:
            self.board_validator.validate_new_plane(6, 2, 6, 5)
        except BoardValidationError as error:
            assert error.msg == "There is another plane on this position"

        try:
            self.board_validator.validate_new_plane(4, 2, 4, 5)
        except BoardValidationError as error:
            assert error.msg == "There is another plane on this position"

        self.test_board.set_cell_status(5, 4, "head")

        try:
            self.board_validator.validate_new_plane(5, 5, 5, 2)
        except BoardValidationError as error:
            assert error.msg == "There is another plane on this position"

        try:
            self.board_validator.validate_new_plane(6, 5, 6, 2)
        except BoardValidationError as error:
            assert error.msg == "There is another plane on this position"

        try:
            self.board_validator.validate_new_plane(4, 5, 4, 2)
        except BoardValidationError as error:
            assert error.msg == "There is another plane on this position"

        # head_column == tail_column

        try:
            self.board_validator.validate_new_plane(2, 4, 6, 4)
        except BoardValidationError as error:
            assert error.msg == "The distance between the tail and the head should be exactly 3 squares"

        try:
            self.board_validator.validate_new_plane(2, -4, 5, -4)
        except BoardValidationError as error:
            assert error.msg == "You can't place a plane outside the map"

        try:
            self.board_validator.validate_new_plane(2, 4, -1, 4)
        except BoardValidationError as error:
            assert error.msg == "You can't place a plane outside the map"

        try:
            self.board_validator.validate_new_plane(3, 4, 6, 4)
        except BoardValidationError as error:
            assert error.msg == "There is another plane on this position"
        self.test_board.set_cell_status(6, 4, "body")
        self.test_board.set_cell_status(6, 6, "body")
        try:
            self.board_validator.validate_new_plane(3, 3, 6, 3)
        except BoardValidationError as error:
            assert error.msg == "There is another plane on this position"

        try:
            self.board_validator.validate_new_plane(5, 5, 8, 5)
        except BoardValidationError as error:
            assert error.msg == "There is another plane on this position"

        try:
            self.board_validator.validate_new_plane(3, 5, 6, 5)
        except BoardValidationError as error:
            assert error.msg == "There is another plane on this position"

        self.test_board.set_cell_status(5, 6, "body")

        try:
            self.board_validator.validate_new_plane(6, 5, 3, 5)
        except BoardValidationError as error:
            assert error.msg == "There is another plane on this position"

        self.test_board.set_cell_status(5, 4, "body")
        try:
            self.board_validator.validate_new_plane(6, 5, 3, 5)
        except BoardValidationError as error:
            assert error.msg == "There is another plane on this position"
        self.test_board.set_cell_status(6, 4, "body")
        try:
            self.board_validator.validate_new_plane(6, 4, 3, 4)
        except BoardValidationError as error:
            assert error.msg == "There is another plane on this position"

        try:
            self.board_validator.validate_new_plane(6, 7, 3, 2)
        except BoardValidationError as error:
            assert error.msg == "The plane should have the body either on the same line, either on the same column"

