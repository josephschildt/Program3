#!/bin/bash

python3 chess_move_checker.py queenInput.txt my_outfile
diff my_outfile sample_queenOutput.txt

python3 chess_move_checker.py pawnInput.txt my_outfile
diff my_outfile sample_pawnOutput.txt

python3 chess_move_checker.py rookInput.txt my_outfile
diff my_outfile sample_rookOutput.txt

python3 chess_move_checker.py bishopInput.txt my_outfile
diff my_outfile sample_bishopOutput.txt

python3 chess_move_checker.py knightInput.txt my_outfile
diff my_outfile sample_knightOutput.txt