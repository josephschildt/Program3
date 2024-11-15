# Joseph Schildt and Daulton Widlacki, Program 3, IT 327 001
# The base class for chess pieces. 
# Including methods for moving the piece, checking its legality, ensuring moves are within 
# the board boundaries, and generating legal moves.

from chess_utils import PieceInfo
from chess_utils import BoardInfo


class ChessPiece:

    # Initializes the ChessPiece
    def __init__(self, row, col, color, label):
        self._row = row
        self._col = col
        self._label = label
        self._color = color

    # Moves the piece to a new position
    def move(self, new_row, new_col):
        self._row = new_row
        self._col = new_col

    # Returns the color of the piece
    def get_color(self):
        return self._color


    # Returns the label of the piece
    def get_label(self):
        return self._label


    # Determines if the move to the destination is legal
    def is_legal_move(self, dest_row, dest_col, board):
        False


    # Generates a list of legal moves of the piece
    def generate_legal_moves(self, board_data, board):
        return []


    # Ensures the piece is in the board's boundaries
    def _is_within_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8


    # Allows for piece to stay in the same position.
    def _is_same_position(self, dest_row, dest_col):
        return dest_row == self._row and dest_col == self._col
