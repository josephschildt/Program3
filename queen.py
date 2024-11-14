from chess_piece import ChessPiece
from board import Board
from chess_utils import BoardInfo
from chess_utils import PieceInfo

class Queen(ChessPiece):

  def __init__(self, row_num, col_num, color, label):
      ChessPiece.__init__(self, row_num, col_num, BoardInfo.BLACK, PieceInfo.BLACK)
      self._color = color
      self._label = label


  def is_legal_move(self, dest_row, dest_col, board):
    #   row_diff = abs(self._row - dest_row)
    #   col_diff = abs(self._col - dest_col) # maybe take out the abs since they can move backwards as well
    #   square_type = board.get_square_info(dest_row, dest_col)

    #   # moves can essentially be anywhere, straight, diag, can go back or forwards
    #   is_legal = (row_diff == col_diff) or ((row_diff > 0 and col_diff == 0) or (row_diff == 0 and col_diff > 0)) and square_type != self._color and square_type != BoardInfo.OFF_THE_BOARD
    #   return is_legal
    if dest_row == self._row and dest_col == self._col:
            return True

        # Ensure move is either straight or diagonal
    if self._row != dest_row and self._col != dest_col and abs(self._row - dest_row) != abs(self._col - dest_col):
            return False

        # Determine movement direction
    row_step = 0 if self._row == dest_row else (
            1 if dest_row > self._row else -1)
    col_step = 0 if self._col == dest_col else (
            1 if dest_col > self._col else -1)

        # Check for obstacles along the path
    current_row, current_col = self._row + row_step, self._col + col_step
    while current_row != dest_row or current_col != dest_col:
            if board._board_info[current_row][current_col] is not None:
                return False
            current_row += row_step
            current_col += col_step

        # Check if destination is empty or has an opponent piece
    destination_piece = board._board_info[dest_row][dest_col]
    return destination_piece is None or destination_piece.get_color() != self.get_color()
  

  def generate_legal_moves(self, board_data, board):
    char_label = self._label.value
    board_data[self._row][self._col] = char_label
    
    #same error as bishop its not recognizing a peice all the way down where the move should not be possible

    #up down left right
    directions = [
      (-1, 0), 
      (1, 0),
      (0, -1),
      (0, 1),
      (-1, -1),  # top-left
      (-1, 1),   # top-right
      (1, -1),   # bottom-left
      (1, 1)     # bottom-right
    ]

    for row_direction, col_direction in directions:
       new_row = self._row
       new_col = self._col

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


    
