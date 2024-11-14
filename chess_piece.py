from chess_utils import PieceInfo
from chess_utils import BoardInfo


class ChessPiece:

    def __init__(self, row, col, color, label):
        self._row = row
        self._col = col
        self._label = label
        self._color = color

    def move(self, new_row, new_col):
        self._row = new_row
        self._col = new_col

    def get_color(self):
        return self._color

    def get_label(self):
        return self._label

    def is_legal_move(self, dest_row, dest_col, board):
        False

    def generate_legal_moves(self, board_data, board):
        return []

    def _is_within_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    # Allows for piece to stay in the same position.
    def _is_same_position(self, dest_row, dest_col):
        return dest_row == self._row and dest_col == self._col
