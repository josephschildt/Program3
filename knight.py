
from chess_piece import ChessPiece
from board import Board
from chess_utils import BoardInfo
from chess_utils import PieceInfo


class Knight(ChessPiece):

  def __init__(self, row_num, col_num, color, label):
    # ChessPiece.__init__(self, row_num, col_num, BoardInfo.BLACK, PieceInfo.BLACK)
    ChessPiece.__init__(self, row_num, col_num, color, label)
    self._color = color
    self._label = label
    


  def is_legal_move(self, dest_row, dest_col, board):
    row_diff = abs(self._row - dest_row)
    col_diff = abs(self._col - dest_col)
    square_type = board.get_square_info(dest_row, dest_col)
    
    is_legal = ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)) and square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD

    return is_legal

 
  def generate_legal_moves(self, board_data, board):
    char_label = self._label.value
    board_data[self._row][self._col] = char_label

    directions = [
      (-2, -1), (-2, 1),  # Move two rows up, one column left/right
      (-1, -2), (-1, 2),  # Move one row up, two columns left/right
      (1, -2), (1, 2),    # Move one row down, two columns left/right
      (2, -1), (2, 1)     # Move two rows down, one column left/right
      ]

    for row_direction, col_direction in directions:
            new_row = self._row + row_direction
            new_col = self._col + col_direction

            # Check if the move is on the board
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                square_type = board.get_square_info(new_row, new_col)

                # Add as a legal move if it's an empty square or occupied by an enemy
                if square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD:
                    board_data[new_row][new_col] = char_label

    return board_data
