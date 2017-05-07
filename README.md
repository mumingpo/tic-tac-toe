# tic-tac-toe
Defines the mechanism of the game tic-tac-toe and creates 3 AIs of different logic.
dependencies: random, accumulate

class 'tttboard' creates a tic-tac-toe board.
  .turn: 1 for 'O', and 2 for 'X', default to 0
  .board [[loc for loc in row] for row in board] representation for the current tic-tac-toe board, with 0=blank space, 1='O', 2='X'
  .availlocs[(row, col)*] representation of the available locations (blank spaces) for the current board
  .lastboard = copy of previous board
  .lastmove (row, col) location of previous move
  
  .__str__() string representation of current board
  .disp() prints current board
  .copyboard() returns a copy of current board
  .setpiece((row, col), disp = True) sets a piece @ loc, prints board and winner if set true, and returns checkwin()
  .checkwin() iterates through lines to check for a winner, -1=Draw, 0=Not Finished, 1='O', 2='X'
 
class 'tttai_rand' AI that sets pieces randomly, except when completing a 3-in-a-row/blocking opponent 3-in-a-rows
  .__init__(board:tttboard = None) uses the tttboard if specified and creates a new one if not
  .ness() returns a location in the priority of winning-in-one-move>blocking opponent 2-in-a-rows
  .makeaimove(disp=True) invoke to board.setpiece(loc) if specified by .ness otherwise board.setpiece(board.availlocs[random])
  
class 'tttai_recur' AI that sets pieces evaluating each position recursively, sans the random first move if moving first
  .__init__(board:tttboard = None) uses the tttboard if specified and creates a new one if not
  .consider(board=None) evaluates the current board based on recursion evaluation of the worst subboard after placing 1 piece in each available location, returns (location, winner) tuple
  .makeaimove(disp=True) invoke to board.setpiece(loc) as specified by .consider()
  
class 'tttai_learn' AI that dynamically score each board with previous results and probabilistically go to its subboards based on their score
  .__init__(board:tttboard = None) uses the tttboard if specified and creates a new one if not, also initiates runtime database and read from existing .db file
  .__enter__() facilitates 'with' method
  .__exit__() saves runtime database to .db file at the end of 'with' method
  .consider() evaluate the current board and returns (recommended move, score) tuple, detailed description alongside code
  .makeaimove(disp=True) invokes board.setpiece(loc) as specified by .consider(), creates entry of currentboard in the database and set associations, and modify scores of existing entries if outcome is obvious
