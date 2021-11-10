from Player.Player import Player
import random
from Board.board_validator import BoardValidationError


class Computer(Player):

    def __init__(self):
        super().__init__()

    def computer_add_planes_random_on_board(self):
        """
        Computer adds a new plane on board by calculating randomly the head line, head column and the orientation of it
        """
        number_of_planes = 0

        while number_of_planes <= 3:
            number_of_planes += 1

            plane_orientation = random.choice(["vertical", "horizontal"])
            if plane_orientation == "vertical":
                plane_direction = random.choice(["up", "down"])

                if plane_direction == "up":
                    head_line = random.randint(0, 6)
                    head_column = random.randint(1, 8)
                    tail_line = head_line + 3
                    tail_column = head_column

                else:
                    head_line = random.randint(3, 9)
                    head_column = random.randint(1, 8)
                    tail_line = head_line - 3
                    tail_column = head_column

            else:
                plane_orientation = random.choice(["left", "right"])

                if plane_orientation == "left":
                    head_line = random.randint(1, 8)
                    head_column = random.randint(0, 6)
                    tail_line = head_line
                    tail_column = head_column + 3

                else:
                    head_line = random.randint(1, 8)
                    head_column = random.randint(3, 9)
                    tail_line = head_line
                    tail_column = head_column - 3

            try:
                Player.add_new_plane(self, head_line, head_column, tail_line, tail_column, number_of_planes)
            except BoardValidationError:
                number_of_planes -= 1

