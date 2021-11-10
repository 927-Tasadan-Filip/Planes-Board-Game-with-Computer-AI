class StoreException(Exception):
    pass


class BoardValidationError(StoreException):
    def __init__(self, msg):
        super().__init__(self, msg)
        self._msg = msg

    @property
    def msg(self):
        return self._msg


class BoardValidator:

    def __init__(self, board):
        self.__board = board

    def validate_position(self, line, column):
        """
        Check if there exist the required position on the game board
        :param line: the line of the requested cell (type: positive integer)
        :param column: the column of the requested cell (type: positive integer)
        :return: it raise an BoardValidationError if the requested cell does not exist
        """
        try:
            line = int(line) - 1
            column = int(column) - 1
        except:
            raise BoardValidationError("This position is invalid")

        if line < 0 or line > (self.__board.lines - 1) or column < 0 or column > (self.__board.columns - 1):
            raise BoardValidationError("This position is invalid")

    def validate_new_move(self, line, column):
        """
        Check if the requested cell is eligible for a strike or not
        :param line: the line of the requested cell (type: positive integer)
        :param column: the column of the requested cell (type: positive integer)
        :return: raise an BoardValidationError if the requested cell has been already hit
        """
        if self.__board.is_empty(line, column) is False:
            raise BoardValidationError("This cell has been already hit")

    def validate_new_plane(self, head_line, head_column, tail_line, tail_column):
        """
        Check if the program can add a plane on the requested groups of cell or not
        :param head_line: the line of the head of the plane to be verified (type: positive integer)
        :param head_column: the column of the head of the plane to be verified (type: positive integer)
        :param tail_line: the line of the head of the plane to be verified (type: positive integer)
        :param tail_column: the column of the tail of the plane to be verified (type: positive integer)
        :return: raise an BoardValidationError if the requested group of cells is not empty so that a plane could't
        be added on those cells
        """
        # The plane is oriented horizontal
        if head_line == tail_line:

            if abs(head_column - tail_column) != 3:
                raise BoardValidationError("The distance between the tail and the head should be exactly 3 squares")

            if head_line < 1 or head_line > (self.__board.lines - 1):
                raise BoardValidationError("You can't place a plane outside the map")

            if head_column >= self.__board.columns or tail_column < 0 or tail_column > self.__board.columns or head_column < 0:
                raise BoardValidationError("You can't place a plane outside the map")

            if head_column < tail_column:
                for col in range(head_column, tail_column + 1):
                    if (col - head_column) % 2 == 1:
                        self.__board.is_empty(head_line - 1, col)
                        if self.__board.is_empty(head_line - 1, col) is False:
                            raise BoardValidationError("There is another plane on this position")
                        if self.__board.is_empty(head_line + 1, col) is False:
                            raise BoardValidationError("There is another plane on this position")

                    if self.__board.is_empty(head_line, col) is False:
                        raise BoardValidationError("There is another plane on this position")

            else:
                for col in range(tail_column, head_column + 1):
                    if (col - tail_column) % 2 == 0:
                        if self.__board.is_empty(head_line - 1, col) is False:
                            raise BoardValidationError("There is another plane on this position")
                        if self.__board.is_empty(head_line + 1, col) is False:
                            raise BoardValidationError("There is another plane on this position")

                    if self.__board.is_empty(head_line, col) is False:
                        raise BoardValidationError("There is another plane on this position")

        # The plane is oriented vertical
        elif head_column == tail_column:

            if abs(head_line - tail_line) != 3:
                raise BoardValidationError("The distance between the tail and the head should be exactly 3 squares")

            if head_column < 1 or head_column > (self.__board.columns - 1):
                raise BoardValidationError("You can't place a plane outside the map")

            if head_line >= self.__board.columns or tail_line < 0 or tail_line >= self.__board.columns or head_line < 0:
                raise BoardValidationError("You can't place a plane outside the map")

            if head_line < tail_line:
                for lin in range(head_line, tail_line + 1):
                    if (lin - head_line) % 2 == 1:
                        if self.__board.is_empty(lin, tail_column - 1) is False:
                            raise BoardValidationError("There is another plane on this position")
                        if self.__board.is_empty(lin, tail_column + 1) is False:
                            raise BoardValidationError("There is another plane on this position")

                    if self.__board.is_empty(lin, tail_column) is False:
                        raise BoardValidationError("There is another plane on this position")

            else:
                for lin in range(tail_line, head_line + 1):
                    if (lin - tail_line) % 2 == 0:
                        if self.__board.is_empty(lin, tail_column - 1) is False:
                            raise BoardValidationError("There is another plane on this position")
                        if self.__board.is_empty(lin, tail_column + 1) is False:
                            raise BoardValidationError("There is another plane on this position")

                    if self.__board.is_empty(lin, tail_column) is False:
                        raise BoardValidationError("There is another plane on this position")

        else:
            raise BoardValidationError("The plane should have the body either on the same line, either on the same column")

