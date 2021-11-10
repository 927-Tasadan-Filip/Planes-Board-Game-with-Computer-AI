from Player.Human import *
from Player.Computer import *
from Board.board_validator import BoardValidationError
import random
from GameEngine.ComputerStrategy import Strategy


class GameEngine:
    def __init__(self):
        self.__human_player = Human()
        self.__computer_player = Computer()
        self.__strategy = Strategy(self.__computer_player.enemy_board, self.__human_player.ally_board, self.__computer_player._enemy_validator)
        self.__human_number_of_planes = 3
        self.__computer_number_of_planes = 3

    def validate_board_position(self, line, column):
        self.__human_player.ally_validator.validate_position(line, column)

    def human_add_new_plane(self, head_line, head_column, tail_line, tail_column, plane_id):
        self.__human_player.add_new_plane(head_line, head_column, tail_line, tail_column, plane_id)

    def human_strike(self, line, column):
        """
        Human perform a new strike
        :param line: strike line (type: positive integer)
        :param column: strike collumn (type: positive integer)
        :return: the status of the computer ally board cell that has been hit in order to update human enemy board
        """
        self.__human_player._enemy_validator.validate_new_move(line, column)
        enemy_cell_status = self.__computer_player.get_ally_cell_status(line, column)
        self.__human_player.strike(line, column, enemy_cell_status)

        if enemy_cell_status == "head":
            self.__human_destroy_computer_plane(line, column)

        return enemy_cell_status

    def computer_strike(self):
        """
        Computer performs a new strike
        """

        strike_position = self.__strategy.calculate_next_strike_position()
        strike_line = strike_position[0]
        strike_column = strike_position[1]


        enemy_cell_status = self.__human_player.get_ally_cell_status(strike_line, strike_column)
        self.__computer_player.strike(strike_line, strike_column, enemy_cell_status)
        self.__human_player.update_board_after_strike(strike_line, strike_column, enemy_cell_status)

        if enemy_cell_status == "head":
            self.__computer_destroy_human_plane(strike_line, strike_column)

        return enemy_cell_status

    def __human_destroy_computer_plane(self, head_line, head_column):
        """
        If at the last strike human destroyed a computer's plane both the human enemy board and computer ally board
        should be updated using the flood-fill algorithm
        :param head_line: the head line of the plane destroyed at the last strike
        :param head_column: the head column of the plane destroyed at the last strike
        """
        enemy_plane_id = self.__computer_player.get_cell_plane_id(head_line, head_column)
        positions_list = []
        self.__computer_player.fill_destroyed_cells(head_line, head_column, positions_list, enemy_plane_id)
        self.__human_player.set_plane_cells_as_destroyed(positions_list)
        self.__computer_number_of_planes -= 1
    
    def __computer_destroy_human_plane(self, head_line, head_column):
        """
        If at the last strike computer destroyed a human's plane both the computer enemy board and human ally board
        should be updated using the flood-fill algorithm
        :param head_line: the head line of the plane destroyed at the last strike
        :param head_column: the head column of the plane destroyed at the last strike
        """
        enemy_plane_id = self.__human_player.get_cell_plane_id(head_line, head_column)
        positions_list = []
        self.__human_player.fill_destroyed_cells(head_line, head_column, positions_list, enemy_plane_id)
        self.__computer_player.set_plane_cells_as_destroyed(positions_list)
        self.__human_number_of_planes -= 1
        
    def get_human_ally_board(self):
        return self.__human_player.get_ally_board_cell_status()

    def get_human_enemy_board(self):
        return self.__human_player.get_enemy_board_cell_status()

    def computer_add_planes(self):
        self.__computer_player.computer_add_planes_random_on_board()

    def human_out_of_planes(self):
        if self.__human_number_of_planes == 0:
            return True
        return False

    def computer_out_of_planes(self):
        if self.__computer_number_of_planes == 0:
            return True
        return False

