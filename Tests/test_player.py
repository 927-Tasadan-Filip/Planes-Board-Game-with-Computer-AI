import unittest
from Player.Player import Player


class TestPLayer(unittest.TestCase):
    def setUp(self):
        self.test_player = Player()

    def test_strike(self):
        self.test_player.strike(2, 2, "")
        assert self.test_player.get_enemy_cell_status(2, 2) == "empty"

        self.test_player.strike(5, 5, "head")
        assert self.test_player.get_enemy_cell_status(5, 5) == "hit"

    def test_add_new_plane(self):
        self.test_player.add_new_plane(6, 5, 9, 5, 1)
        assert self.test_player.get_ally_cell_status(5, 4) == "head"
        assert self.test_player.get_cell_plane_id(5, 4) == 1

    def test_get_last_hit_cell_status(self):
        assert self.test_player.get_last_hit_cell_status(1, 1) == ""

    def test_fill_destroyed_cells(self):
        self.test_player.add_new_plane(6, 5, 9, 5, 1)
        self.test_player.strike(6, 5, "head")
        self.test_player.fill_destroyed_cells(6, 5, [], 1)

        assert self.test_player.get_enemy_cell_status(6, 5) == "hit"

    def test_set_plane_cells_as_destroyed(self):
        self.test_player.set_plane_cells_as_destroyed([[5, 5]])
        assert self.test_player.get_enemy_cell_status(5, 5) == "destroyed"

    def test_get_ally_board_cell_status(self):
        for list_of_elem in self.test_player.get_ally_board_cell_status():
            for element in list_of_elem:
                assert element == ''

    def test_get_enemy_board_cell_status(self):
        for list_of_elem in self.test_player.get_enemy_board_cell_status():
            for element in list_of_elem:
                assert element == ''

    def test_update_board_after_strike(self):
        self.test_player.update_board_after_strike(5, 5, "body")
        assert self.test_player.get_ally_cell_status(5, 5) == "body_hit"
        self.test_player.update_board_after_strike(6, 5, "")
        assert self.test_player.get_ally_cell_status(6, 5) == "hit"