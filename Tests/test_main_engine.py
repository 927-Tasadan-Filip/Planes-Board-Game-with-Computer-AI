from GameEngine.MainEngine import *
import unittest
from Board.board_validator import BoardValidationError


class TestComputerPlayer(unittest.TestCase):
    def setUp(self):
        self.test_engine = GameEngine()

    def test_validate_board_position(self):
        self.test_engine.validate_board_position(2, 2)

        try:
            self.test_engine.validate_board_position(-2, 5)
        except BoardValidationError:
            assert True

    def test_human_add_plane(self):
        self.test_engine.human_add_new_plane(6, 5, 9, 5, 1)
        ally_board = self.test_engine.get_human_ally_board()
        assert ally_board[6][5] == "body"

    def test_human_strike(self):
        cell_status = self.test_engine.human_strike(5, 5)
        human_board = self.test_engine.get_human_enemy_board()
        assert human_board[5][5] == "empty"
        assert cell_status == ""

    def test_computer_strike(self):
        cell_stauts = self.test_engine.computer_strike()


    def test_computer_add_planes(self):
        self.test_engine.computer_add_planes()

    def test_human_out_of_planes(self):
        assert self.test_engine.human_out_of_planes() == False

    def test_cumputer_out_of_planes(self):
        assert self.test_engine.computer_out_of_planes() == False