from chess_piece import ChessPiece
from board import Board
from chess_utils import BoardInfo
from chess_utils import PieceInfo

class Rook(ChessPiece):

  def __init__(self, row_num, col_num, color, label):
    ChessPiece.__init__(self, row_num, col_num, BoardInfo.BLACK, PieceInfo.BLACK)
    self._color = color
    self._label = label


  def is_legal_move(self, dest_row, dest_col, board):
    
    # if dest_row == self._row and dest_col == self._col:
    #         return True
    
    # row_diff = abs(self._row - dest_row)
    # col_diff = abs(self._col - dest_col)
    # #check the diffs
    
    # # need to make a file called my_pieces.py and put all of the stuff in there 
    # # need to make it a check so the rook can choose not to move aswell, needed for all most likely
    # square_type = board.get_square_info(dest_row, dest_col)
    
    # is_legal = ((row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0)) and square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD

    # return is_legal
      if dest_row == self._row and dest_col == self._col:
            return True  # The rook can stay in place.

      row_diff = abs(self._row - dest_row)
      col_diff = abs(self._col - dest_col)

      # Check if the move is horizontal or vertical
      if not ((row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0)):
            return False  # Rook can only move horizontally or vertically.

      # Check for obstacles in the path
      row_direction = 0 if self._row == dest_row else (1 if dest_row > self._row else -1)
      col_direction = 0 if self._col == dest_col else (1 if dest_col > self._col else -1)

      current_row = self._row + row_direction
      current_col = self._col + col_direction
      while current_row != dest_row or current_col != dest_col:
            square_type = board.get_square_info(current_row, current_col)
            if square_type != BoardInfo.EMPTY:
                return False  # Path is blocked by a piece
            current_row += row_direction
            current_col += col_direction

        # Destination square must be empty or occupied by an enemy piece
      square_type = board.get_square_info(dest_row, dest_col)

      return square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD
  

  def generate_legal_moves(self, board_data, board):
    char_label = self._label.value
    board_data[self._row][self._col] = char_label

    # up down left right
    directions = [
      (-1, 0),
      (1, 0),
      (0, -1),
      (0, 1)
    ]
    
    for row_direction, col_direction in directions:
        new_row = self._row
        new_col = self._col

        # Keep going in this direction until blocked
        while True:
            new_row += row_direction
            new_col += col_direction
            
            # Check if we are off the board
            if new_row < 0 or new_row >= 8 or new_col < 0 or new_col >= 8:
                break  # Stop if it's off the board
            
            square_type = board.get_square_info(new_row, new_col)

            # If we hit any piece (friend or enemy)
            if square_type != BoardInfo.EMPTY:
                if square_type != self._color:  # If it's an enemy piece, it's a legal move
                    board_data[new_row][new_col] = char_label  # Mark the legal move
                break  # Stop if we hit any piece (friend or enemy)
            else:
                board_data[new_row][new_col] = char_label  # Mark the empty square as a legal move

    return board_data

