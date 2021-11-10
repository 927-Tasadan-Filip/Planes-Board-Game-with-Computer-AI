from Player.Player import *
from Player.Computer import *
import unittest

class TestComputerPlayer(unittest.TestCase):
    def setUp(self):
        self.test_computer_player = Computer()

    def test_computer_add_planes_on_board(self):
        self.test_computer_player.computer_add_planes_random_on_board()