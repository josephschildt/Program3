from chess_piece import ChessPiece
from board import Board
from chess_utils import BoardInfo
from chess_utils import PieceInfo


class Knight(ChessPiece):
    def __init__(self, row_num, col_num, color, label):
        super().__init__(row_num, col_num, color, label)
        self._color = color
        self._label = label

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

    def _is_within_board(self, row, col):
        """Checks if the given position is within the board boundaries."""
        return 0 <= row < 8 and 0 <= col < 8

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

            if (self._is_within_board(new_row, new_col) and
                    self._is_valid_destination(new_row, new_col, board)):
                board_data[new_row][new_col] = self._label.value

        return board_data
