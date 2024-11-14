from chess_piece import ChessPiece
from board import Board
from chess_utils import BoardInfo
from chess_utils import PieceInfo

class WhitePawn(ChessPiece):
    
    def __init__(self, row_num, col_num, color, label):
      ChessPiece.__init__(self, row_num, col_num, BoardInfo.BLACK, PieceInfo.BLACK)
      self._color = color
      self._label = label
      self._has_moved = False

    def is_legal_move(self, dest_row, dest_col, board):
      row_diff = abs(self._row - dest_row)
      col_diff = abs(self._col - dest_col)
      square_type = board.get_square_info(dest_row, dest_col)
    
      #need logic here to check if it is the first move by that pawn, allowing them to move 2 spaces instead of 1 forward
      # is_legal = ((row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0)) and square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD
      if self._has_moved:
         return row_diff == -1 or col_diff == 0 and square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD
      else: 
         return (row_diff == -1 or row_diff == -2) and col_diff == 0 and square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD
  
    def generate_legal_moves(self, board_data, board):
       
      char_label = self._label.value
      board_data[self._row][self._col] = char_label

      #up up2 diag-left diag-right
      directions = [
        (-1, 0),
        (-2, 0) if not self._has_moved else None,
        (-1, -1),
        (-1, 1)
      ]

      for row_direction, col_direction in directions:
        if row_direction == None:
           continue
        
        new_row = self._row + row_direction
        new_col = self._col + col_direction

      
            
            # Check if we are off the board
        if new_row < 0 or new_row >= 8 or new_col < 0 or new_col >= 8:
                continue  # Stop if it's off the board
            
        square_type = board.get_square_info(new_row, new_col)

            # If we hit any piece (friend or enemy)
        if square_type != BoardInfo.EMPTY:
                if square_type != self._color:  # If it's an enemy piece, it's a legal move
                    board_data[new_row][new_col] = char_label  # Mark the legal move
                continue  # Stop if we hit any piece (friend or enemy)
        else:
                board_data[new_row][new_col] = char_label  # Mark the empty square as a legal move

      self._has_moved = True
      return board_data
