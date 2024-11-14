from chess_piece import ChessPiece
from board import Board
from chess_utils import BoardInfo
from chess_utils import PieceInfo


class Queen(ChessPiece):
    def __init__(self, row_num, col_num, color, label):
        ChessPiece.__init__(self, row_num, col_num,
                            BoardInfo.BLACK, PieceInfo.BLACK)
        self._color = color
        self._label = label

    def _is_same_position(self, dest_row, dest_col):
        """Check if the destination is the same as current position."""
        return dest_row == self._row and dest_col == self._col

    def _is_valid_direction(self, dest_row, dest_col):
        """Check if move is either straight or diagonal."""
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

    def _is_path_clear(self, dest_row, dest_col, board):
        """Check if there are any pieces blocking the path."""
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

    def _is_within_board(self, row, col):
        """Check if position is within board boundaries."""
        return 0 <= row < 8 and 0 <= col < 8

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

                if not self._is_within_board(new_row, new_col):
                    break

                square_type = board.get_square_info(new_row, new_col)
                if square_type != BoardInfo.EMPTY:
                    if square_type != self._color:
                        board_data[new_row][new_col] = char_label
                    break

                board_data[new_row][new_col] = char_label

        return board_data
