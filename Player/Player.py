from Board.board_validator import BoardValidator
from Board.board import Board


class Player:

    def __init__(self):
        self.ally_board = Board(10, 10)
        self.enemy_board = Board(10, 10)
        self.ally_validator = BoardValidator(self.ally_board)
        self._enemy_validator = BoardValidator(self.enemy_board)

    def strike(self, line, column, enemy_cell_status):
        """
        Perform a strike on the enemy board
        :param line: line of the strike (type: positive integer)
        :param column: column of the strike (type: positive integer)
        :param enemy_cell_status: the status of the enemy board "ally board" on this particular cell in
        order to update the current strikning player"enmey board" with the value (type: string)
        (if the enemy has on it's board "body" the strike cell "enemy board" of the current player should be updated with "hit" value)
        """
        if enemy_cell_status == "":
            self.enemy_board.set_cell_status(line, column, "empty")

        elif enemy_cell_status == "body" or enemy_cell_status == "head":
            self.enemy_board.set_cell_status(line, column, "hit")

    def add_new_plane(self, head_line, head_column, tail_line, tail_column, plane_id):
        """
        Add a new plane on the "ally board"
        :param head_line: the line of the head of the plane to be added (type: positive integer)
        :param head_column: the column of the head of the plane to be added (type: positive integer)
        :param tail_line: the line of the head of the plane to be added (type: positive integer)
        :param tail_column: the column of the tail of the plane to be added (type: positive integer)
        :param plane_id: the id of the plane to be added (type: positive integer)
        """
        self.ally_validator.validate_position(head_line, head_column)
        self.ally_validator.validate_position(tail_line, tail_column)
        head_line = int(head_line) - 1
        head_column = int(head_column) - 1
        tail_line = int(tail_line) - 1
        tail_column = int(tail_column) - 1

        self.ally_validator.validate_new_plane(head_line, head_column, tail_line, tail_column)
        self.ally_board.create_plane_on_board(head_line, head_column, tail_line, tail_column, plane_id)

    def get_ally_cell_status(self, line, column):
        return self.ally_board.get_cell_status(line, column)

    def get_enemy_cell_status(self, line, column):
        return self.enemy_board.get_cell_status(line, column)

    def get_last_hit_cell_status(self, line, column):
        return self.ally_board.get_cell_status(line, column)

    def get_cell_plane_id(self, line, column):
        return self.ally_board.get_cell_plane_id(line, column)

    def fill_destroyed_cells(self, line, column, positions_list, enemy_plane_id):
        """
        This is the flood-fill recursive algorithm which will update the boards after a plane is destroyed by filling those
        cells that belongs to the destroyed plane with "destroy" value
        :param line: the line of the cell that should be updated with "destroy" value
        :param column: the collumn of the cell that should be updated with "destroy" value
        :param positions_list: the positions of the cells that were updated with "desstroy" value (type: list of tuples)
        :param enemy_plane_id: the id of the plane that was destroyed (type: positive integer)
        """
        self.ally_board.set_cell_status(line, column, "destroyed")
        positions_list.append([line, column])

        if self.ally_board.get_cell_status(line - 1, column) in ["body", "head", "body_hit"]:
            if self.ally_board.get_cell_plane_id(line - 1, column) == enemy_plane_id:
                self.fill_destroyed_cells(line - 1, column, positions_list, enemy_plane_id)

        if self.ally_board.get_cell_status(line + 1, column) in ["body", "head", "body_hit"]:
            if self.ally_board.get_cell_plane_id(line + 1, column) == enemy_plane_id:
                self.fill_destroyed_cells(line + 1, column, positions_list, enemy_plane_id)

        if self.ally_board.get_cell_status(line, column - 1) in ["body", "head", "body_hit"]:
            if self.ally_board.get_cell_plane_id(line, column - 1) == enemy_plane_id:
                self.fill_destroyed_cells(line, column - 1, positions_list, enemy_plane_id)

        if self.ally_board.get_cell_status(line, column + 1) in ["body", "head", "body_hit"]:
            if self.ally_board.get_cell_plane_id(line, column + 1) == enemy_plane_id:
                self.fill_destroyed_cells(line, column + 1, positions_list, enemy_plane_id)

    def set_plane_cells_as_destroyed(self, positions_list):
        for element in positions_list:
            self.enemy_board.set_cell_status(element[0], element[1], "destroyed")

    def get_ally_board_cell_status(self):
        return self.ally_board.get_grid_board_status_as_list_of_lists_of_cells()

    def get_enemy_board_cell_status(self):
        return self.enemy_board.get_grid_board_status_as_list_of_lists_of_cells()

    def update_board_after_strike(self, line, column, old_value):
        if old_value == "":
            self.ally_board.set_cell_status(line, column, "hit")
        if old_value == "body":
            self.ally_board.set_cell_status(line, column, "body_hit")




