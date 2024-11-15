from chess_piece import ChessPiece
from board import Board
from chess_utils import BoardInfo
from chess_utils import PieceInfo


class Knight(ChessPiece):

    # Returns all possible knight moves
    def _get_knight_moves(self):

        return [
            (-2, -1),  # Two rows up
            (-2, 1),  # One column left / right
            (-1, -2),  # One row up
            (-1, 2),  # Two columns left / right
            (1, -2),  # One row down
            (1, 2),   # Two columns left / right
            (2, -1),  # Move two rows down
            (2, 1)    # One column left / right
        ]

    # Determines is the knight's movement is valid
    def _is_valid_knight_pattern(self, row_diff, col_diff):
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

    # Checks is the destination square is valid (Either off the board or the same color)

    def _is_valid_destination(self, dest_row, dest_col, board):
        square_type = board.get_square_info(dest_row, dest_col)
        return square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD

    # Checks to see if the move is able to be made to the destination square

    def is_legal_move(self, dest_row, dest_col, board):

        row_diff = abs(self._row - dest_row)
        col_diff = abs(self._col - dest_col)

        return (self._is_valid_knight_pattern(row_diff, col_diff) and
                self._is_valid_destination(dest_row, dest_col, board))

    # Calculates the position based on where it moved from
    def _calculate_new_position(self, direction):
        row_direction, col_direction = direction
        return (self._row + row_direction, self._col + col_direction)

    # Generates all moves for the knight given the current board state
    def generate_legal_moves(self, board_data, board):

        board_data[self._row][self._col] = self._label.value

        for direction in self._get_knight_moves():
            new_row, new_col = self._calculate_new_position(direction)

            if (super()._is_within_board(new_row, new_col) and
                    self._is_valid_destination(new_row, new_col, board)):
                board_data[new_row][new_col] = self._label.value

        return board_data


class Rook(ChessPiece):
    def _is_straight_line_move(self, row_diff, col_diff):
        return (row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0)

    # Returns the direction of the movement (moving up, down, or not moving)

    def _get_direction(self, dest_pos, current_pos):
        if dest_pos == current_pos:
            return 0
        elif dest_pos > current_pos:
            return 1
        else:
            return -1

     # Checks is the destination square is valid (Either off the board or the same color)

    def _is_valid_destination(self, square_type):
        return square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD

    # Finds if there are any pieces along the path to the destination

    def _is_path_clear(self, dest_row, dest_col, board):

        row_direction = self._get_direction(dest_row, self._row)
        col_direction = self._get_direction(dest_col, self._col)

        current_row = self._row + row_direction
        current_col = self._col + col_direction

        while current_row != dest_row or current_col != dest_col:
            if board.get_square_info(current_row, current_col) != BoardInfo.EMPTY:
                return False
            current_row += row_direction
            current_col += col_direction
        return True

    # Checks to see if the move is able to be made to the destination square

    def is_legal_move(self, dest_row, dest_col, board):
        # Check if staying in place
        if super()._is_same_position(dest_row, dest_col):
            return True

        row_diff = abs(self._row - dest_row)
        col_diff = abs(self._col - dest_col)

        if not self._is_straight_line_move(row_diff, col_diff):
            return False

        return (self._is_path_clear(dest_row, dest_col, board) and
                self._is_valid_destination(board.get_square_info(dest_row, dest_col)))

    # Calculates legal moves by direction
    def _get_moves_in_direction(self, row_direction, col_direction, board_data, board):

        new_row = self._row
        new_col = self._col

        while True:
            new_row += row_direction
            new_col += col_direction

            # Check board boundaries
            if not (0 <= new_row < 8 and 0 <= new_col < 8):
                break

            square_type = board.get_square_info(new_row, new_col)

            if square_type != BoardInfo.EMPTY:
                if square_type != self._color:
                    board_data[new_row][new_col] = self._label.value
                break

            board_data[new_row][new_col] = self._label.value

        return board_data

    # Generates legal moves for the piece

    def generate_legal_moves(self, board_data, board):

        board_data[self._row][self._col] = self._label.value

        directions = [
            (-1, 0),  # up
            (1, 0),  # down
            (0, -1),  # left
            (0, 1)]  # right

        # Generate moves for each direction
        for row_direction, col_direction in directions:
            board_data = self._get_moves_in_direction(
                row_direction, col_direction, board_data, board)

        return board_data


