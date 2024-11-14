from chess_piece import ChessPiece
from board import Board
from chess_utils import BoardInfo
from chess_utils import PieceInfo


class Rook(ChessPiece):
    def __init__(self, row_num, col_num, color, label):
        ChessPiece.__init__(self, row_num, col_num,
                            BoardInfo.BLACK, PieceInfo.BLACK)
        self._color = color
        self._label = label

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
