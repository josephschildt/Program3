from chess_piece import ChessPiece
from board import Board
from chess_utils import BoardInfo
from chess_utils import PieceInfo


class Knight(ChessPiece):

    def _get_knight_moves(self):
        """Returns all possible knight move patterns."""
        return [
            (-2, -1), (-2, 1),  # Move two rows up, one column left/right
            (-1, -2), (-1, 2),  # Move one row up, two columns left/right
            (1, -2), (1, 2),    # Move one row down, two columns left/right
            (2, -1), (2, 1)     # Move two rows down, one column left/right
        ]

    def _is_valid_knight_pattern(self, row_diff, col_diff):
        """Checks if the move follows valid knight movement pattern."""
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

    def _is_valid_destination(self, dest_row, dest_col, board):
        """Checks if the destination square is valid (not off board or same color)."""
        square_type = board.get_square_info(dest_row, dest_col)
        return square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD

    def is_legal_move(self, dest_row, dest_col, board):
        """Determines if a move to the destination square is legal."""
        row_diff = abs(self._row - dest_row)
        col_diff = abs(self._col - dest_col)

        return (self._is_valid_knight_pattern(row_diff, col_diff) and
                self._is_valid_destination(dest_row, dest_col, board))

    def _calculate_new_position(self, direction):
        """Calculates new position based on movement direction."""
        row_direction, col_direction = direction
        return (self._row + row_direction, self._col + col_direction)

    def generate_legal_moves(self, board_data, board):
        """Generates all legal moves for the knight on the current board."""
        # Mark current position
        board_data[self._row][self._col] = self._label.value

        # Check all possible knight moves
        for direction in self._get_knight_moves():
            new_row, new_col = self._calculate_new_position(direction)

            if (super()._is_within_board(new_row, new_col) and
                    self._is_valid_destination(new_row, new_col, board)):
                board_data[new_row][new_col] = self._label.value

        return board_data


class Rook(ChessPiece):

    def _is_same_position(self, dest_row, dest_col):
        """Check if the destination is the same as current position."""
        return dest_row == self._row and dest_col == self._col

    def _is_straight_line_move(self, row_diff, col_diff):
        """Check if the move is horizontal or vertical."""
        return (row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0)

    def _get_direction(self, dest_pos, current_pos):
        """Calculate the direction of movement (+1, 0, or -1)."""
        if dest_pos == current_pos:
            return 0
        return 1 if dest_pos > current_pos else -1

    def _is_valid_destination(self, square_type):
        """Check if the destination square is valid to move to."""
        return square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD

    def _is_path_clear(self, dest_row, dest_col, board):
        """Check if there are any pieces blocking the path to destination."""
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

    def is_legal_move(self, dest_row, dest_col, board):
        # Check if staying in place
        if self._is_same_position(dest_row, dest_col):
            return True

        row_diff = abs(self._row - dest_row)
        col_diff = abs(self._col - dest_col)

        # Check if move is horizontal or vertical
        if not self._is_straight_line_move(row_diff, col_diff):
            return False

        # Check for obstacles and valid destination
        return (self._is_path_clear(dest_row, dest_col, board) and
                self._is_valid_destination(board.get_square_info(dest_row, dest_col)))

    def _get_moves_in_direction(self, row_direction, col_direction, board_data, board):
        """Generate legal moves in a specific direction."""
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

    def generate_legal_moves(self, board_data, board):
        # Mark current position
        board_data[self._row][self._col] = self._label.value

        # Define directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Generate moves for each direction
        for row_direction, col_direction in directions:
            board_data = self._get_moves_in_direction(row_direction, col_direction,
                                                      board_data, board)

        return board_data


class WhitePawn(ChessPiece):
    def _is_within_bounds(self, row, col):
        return 0 <= row < 9 and 0 <= col < 8

    def _is_empty_square(self, row, col, board):
        return board._board_info[row][col] is None

    def _is_capturable_piece(self, row, col, board):
        target_piece = board._board_info[row][col]
        return target_piece is not None and target_piece.get_color() == BoardInfo.BLACK

    def is_legal_move(self, dest_row, dest_col, board):
        if dest_row == self._row and dest_col == self._col:
            return True

        if not self._is_within_bounds(dest_row, dest_col):
            return False

        # Forward one square
        if dest_col == self._col and dest_row == self._row + 1:
            return self._is_empty_square(dest_row, dest_col, board)

        # Initial two square advance
        if self._row == 1 and dest_col == self._col and dest_row == self._row + 2:
            return (self._is_empty_square(self._row + 1, self._col, board) and
                    self._is_empty_square(dest_row, dest_col, board))

        # Diagonal capture
        if abs(dest_col - self._col) == 1 and dest_row == self._row + 1:
            return self._is_capturable_piece(dest_row, dest_col, board)

        return False

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

        # Initial two square advance
        if (self._row == 1 and
            self._is_within_bounds(self._row + 2, self._col) and
            self._is_empty_square(self._row + 1, self._col, board) and
                self._is_empty_square(self._row + 2, self._col, board)):
            board_data[self._row + 2][self._col] = char_label

        # Diagonal captures
        for new_col in [self._col - 1, self._col + 1]:
            new_row = self._row + 1
            if (self._is_within_bounds(new_row, new_col) and
                    self._is_capturable_piece(new_row, new_col, board)):
                board_data[new_row][new_col] = char_label

        return board_data


