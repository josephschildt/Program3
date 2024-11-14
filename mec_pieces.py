# The file has the blackPiece and the king in it
# Mary Elaine Califf
# 10/22/2021

from chess_piece import ChessPiece
from board import Board
from chess_utils import BoardInfo
from chess_utils import PieceInfo


class BlackPiece(ChessPiece):
    """A black piece that never does anything -- we're always playing white"""

    def __init__(self, row_num, col_num):
        ChessPiece.__init__(self, row_num, col_num,
                            BoardInfo.BLACK, PieceInfo.BLACK)

    def generate_legal_moves(self, board_data, board):
        """Adds representation for the legal moves to the provided 
        board representation and returns the result"""
        board_data[self._row][self._col] = self._label.value
        return board_data


class King(ChessPiece):
    def __init__(self, row_num, col_num, color, label):
        ChessPiece.__init__(self, row_num, col_num, color, label)

    def is_legal_move(self, dest_row, dest_col, board):
        """Returns true if this piece can legally move to the specified
        location on the provide board"""
        row_diff = abs(self._row-dest_row)
        col_diff = abs(self._col-dest_col)
        square_type = board.get_square_info(dest_row, dest_col)

        is_legal = (row_diff == 1 and col_diff < 2 or row_diff < 2 and col_diff ==
                    1) and square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD
        return is_legal

    def generate_legal_moves(self, board_data, board):
        """Adds representation for the legal moves to the provided 
        board representation and returns the result"""
        char_label = self._label.value
        board_data[self._row][self._col] = char_label
        for row in range(self._row-1, self._row+2):
            for col in range(self._col-1, self._col+2):
                square_type = board.get_square_info(row, col)
                if square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD:
                    board_data[row][col] = char_label
        return board_data
