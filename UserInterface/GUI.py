from tkinter import *
from GameEngine.MainEngine import GameEngine

from Board.board_validator import BoardValidationError


class GraphicalUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Planes")

        self.__game_engine = GameEngine()
        self.planes_added = 1
        self.__turn = 0


    @property
    def turn(self):
        return self.__turn

    def table_graphic_interface(self, root, matrix, start_col, total_rows, total_columns):

        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):

                if start_col > 5 and j == 0:
                    self.e = Entry(root, width=3, bg='black',
                                   font=('Times New Roman', 16, 'bold'))
                else:
                    if i == 0:
                        self.e = Entry(root, width=3, fg='black',
                                       font=('Times New Roman', 16, 'bold'))
                    else:
                        if start_col == 0:
                            if j == 0:
                                self.e = Entry(root, width=3, fg='black',
                                               font=('Times New Roman', 16, 'bold'))
                            else:
                                self.e = Entry(root, width=3, fg='blue',
                                               font=('Arial', 16))
                        else:
                            if j == 1:
                                self.e = Entry(root, width=3, fg='black',
                                               font=('Times New Roman', 16, 'bold'))
                            else:
                                self.e = Entry(root, width=3, fg='blue',
                                               font=('Arial', 16))


                self.e.grid(row=i, column=start_col + j)
                self.e.insert(END, matrix[i][j])

    def transform_human_ally_board_in_display_mode(self):
        ally_board_status = self.__game_engine.get_human_ally_board()
        printable_ally_board = []
        counter_columns_string_list = [""]

        for index in range(1, 11):
            counter_columns_string_list.append(str(index))
        printable_ally_board.append(counter_columns_string_list)

        for line_index in range(0, 10):
            line_str = [line_index + 1]
            for column_index in range(0, 10):
                if ally_board_status[line_index][column_index] in ["head", "body"]:
                    line_str.append(chr(9633))
                elif ally_board_status[line_index][column_index] in ["body_hit", "destroyed"]:
                    line_str.append(chr(9632))
                elif ally_board_status[line_index][column_index] == "hit":
                    line_str.append("X")
                else:
                    line_str.append(" ")
            line_str.append("/")
            printable_ally_board.append(line_str)

        return printable_ally_board

    def transform_human_enemy_board_in_display_mode(self):
        enemy_board_status = self.__game_engine.get_human_enemy_board()
        printable_enemy_board = []
        counter_columns_string_list = ["", ""]

        for index in range(1, 11):
            counter_columns_string_list.append(str(index))
        printable_enemy_board.append(counter_columns_string_list)

        for line_index in range(0, 10):
            line_str = ["", line_index + 1]
            for column_index in range(0, 10):
                if enemy_board_status[line_index][column_index] == "":
                    message = " "
                elif enemy_board_status[line_index][column_index] == "empty":
                    message = "X"
                elif enemy_board_status[line_index][column_index] == "hit":
                    message = "o"
                else:
                    message = chr(10687)

                line_str.append(message)
            line_str.append("/")
            printable_enemy_board.append(line_str)

        return printable_enemy_board

    def display_both_boards(self, game_frame):
        Label(game_frame, text="Your board", font=10).grid(row=0, column=0)
        Label(game_frame, text="Enemy board", font=10).grid(row=0, column=1)

        ally_board_frame = Frame(game_frame)
        ally_board_frame.grid(row=1, column=0)

        enemy_board_frame = Frame(game_frame)
        enemy_board_frame.grid(row=1, column=1)

        printable_human_ally_board = self.transform_human_ally_board_in_display_mode()
        printable_human_enemy_board = self.transform_human_enemy_board_in_display_mode()
        self.table_graphic_interface(ally_board_frame, printable_human_ally_board, 0, 11, 11)
        self.table_graphic_interface(enemy_board_frame, printable_human_enemy_board, 12, 11, 12)

    def clicked_strike(self, current_level, game_frame, strike_line, strike_column):
        try:
            self.__game_engine.validate_board_position(strike_line, strike_column)
            last_hit_cell_status = self.__game_engine.human_strike(int(strike_line) - 1, int(strike_column) - 1)
            if last_hit_cell_status not in ["body", "head"]:
                self.__turn += 1
            game_frame.destroy()
            self.gui_game_run(current_level, "")
        except BoardValidationError as ve:
            message = "Error: " + str(ve.msg)
            game_frame.destroy()
            self.gui_game_run(current_level, message)

    def gui_game_run(self, current_level, error_message):

        if self.__game_engine.human_out_of_planes():
            game_frame = Frame(current_level)
            game_frame.grid(row=0, column=0)
            Label(game_frame, text="You lost!", fg="Red", width=20, height=20, font=20).grid(row=0, column=0)

        elif self.__game_engine.computer_out_of_planes():
            game_frame = Frame(current_level)
            game_frame.grid(row=0, column=0)
            Label(game_frame, text="You won!", fg="Red", width=20, height=20, font=20).grid(row=0, column=0)

        elif self.turn % 2 == 0:
            game_frame = Frame(current_level)
            game_frame.grid(row=0,column=0)
            self.display_both_boards(game_frame)
            strike_frame = Frame(game_frame)
            strike_frame.grid(row=12,column=0)
            Label(strike_frame, text="Line to strike >>", font=10).grid(row=0, column=0)
            strike_line = Entry(strike_frame, width=30, font=10)
            strike_line.grid(row=0, column=1)
            Label(strike_frame, text="Column to strike >>", font=10).grid(row=1, column=0)
            strike_column = Entry(strike_frame, width=30, font=10)
            strike_column.grid(row=1, column=1)
            Button(strike_frame, text="STRIKE", font=10, bg='purple', fg='white',
                   command=lambda: self.clicked_strike(current_level, game_frame, strike_line.get(), strike_column.get())).grid(row=2, column=0)
            if error_message != "":
                status = Entry(strike_frame, width=30, font=5, fg="blue", bg="yellow")
                status.insert(0, str(error_message))
                status.grid(row=2, column=1)
                message = ""
        else:
            last_hit_cell_status = self.__game_engine.computer_strike()
            if last_hit_cell_status not in ["body", "head"]:
                self.__turn += 1
            self.gui_game_run(current_level, "")

    def clicked_add_plane(self, frame, board_frame, current_level, head_line, head_column, tail_line, tail_column):
        try:

            self.__game_engine.human_add_new_plane(head_line, head_column, tail_line, tail_column, self.planes_added)
            frame.destroy()
            board_frame.destroy()
            self.planes_added += 1
            if self.planes_added <= 3:
                self.gui_human_add_planes(current_level)
            else:
                self.gui_game_run(current_level, "")

        except BoardValidationError as ve:
            message = "Error: " + str(ve.msg)
            status = Entry(frame, width=40, font=10, fg="blue", bg="yellow")
            status.insert(0, str(message))
            status.grid(row=5, column=1)

    def gui_human_add_planes(self, current_level):
        frame = Frame(current_level)
        frame.grid(row=0, column=0)
        board_frame = Frame(current_level)
        board_frame.grid(row=1, column=0)

        printable_human_ally_board = self.transform_human_ally_board_in_display_mode()
        self.table_graphic_interface(board_frame, printable_human_ally_board, 0, 11, 11)
        Label(frame, text="Your board status", font=10).grid(row=6, column=1)

        if self.planes_added == 1:
            Label(frame, text="First plane head line", font=10).grid(row=1, column=0)
            head_line_1 = Entry(frame, width=40, font=10)
            head_line_1.grid(row=1, column=1)

            Label(frame, text="First plane head column", font=10).grid(row=2, column=0)
            head_column_1 = Entry(frame, width=40, font=10)
            head_column_1.grid(row=2, column=1)

            Label(frame, text="First plane tail line", font=10).grid(row=3, column=0)
            tail_line_1 = Entry(frame, width=40, font=10)
            tail_line_1.grid(row=3, column=1)

            Label(frame, text="First plane tail column", font=10).grid(row=4, column=0)
            tail_column_1 = Entry(frame, width=40, font=10)
            tail_column_1.grid(row=4, column=1)

            Button(frame, text="Add first plane", font=10, bg='purple', fg='white',
                   command=lambda: self.clicked_add_plane(frame, board_frame, current_level, head_line_1.get(), head_column_1.get(), tail_line_1.get(),
                                                          tail_column_1.get())).grid(row=5, column=0)

        elif self.planes_added == 2:
            Label(frame, text="Second plane head line", font=10).grid(row=1, column=0)
            head_line = Entry(frame, width=40, font=10)
            head_line.grid(row=1, column=1)

            Label(frame, text="Second plane head column", font=10).grid(row=2, column=0)
            head_column = Entry(frame, width=40, font=10)
            head_column.grid(row=2, column=1)

            Label(frame, text="Second plane tail line", font=10).grid(row=3, column=0)
            tail_line = Entry(frame, width=40, font=10)
            tail_line.grid(row=3, column=1)

            Label(frame, text="Second plane tail column", font=10).grid(row=4, column=0)
            tail_column = Entry(frame, width=40, font=10)
            tail_column.grid(row=4, column=1)

            Button(frame, text="Add second plane", font=10, bg='purple', fg='white',
                   command=lambda: self.clicked_add_plane(frame, board_frame, current_level, head_line.get(), head_column.get(), tail_line.get(),
                                                          tail_column.get())).grid(row=5, column=0)

        elif self.planes_added == 3:
            Label(frame, text="Third plane head line", font=10).grid(row=1, column=0)
            head_line = Entry(frame, width=40, font=10)
            head_line.grid(row=1, column=1)

            Label(frame, text="Third plane head column", font=10).grid(row=2, column=0)
            head_column = Entry(frame, width=40, font=10)
            head_column.grid(row=2, column=1)

            Label(frame, text="Third plane tail line", font=10).grid(row=3, column=0)
            tail_line = Entry(frame, width=40, font=10)
            tail_line.grid(row=3, column=1)

            Label(frame, text="Third plane tail column", font=10).grid(row=4, column=0)
            tail_column = Entry(frame, width=40, font=10)
            tail_column.grid(row=4, column=1)

            Button(frame, text="Add third plane", font=10, bg='purple', fg='white',
                   command=lambda: self.clicked_add_plane(frame, board_frame, current_level, head_line.get(), head_column.get(),
                                                          tail_line.get(),
                                                          tail_column.get())).grid(row=5, column=0)

    def run_game(self):
        current_level = Toplevel()
        self.__game_engine.computer_add_planes()
        self.gui_human_add_planes(current_level)

    def instructions(self):
        curent_level = Toplevel()
        Label(curent_level, text="The game has 2 phases", font=10, fg="blue").grid(row=0, column=0)
        Label(curent_level, text="Phase I", font=10, fg="blue").grid(row=1, column=0)
        Label(curent_level, text="In this phase each player adds 3 planes on board", font=10, fg="blue").grid(row=2, column=0)
        Label(curent_level, text="Phase II", font=10, fg="red").grid(row=3, column=0)
        Label(curent_level, text="In this phase every player strike once on the enemy board", font=10, fg="red").grid(row=4, column=0)
        Label(curent_level, text="If the last strike hits an enemy plane that player has one more strike to perform", font=10, fg="red").grid(row=5, column=0)
        Label(curent_level, text="After one of the players manages to destroy the other player's planes the game ends and he is declared as winner", font=10, fg="red").grid(row=6, column=0)



    def run_menu(self):
        Button(self.root, text="Play", font=10, command=self.run_game, width=20, bg='yellow').grid(row=0, column=0)
        Button(self.root, text="Instructions", font=10, command=self.instructions, width=20, bg='yellow').grid(row=1, column=0)
        self.root.mainloop()


