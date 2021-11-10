from Board.cell import Cell


class Board:

    def __init__(self, lines, columns, empty_value=""):
        self.__lines = lines
        self.__columns = columns
        self.__empty_value = empty_value

        self.__grid_board = self.__create_board()

    @property
    def lines(self):
        """
        :return: the number of lines from the board (type: positive integer)
        """
        return self.__lines

    @property
    def columns(self):
        """
        :return: the number of columns from the board (type: positive integer)
        """
        return self.__columns

    def is_empty(self, line, column):
        """
        Check if the given cell from the board is empty or not
        :param line: the line of the cell to be checked (type: positive integer)
        :param column: the column of the cell to be checked (type: positive integer)
        :return: if the cell is empty returns True, else it returns False (type: boolean value)
        """
        try:
            if self.__grid_board[line][column].status == self.__empty_value:
                return True
            else:
                return False
        except:
            return True

    def __create_board(self):
        """
        Create a grid which is going to represent the game board where every element is a Cell object
        :return: the game board with the cell objects (type: list of list of objects)
        """
        return [[Cell(line, column, self.__empty_value, 0) for column in range(self.__columns)]
                for line in range(self.__lines)]

    def get_cell_status(self, line, column):
        """
        Return the value of a particular cell from the board (this is a getter method)
        :param line: the line of the requested cell (type: positive integer)
        :param column: the column of the requested cell (type: positive integer)
        :return: the value of the cell (type: string)
        """
        if line < 0 or line > (self.lines - 1) or column < 0 or column > (self.columns - 1):
            return None
        return self.__grid_board[line][column].status

    def set_cell_status(self, line, column, new_status):
        """
        This method will change the status (value) of a given cell with the new one
        :param line: the line of the requested cell (type: positive integer)
        :param column: the column of the requested cell (type: positive integer)
        :param new_status: the new status of the given cell (type: string)
        """
        self.__grid_board[line][column].status = new_status

    def get_grid_board_status_as_list_of_lists_of_cells(self):
        """
        This method will return the board as a grid where each element is the cell status (value)
        :return: a grid of cell statuses (type: list of list of strings)
        """
        aux_board = []
        for line in range(self.__lines):
            aux_board.append([cell.status for cell in self.__grid_board[line]])

        return aux_board

    def set_cell_plane_status(self, line, column, new_status, new_plane_id):
        """
        If a cell contains a part of the plane it will recieve that plane id in order to be easier for the program to
        check if a cell is a part of a plane that was destroyed in order to apply the flood-fill algorithm correctly
        :param line: the line of the requested cell (type: positive integer)
        :param column: the column of the requested cell (type: positive integer)
         :param new_status: the new status of the given cell, it will be either "body" if it's part of the body of
          the plane or "head" if it's the head of a particular plane (type: string)
        :param new_plane_id: the id of the plane which occupies this cell (type: positive integer)
        """
        self.__grid_board[line][column].status = new_status
        self.__grid_board[line][column].plane_id = new_plane_id

    def get_cell_plane_id(self, line, column):
        """

        :param line: the line of the requested cell (type: positive integer)
        :param column: the column of the requested cell (type: positive integer)
        :return: returns the id of the plane that occupies the requested cell
        """
        return self.__grid_board[line][column].plane_id

    def create_plane_on_board(self, head_line, head_column, tail_line, tail_column, plane_id):
        """
        Creates a plane on the board with a fixed shape
        :param head_line: the line of the head of the plane to be created (type: positive integer)
        :param head_column: the column of the head of the plane to be created (type: positive integer)
        :param tail_line: the line of the head of the plane to be created (type: positive integer)
        :param tail_column: the column of the tail of the plane to be created (type: positive integer)
        :param plane_id: the id of the plane to be created (type: positive integer)
        """
        if head_line == tail_line:
            if head_column < tail_column:
                for col in range(head_column + 1, tail_column + 1):

                    if (col - head_column) % 2 == 1:
                        self.set_cell_plane_status(head_line - 1, col, "body", plane_id)
                        self.set_cell_plane_status(head_line + 1, col, "body", plane_id)

                    self.set_cell_plane_status(head_line, col, "body", plane_id)

            else:
                for col in range(tail_column, head_column):

                    if (col - tail_column) % 2 == 0:
                        self.set_cell_plane_status(head_line - 1, col, "body", plane_id)
                        self.set_cell_plane_status(head_line + 1, col, "body", plane_id)

                    self.set_cell_plane_status(head_line, col, "body", plane_id)

        elif head_column == tail_column:
            if head_line < tail_line:
                for lin in range(head_line + 1, tail_line + 1):

                    if (lin - head_line) % 2 == 1:
                        self.set_cell_plane_status(lin, head_column - 1, "body", plane_id)
                        self.set_cell_plane_status(lin, head_column + 1, "body", plane_id)

                    self.set_cell_plane_status(lin, head_column, "body", plane_id)

            else:
                for lin in range(tail_line, head_line):

                    if (lin - tail_line) % 2 == 0:
                        self.set_cell_plane_status(lin, head_column - 1, "body", plane_id)
                        self.set_cell_plane_status(lin, head_column + 1, "body", plane_id)

                    self.set_cell_plane_status(lin, head_column, "body", plane_id)

        self.set_cell_plane_status(head_line, head_column, "head", plane_id)