class Bishop(ChessPiece):

    def is_legal_move(self, dest_row, dest_col, board):
        """Check if the bishop's move to the destination square is legal."""
        if not self._is_valid_starting_position(dest_row, dest_col):
            return False

        if not self._is_valid_diagonal_move(dest_row, dest_col):
            return False

        if not self._is_valid_destination(dest_row, dest_col, board):
            return False

        return self._is_path_clear(dest_row, dest_col, board)

    def _is_valid_starting_position(self, dest_row, dest_col):
        """Check if the move isn't to the same square."""
        return not (dest_row == self._row and dest_col == self._col)

    def _is_valid_diagonal_move(self, dest_row, dest_col):
        """Check if the move is diagonal."""
        row_diff = abs(self._row - dest_row)
        col_diff = abs(self._col - dest_col)
        return row_diff == col_diff

    def _is_valid_destination(self, dest_row, dest_col, board):
        """Check if the destination square is valid."""
        square_type = board.get_square_info(dest_row, dest_col)
        return (square_type != self._color and
                square_type != BoardInfo.OFF_THE_BOARD)

    def _is_path_clear(self, dest_row, dest_col, board):
        """Check if the diagonal path to destination is clear of pieces."""
        row_step = 1 if dest_row > self._row else -1
        col_step = 1 if dest_col > self._col else -1

        curr_row = self._row + row_step
        curr_col = self._col + col_step

        while (curr_row != dest_row) and (curr_col != dest_col):
            if board.get_square_info(curr_row, curr_col) != BoardInfo.EMPTY:
                return False
            curr_row += row_step
            curr_col += col_step

        return True

    def generate_legal_moves(self, board_data, board):
        """Generate all legal moves for the bishop."""
        char_label = self._label.value
        board_data[self._row][self._col] = char_label

        directions = [
            (-1, -1),  # top-left
            (-1, 1),   # top-right
            (1, -1),   # bottom-left
            (1, 1)     # bottom-right
        ]

        for direction in directions:
            self._mark_moves_in_direction(board_data, board, direction)

        return board_data

    def _mark_moves_in_direction(self, board_data, board, direction):
        """Mark all legal moves in a given direction."""
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

    # Allows for piece to stay in the same position.
    def _is_same_position(self, dest_row, dest_col):
        return dest_row == self._row and dest_col == self._col

    # Checks if the move is vertical, horizontal, or diagonal
    def _is_valid_direction(self, dest_row, dest_col):
        is_straight = self._row == dest_row or self._col == dest_col
        is_diagonal = abs(self._row - dest_row) == abs(self._col - dest_col)
        return is_straight or is_diagonal

    def _get_direction_steps(self, dest_row, dest_col):
        """Calculate the step direction for row and column."""
        row_step = 0 if self._row == dest_row else (
            1 if dest_row > self._row else -1)
        col_step = 0 if self._col == dest_col else (
            1 if dest_col > self._col else -1)
        return row_step, col_step

    # checks to see if there is a clear path, and if not will return false.
    def _is_path_clear(self, dest_row, dest_col, board):
        row_step, col_step = self._get_direction_steps(dest_row, dest_col)
        current_row, current_col = self._row + row_step, self._col + col_step

        while current_row != dest_row or current_col != dest_col:
            if board._board_info[current_row][current_col] is not None:
                return False
            current_row += row_step
            current_col += col_step
        return True

    def _is_valid_destination(self, dest_row, dest_col, board):
        """Check if destination square is empty or contains an opponent's piece."""
        destination_piece = board._board_info[dest_row][dest_col]
        return destination_piece is None or destination_piece.get_color() != self.get_color()

    def _get_directions(self):
        """Return all possible directions for queen movement."""
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

    def is_legal_move(self, dest_row, dest_col, board):
        # If same position, move is legal (no movement)
        if self._is_same_position(dest_row, dest_col):
            return True

        # Check if move direction is valid
        if not self._is_valid_direction(dest_row, dest_col):
            return False

        # Check if path is clear and destination is valid
        return (self._is_path_clear(dest_row, dest_col, board) and
                self._is_valid_destination(dest_row, dest_col, board))

    def generate_legal_moves(self, board_data, board):
        char_label = self._label.value
        board_data[self._row][self._col] = char_label

        for row_direction, col_direction in self._get_directions():
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
                        board_data[new_row][new_col] = char_label
                    break

                board_data[new_row][new_col] = char_label

        return board_data
