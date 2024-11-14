from chess_piece import ChessPiece
from board import Board
from chess_utils import BoardInfo, PieceInfo


class Bishop(ChessPiece):
    def __init__(self, row_num, col_num, color, label):
        ChessPiece.__init__(self, row_num, col_num,
                            BoardInfo.BLACK, PieceInfo.BLACK)
        self._color = color
        self._label = label

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

            if not self._is_within_board(new_row, new_col):
                break

            square_type = board.get_square_info(new_row, new_col)

            if square_type != BoardInfo.EMPTY:
                if square_type != self._color:
                    board_data[new_row][new_col] = self._label.value
                break

            board_data[new_row][new_col] = self._label.value

    def _is_within_board(self, row, col):
        """Check if the given position is within the board boundaries."""
        return 0 <= row < 8 and 0 <= col < 8
