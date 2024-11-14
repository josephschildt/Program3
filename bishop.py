from chess_piece import ChessPiece
from board import Board
from chess_utils import BoardInfo
from chess_utils import PieceInfo

class Bishop(ChessPiece):
  
  def __init__(self, row_num, col_num, color, label):
      ChessPiece.__init__(self, row_num, col_num, BoardInfo.BLACK, PieceInfo.BLACK)
      self._color = color
      self._label = label

  def is_legal_move(self, dest_row, dest_col, board):
      row_diff = abs(self._row - dest_row)
      col_diff = abs(self._col - dest_col)
      square_type = board.get_square_info(dest_row, dest_col)

    #   if dest_row == self._row and dest_col == self._col:
    #         return True

    #     # Ensure move is diagonal
    #   if abs(self._row - dest_row) != abs(self._col - dest_col):
    #         return False


    #   # make sure the move is diagonal
    #   is_legal = (row_diff == col_diff) and square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD
    #   return is_legal
      if dest_row == self._row and dest_col == self._col:
        return False

    # Check if the move is diagonal (row difference == column difference)
      if row_diff != col_diff:
        return False

    # Check if the destination is off the board or occupied by a piece of the same color
      if square_type == self._color or square_type == BoardInfo.OFF_THE_BOARD:
        return False

    # Check if there are any pieces blocking the path for diagonal movement
      row_step = 1 if dest_row > self._row else -1
      col_step = 1 if dest_col > self._col else -1

    # Traverse along the diagonal and check for any pieces in the way
      curr_row, curr_col = self._row + row_step, self._col + col_step
      while (curr_row != dest_row) and (curr_col != dest_col):
        if board.get_square_info(curr_row, curr_col) != BoardInfo.EMPTY:
            return False  # Path is blocked by another piece
        curr_row += row_step
        curr_col += col_step

      return True  # The move is legal
  

# def is_legal_move(self, dest_row, dest_col, board):
#         """Check if the bishop move to dest_row, dest_col is legal, including staying in place."""
#         # Allow bishop to stay in place
#         if dest_row == self._row and dest_col == self._col:
#             return True

#         # Ensure move is diagonal
#         if abs(self._row - dest_row) != abs(self._col - dest_col):
#             return False

#         # Check for obstacles in the path
#         row_step = 1 if dest_row > self._row else -1
#         col_step = 1 if dest_col > self._col else -1

#         current_row, current_col = self._row + row_step, self._col + col_step
#         while current_row != dest_row or current_col != dest_col:
#             if board._board_info[current_row][current_col] is not None:
#                 return False
#             current_row += row_step
#             current_col += col_step

#         # Check if destination is empty or has an opponent piece
#         destination_piece = board._board_info[dest_row][dest_col]
#         return destination_piece is None or destination_piece.get_color() != self.get_color()


  def generate_legal_moves(self, board_data, board):
        char_label = self._label.value
        board_data[self._row][self._col] = char_label

     # Diagonal directions
        directions = [
        (-1, -1),  # top-left
        (-1, 1),   # top-right
        (1, -1),   # bottom-left
        (1, 1)     # bottom-right
        ]

        for row_direction, col_direction in directions:
            new_row = self._row
            new_col = self._col

        # Keep going in this direction until blocked
            while True:
                new_row += row_direction
                new_col += col_direction

                if new_row < 0 or new_row >= 8 or new_col < 0 or new_col >= 8:
                    break  # Stop if it's off the board
            
                square_type = board.get_square_info(new_row, new_col)

                if square_type != BoardInfo.EMPTY:
                    if square_type != self._color:  # If it's an enemy piece, it's a legal move
                        board_data[new_row][new_col] = char_label  # Mark the legal move
                    break  # Stop if we hit any piece (friend or enemy)
            

                board_data[new_row][new_col] = char_label  # Mark the empty square as a legal move

        return board_data
      
    
