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