from GameEngine.MainEngine import GameEngine
from Board.board_validator import BoardValidationError


class UserInterface:
    def __init__(self):
        self.__game_engine = GameEngine()
        self.__turn = 0

    @property
    def turn(self):
        return self.__turn

    def __ui_human_add_planes(self):
        number_of_planes = 0
        while number_of_planes < 3:
            number_of_planes += 1
            head_line = input("Line of the head of plane >> ")
            head_column = input("Column of the head of plane >> ")
            tail_line = input("Line of the tail of plane >> ")
            tail_column = input("Column of the tail of plane >> ")

            try:
                self.__game_engine.human_add_new_plane(head_line, head_column, tail_line, tail_column, number_of_planes)
            except BoardValidationError as ve:
                print("Error: ", str(ve.msg))
                print("Try to add the plane on a different position")
                number_of_planes -= 1

    def __read_strike_data(self):
        line = input("Enter the line of the next strike >> ")
        column = input("Enter the column of the next strike >> ")

        self.__game_engine.validate_board_position(line, column)
        return [int(line) - 1, int(column) - 1]

    def __ui_human_strike(self):
        line, column = self.__read_strike_data()
        last_hit_cell_status = self.__game_engine.human_strike(line, column)
        if last_hit_cell_status not in ["body", "head"]:
            self.__turn += 1

    def __ui_computer_strike(self):
        last_hit_cell_status = self.__game_engine.computer_strike()
        if last_hit_cell_status not in ["body", "head"]:
            self.__turn += 1

    def __display_human_ally_board(self):
        print()
        print("ALLY BOARD")
        ally_board_status = self.__game_engine.get_human_ally_board()
        counter_columns_string = " "
        for index in range(1, 11):
            counter_columns_string += "   " + str(index)
        print(counter_columns_string)
        for line_index in range(0, 10):
            line_str = str(line_index + 1) + "  "
            for column_index in range(0, 10):
                if ally_board_status[line_index][column_index] in ["head", "body"]:
                    line_str += "[" + chr(9633) + "]" + " "
                elif ally_board_status[line_index][column_index] in ["body_hit", "destroyed"]:
                    line_str += "[" + chr(9632) + "]" + " "
                elif ally_board_status[line_index][column_index] == "hit":
                    line_str += "[" + "X" + "]" + " "
                else:
                    line_str += "[" + " " + "]" + " "
            line_str += "\n"
            print(line_str)

    def __display_human_enemy_board(self):
        print()
        print("ENEMY BOARD")
        enemy_board_status = self.__game_engine.get_human_enemy_board()
        counter_columns_string = " "
        for index in range(1, 11):
            counter_columns_string += "   " + str(index)
        print(counter_columns_string)
        for line_index in range(0, 10):
                line_str = str(line_index + 1) + "  "
                for column_index in range(0, 10):
                    if enemy_board_status[line_index][column_index] == "":
                        message = " "
                    elif enemy_board_status[line_index][column_index] == "empty":
                        message = "X"
                    elif enemy_board_status[line_index][column_index] == "hit":
                        message = "o"
                    else:
                        message = chr(10687)

                    line_str += "[" + message + "]" + " "
                line_str += "\n"
                print(line_str)

    @staticmethod
    def __display_entry_phase():
        print("Welcome to planes!")
        print()
        print("The game has 2 phases")
        print()
        print("Phase I")
        print("In this phase each player adds 3 planes on board")

    @staticmethod
    def __display_game_phase():
        print()
        print("Phase II - Game phase")
        print("In this phase every player strike once on the enemy board")
        print("If the last strike hits an enemy plane that player has one more strike to perform")
        print("After one of the players manages to destroy the other player's planes the game ends and he is declared as winner")
        print()
        print("Good luck!")

    def run_game(self):
        self.__display_entry_phase()
        self.__ui_human_add_planes()
        self.__game_engine.computer_add_planes()
        done = False
        self.__display_game_phase()
        while not done:
            if self.turn % 2 == 0:
                self.__display_human_ally_board()
                self.__display_human_enemy_board()
                try:
                    self.__ui_human_strike()
                except BoardValidationError as ve:
                    print("Error: " + str(ve.msg))
                    print("Try to hit another position")

            else:
                self.__ui_computer_strike()


            if self.__game_engine.human_out_of_planes():
                self.__display_human_ally_board()
                print("Computer won!")
                done = True

            elif self.__game_engine.computer_out_of_planes():
                self.__display_human_enemy_board()
                print("Human won!")
                done = True