class WhitePawn(ChessPiece):

    # Ensures the piece is within the board
    def _is_within_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    # Checks if the square is empty

    def _is_empty_square(self, row, col, board):
        return board._board_info[row][col] is None

    # Checks if the piece is able to be captured

    def _is_capturable_piece(self, row, col, board):
        target_piece = board._board_info[row][col]
        return target_piece is not None and target_piece.get_color() == BoardInfo.BLACK

    # Determines is the move is able to be made

    def is_legal_move(self, dest_row, dest_col, board):
        if dest_row == self._row and dest_col == self._col:
            return True

        if not self._is_within_bounds(dest_row, dest_col):
            return False

        # One square movement
        if dest_col == self._col and dest_row == self._row + 1:
            return self._is_empty_square(dest_row, dest_col, board)

        # Two square movement
        if self._row == 1 and dest_col == self._col and dest_row == self._row + 2:
            return (self._is_empty_square(self._row + 1, self._col, board) and
                    self._is_empty_square(dest_row, dest_col, board))

        # Capturing diagonal pieces
        if abs(dest_col - self._col) == 1 and dest_row == self._row + 1:
            return self._is_capturable_piece(dest_row, dest_col, board)

        return False

    # Generates legal moves for the pawn, handling one and two square movement
    def generate_legal_moves(self, board_data, board):
        char_label = self._label.value

        # Staying in the same position
        if self._is_within_bounds(self._row, self._col):
            board_data[self._row][self._col] = char_label

        # Forward one square
        new_row = self._row + 1
        if (self._is_within_bounds(new_row, self._col) and
                self._is_empty_square(new_row, self._col, board)):
            board_data[new_row][self._col] = char_label

        # Two square movement
        if (self._row == 1 and
            self._is_within_bounds(self._row + 2, self._col) and
            self._is_empty_square(self._row + 1, self._col, board) and
                self._is_empty_square(self._row + 2, self._col, board)):
            board_data[self._row + 2][self._col] = char_label

        # Capturing diagonal pieces
        for new_col in [self._col - 1, self._col + 1]:
            new_row = self._row + 1
            if (self._is_within_bounds(new_row, new_col) and
                    self._is_capturable_piece(new_row, new_col, board)):
                board_data[new_row][new_col] = char_label

        return board_data


class Bishop(ChessPiece):

    # Checks if the piece can move to the destination square
    def is_legal_move(self, dest_row, dest_col, board):

        if not self._is_valid_starting_position(dest_row, dest_col):
            return False

        if not self._is_valid_diagonal_move(dest_row, dest_col):
            return False

        if not self._is_valid_destination(dest_row, dest_col, board):
            return False

        return self._is_path_clear(dest_row, dest_col, board)

    # Ensures the move is not to the current square
    def _is_valid_starting_position(self, dest_row, dest_col):
        return not (dest_row == self._row and dest_col == self._col)

    # Detemines is the move is diagonal

    def _is_valid_diagonal_move(self, dest_row, dest_col):
        row_diff = abs(self._row - dest_row)
        col_diff = abs(self._col - dest_col)
        return row_diff == col_diff

    # Checks if the destination square is a valid move

    def _is_valid_destination(self, dest_row, dest_col, board):
        square_type = board.get_square_info(dest_row, dest_col)
        return (square_type != self._color and
                square_type != BoardInfo.OFF_THE_BOARD)

    # Checks diagonal paths to the destination location to see if there are pieces along the path

    def _is_path_clear(self, dest_row, dest_col, board):

        if dest_row > self._row:
            row_step = 1
        else:
            row_step = -1

        if dest_col > self._col:
            col_step = 1
        else:
            col_step = -1

        curr_row = self._row + row_step
        curr_col = self._col + col_step

        while (curr_row != dest_row) and (curr_col != dest_col):
            if board.get_square_info(curr_row, curr_col) != BoardInfo.EMPTY:
                return False
            curr_row += row_step
            curr_col += col_step

        return True

    # Generates legal moves for the bishop
    def generate_legal_moves(self, board_data, board):
        char_label = self._label.value
        board_data[self._row][self._col] = char_label

        directions = [
            (-1, -1),  # top left
            (-1, 1),   # top right
            (1, -1),   # bottom left
            (1, 1)     # bottom right
        ]

        for direction in directions:
            self._mark_moves_in_direction(board_data, board, direction)

        return board_data

    # Marks all moves that are legal in the direction the move is being made
    def _mark_moves_in_direction(self, board_data, board, direction):

        row_direction, col_direction = direction
        new_row = self._row
        new_col = self._col

        while True:
            new_row += row_direction
            new_col += col_direction

            if not super()._is_within_board(new_row, new_col):
                break

            square_type = board.get_square_info(new_row, new_col)

            if square_type != BoardInfo.EMPTY:
                if square_type != self._color:
                    board_data[new_row][new_col] = self._label.value
                break

            board_data[new_row][new_col] = self._label.value


