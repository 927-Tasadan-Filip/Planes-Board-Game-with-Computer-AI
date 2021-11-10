import random
from Board.board_validator import BoardValidationError


class Strategy:
    def __init__(self, computer_enemy_board, human_ally_board, computer_enemy_board_validator):
        self.__computer_enemy_board = computer_enemy_board
        self.__human_ally_board = human_ally_board
        self.__enemy_board_validator = computer_enemy_board_validator
        self.__last_hit_cell_status = ""
        self.__central_pivot_position = [-1, -1]
        self.__list_of_all_pivots = []
        self.__done_directional_hitting = False
        self.__done_hit_above = False
        self.__hit_above_position = []
        self.__done_hit_bellow = False
        self.__hit_bellow_position = []
        self.__done_hit_left = False
        self.__hit_left_position = []
        self.__done_hit_right = False
        self.__hit_right_position = []
        self.first_strike = False



    def update_positional_hit_tuples(self, new_position):
        """
        It will update all the positional lists when the central pivot is updated in order to start striking near the new pivot position
        :param new_position: the new position of the central pivot
        """
        self.__hit_above_position = new_position
        self.__hit_bellow_position = new_position
        self.__hit_left_position = new_position
        self.__hit_right_position = new_position
        self.__done_directional_hitting = False
        self.__done_hit_above = False
        self.__done_hit_bellow = False
        self.__done_hit_left = False
        self.__done_hit_right = False

    def update_last_hit_cell_status(self, new_status):
        self.__last_hit_cell_status = new_status

    def update_central_pivot_position(self, new_position):
        if new_position != [-1, -1]:
            self.__list_of_all_pivots.append(new_position)
            self.update_positional_hit_tuples(new_position[:])
        self.__central_pivot_position = new_position[:]

    @property
    def central_pivot_position(self):
        return self.__central_pivot_position

    @property
    def central_pivot_line(self):
        return self.__central_pivot_position[0]

    @property
    def central_pivot_column(self):
        return self.__central_pivot_position[1]

    @property
    def last_hit_cell_status(self):
        return self.__last_hit_cell_status

    def is_empty_last_hit_cell_status(self):
        if self.__last_hit_cell_status == "":
            return True
        return False
    
    def is_empty_central_pivot(self):
        if self.__central_pivot_position == [-1, -1]:
            return True
        return False

    def __check_if_strike_position_is_valid(self, strike_line, strike_column):
        """
        It will check if the new strike position is valid or not and return the Truth value of this checkings
        :param strike_line: line of the strike (type: positive integer)
        :param strike_column: column of the strike (type: positive integer)
        :return: the truth value of the checking (type: boolean value)
        """
        try:
            self.__enemy_board_validator.validate_position(strike_line, strike_column)
            self.__enemy_board_validator.validate_new_move(strike_line, strike_column)
            return True
        except BoardValidationError:
            return False

    def search_for_hit_cell(self):
        """
        It will search if there is another hit plane on the map which  was not destroyed in order to take it as a pivot
        :return: the plane which was not destroyed position or in case there is no plane which was not destoryed return -1
        """
        for line in range(0, 10):
            for column in range(0, 10):
                current_cell_status = self.__human_ally_board.get_cell_status(line, column)
                if current_cell_status == "body_hit" and [line, column] not in self.__list_of_all_pivots:
                    return [line, column]
        return [-1, -1]

    def computer_random_strike(self):
        """
        It search for a random cell in order to hit there if the central pivot is empty
        :return: the random strike positions (type: list with 2 elements)
        """
        if self.first_strike is False:
            self.first_strike = True
            strike_line = 2
            strike_column = 6
        else:
            strike_line = random.randint(0, 9)
            strike_column = random.randint(0, 9)

        while not self.__check_if_strike_position_is_valid(strike_line, strike_column):
            strike_line = random.randint(0, 9)
            strike_column = random.randint(0, 9)

        self.update_last_hit_cell_status(self.__human_ally_board.get_cell_status(strike_line, strike_column))
        if self.last_hit_cell_status == "body":
            self.update_central_pivot_position([strike_line, strike_column])
        return [strike_line, strike_column]

    def check_pivot_status(self):
        """
        It checks if the plane which belonged to the pivot was detroyed in order to take a new pivot, or if all postitional hitting are done
        """
        pivot_status = self.__computer_enemy_board.get_cell_status(self.__central_pivot_position[0], self.__central_pivot_position[1])
        if pivot_status == "destroyed":
            self.__central_pivot_position = [-1, -1]
        if self.__done_directional_hitting is True:
            self.__central_pivot_position = [-1, -1]

    def strike_above(self):
        """
        It will strike above the pivot as long as it can until it hits an empty cell or it goes out of the board
        :return: the next strike position above the pivot
        """
        strike_line = self.__hit_above_position[0] - 1
        strike_column = self.__hit_above_position[1]
        if self.__check_if_strike_position_is_valid(strike_line, strike_column) is False:
            self.__done_hit_above = True
            return [-1, -1]
        self.update_last_hit_cell_status(self.__human_ally_board.get_cell_status(strike_line, strike_column))
        if self.__last_hit_cell_status in ["body_hit", "destroyed"]:
            self.__done_hit_above = True
            return [-1, -1]
        if self.__last_hit_cell_status == "" or self.__last_hit_cell_status == "head":
            self.__done_hit_above = True
        self.__hit_above_position = [strike_line, strike_column][:]
        return [strike_line, strike_column][:]

    def strike_bellow(self):
        """
        It will strike below the pivot as long as it can until it hits an empty cell or it goes out of the board
        :return: the next strike position below the pivot
        """
        strike_line = self.__hit_bellow_position[0] + 1
        strike_column = self.__hit_bellow_position[1]
        if self.__check_if_strike_position_is_valid(strike_line, strike_column) is False:
            self.__done_hit_bellow = True
            return [-1, -1]
        self.update_last_hit_cell_status(self.__human_ally_board.get_cell_status(strike_line, strike_column))
        if self.__last_hit_cell_status in ["body_hit", "destroyed"]:
            self.__done_hit_bellow = True
            return [-1, -1]
        if self.__last_hit_cell_status == "" or self.__last_hit_cell_status == "head":
            self.__done_hit_bellow = True
        self.__hit_bellow_position = [strike_line, strike_column][:]
        return [strike_line, strike_column][:]

    def strike_left(self):
        """
        It will strike left the pivot as long as it can until it hits an empty cell or it goes out of the board
        :return: the next strike position left the pivot
        """
        strike_line = self.__hit_left_position[0]
        strike_column = self.__hit_left_position[1] - 1
        if self.__check_if_strike_position_is_valid(strike_line, strike_column) is False:
            self.__done_hit_left = True
            return [-1, -1]
        self.update_last_hit_cell_status(self.__human_ally_board.get_cell_status(strike_line, strike_column))
        if self.__last_hit_cell_status in ["body_hit", "destroyed"]:
            self.__done_hit_left = True
            return [-1, -1]
        if self.__last_hit_cell_status == "" or self.__last_hit_cell_status == "head":
            self.__done_hit_left = True
        self.__hit_left_position = [strike_line, strike_column][:]
        return [strike_line, strike_column][:]

    def strike_right(self):
        """
        It will strike right the pivot as long as it can until it hits an empty cell or it goes out of the board
        :return: the next strike position right the pivot
         """
        strike_line = self.__hit_right_position[0]
        strike_column = self.__hit_right_position[1] + 1
        if self.__check_if_strike_position_is_valid(strike_line, strike_column) is False:
            self.__done_hit_right = True
            return [-1, -1]
        self.update_last_hit_cell_status(self.__human_ally_board.get_cell_status(strike_line, strike_column))
        if self.__last_hit_cell_status in ["body_hit", "destroyed"]:
            self.__done_hit_right = True
            return [-1, -1]
        if self.__last_hit_cell_status == "" or self.__last_hit_cell_status == "head":
            self.__done_hit_right = True
        self.__hit_right_position = [strike_line, strike_column][:]
        return [strike_line, strike_column][:]

    def check_if_done_directional_hitting(self):
        if self.__done_hit_above is True and self.__done_hit_bellow is True and self.__done_hit_left is True and self.__done_hit_right is True:
            self.__done_directional_hitting = True

    def calculate_next_strike_position(self):
        self.check_if_done_directional_hitting()
        self.check_pivot_status()

        if self.is_empty_central_pivot():
            position_tuple = self.search_for_hit_cell()
            if position_tuple == [-1, -1]:
                return self.computer_random_strike()

            else:

                self.update_central_pivot_position(position_tuple)

        if self.__done_hit_above is False:
            strike_above_position = self.strike_above()
            if strike_above_position != [-1, -1]:
                return strike_above_position

        if self.__done_hit_bellow is False:
            strike_bellow_position = self.strike_bellow()
            if strike_bellow_position != [-1, -1]:
                return strike_bellow_position

        if self.__done_hit_left is False:
            strike_left_position = self.strike_left()
            if strike_left_position != [-1, -1]:
                return strike_left_position

        if self.__done_hit_right is False:
            strike_right_position = self.strike_right()
            if strike_right_position != [-1, -1]:
                return strike_right_position

        self.calculate_next_strike_position()




