from chess_piece import ChessPiece
from board import Board
from chess_utils import BoardInfo
from chess_utils import PieceInfo


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