class Queen(ChessPiece):

    # Checks if the move is vertical, horizontal, or diagonal
    def _is_valid_direction(self, dest_row, dest_col):
        is_straight = self._row == dest_row or self._col == dest_col
        is_diagonal = abs(self._row - dest_row) == abs(self._col - dest_col)
        return is_straight or is_diagonal

    # Increment to keep track of each step taken.
    def _get_direction_steps(self, dest_row, dest_col):
        # Determine vertical step direction: no movement, down, or up
        if self._row == dest_row:
            row_step = 0
        elif dest_row > self._row:
            row_step = 1
        else:
            row_step = -1

        # Determine horizontal step direction: no movement, right, or left
        if self._col == dest_col:
            col_step = 0
        elif dest_col > self._col:
            col_step = 1
        else:
            col_step = -1

        return row_step, col_step

    # Checks to see if the path is clear step by step
    def _is_path_clear(self, dest_row, dest_col, board):
        row_step, col_step = self._get_direction_steps(dest_row, dest_col)
        current_row, current_col = self._row + row_step, self._col + col_step

        while current_row != dest_row or current_col != dest_col:
            if board._board_info[current_row][current_col] is not None:
                return False

            current_row += row_step
            current_col += col_step
        return True

    # Checks if destination square is empty or contains an opponents piece
    def _is_valid_destination(self, dest_row, dest_col, board):
        destination_piece = board._board_info[dest_row][dest_col]
        return destination_piece is None or destination_piece.get_color() != self.get_color()

    # Returns the possible directions for queen
    def _get_directions(self):
        return [
            (-1, 0),   # up
            (1, 0),    # down
            (0, -1),   # left
            (0, 1),    # right
            (-1, -1),  # top-left
            (-1, 1),   # top-right
            (1, -1),   # bottom-left
            (1, 1)     # bottom-right
        ]

    # Returns true or false depending on if the move trying to be made is legal.
    def is_legal_move(self, dest_row, dest_col, board):
        # If same position, move is legal (no movement)
        if super()._is_same_position(dest_row, dest_col):
            return True

        # Check if move direction is valid
        if not self._is_valid_direction(dest_row, dest_col):
            return False

        # Check if path is clear and destination is valid
        return (self._is_path_clear(dest_row, dest_col, board) and
                self._is_valid_destination(dest_row, dest_col, board))

    # Generates all possible moves given the current board state.
    def generate_legal_moves(self, board_data, board):
        char_label = self._label.value
        board_data[self._row][self._col] = char_label

        for row_direction, col_direction in self._get_directions():
            new_row = self._row
            new_col = self._col

            while True:
                new_row += row_direction
                new_col += col_direction

                if not self._is_within_board(new_row, new_col):
                    break

                square_type = board.get_square_info(new_row, new_col)
                if square_type != BoardInfo.EMPTY:
                    if square_type != self._color:
                        board_data[new_row][new_col] = char_label
                    break

                board_data[new_row][new_col] = char_label

        return board_data
