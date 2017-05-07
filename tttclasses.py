from random import randrange as rand
from itertools import accumulate

def straightlines():
    rcd = [((0,0),(1,1),(2,2)),((0,2),(1,1),(2,0)),((0,0),(0,1),(0,2)),((1,0),(1,1),(1,2)),((2,0),(2,1),(2,2)),((0,0),(1,0),(2,0)),((0,1),(1,1),(2,1)),((0,2),(1,2),(2,2))]
    for i in rcd: yield i

class tttboard:
    '''Board has 5 elements:
    board = [[i for i in row] for row in board] list of all the individual spaces in the tic-tac-toe board, with 0 = empty space, 1 = O, and 2 = X
    turn = 1 or 2 depending on which one has the turn
    lastboard = copy of the last board
    lastmove = (row, col) tuple of the last placed location
    availlocs = list of (row, col) tuples for availble locations'''
    @staticmethod
    def availloc(board):    
        '''iterator through empty spaces'''
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    yield (row, col)

    def __init__(self, board = None, turn = 1):                                                                     ##initialization
        if board is None:                           
            self.board = [[0] * 3 for i in range(3)]                                                                ##by default, an empty board is set
        else:                                                   
            self.board = board                                                                                      ##if board is specified, use it
        self.turn = turn
        self.lastboard = None
        self.lastmove = None
        self.availlocs = [i for i in self.availloc(self.board)]
    def __str__(self):                                                                                              ##create a nice printable format of the current board
        s = '  0 1 2\n -------'
        for i in range(3):
            s += '\n{}|'.format(i) + '|'.join([{0:' ', 1:'O', 2:'X'}[n] for n in self.board[i]]) + '|'
            s += '\n -------'
        return s
    def disp(self):
        '''display current board'''
        print(str(self))    
    def copyboard(self): 
        '''return a copy of the board'''
        return [[loc for loc in row] for row in self.board]                                                        
    def canonicalize(self):
        '''if it's X's turn, make self into a equivalent in O's turn'''
        if self.turn == 2:
            self.board = [[{0:0, 1:2, 2:1}[loc] for loc in row] for row in self.board]
            self.turn = 1
    def setpiece(self, loc, disp = True):
        '''Proper way to edit tttboard.board to keep track of available locations, last board, last move, available locations, and to avoid unwanted behaviors'''
        try:
            loc = (int(loc[0]), int(loc[1]))                                                                        ##catch corrupted inputs
        except TypeError:
            raise IllegalMove(message = 'Invalid input parameter.')
        if loc[0] < 0 or loc[0] > 2 or loc[1] < 0 or loc[1] > 2: raise IllegalMove(message = 'This location is outside the board.')
        if len(self.availlocs) == 0: raise IllegalMove(message = 'Board is full.')
        if self.board[loc[0]][loc[1]]: raise IllegalMove(message = 'This location already contains a chess piece.')
        self.lastboard = self.copyboard()                                                                           ##copy current board config
        self.lastmove = (loc[0], loc[1])                                                                            ##copy the move
        self.board[loc[0]][loc[1]] = self.turn                                                                      ##make the move
        self.turn = 3 - self.turn                                                                                   ##revert turn
        self.availlocs = [i for i in self.availloc(self.board)]
        winner = self.checkwin()                                                                                    ##check if game ended
        if disp == True:
            self.disp()
            if winner == 1 or winner == 2: print('{} wins!'.format({1:'O', 2:'X'}[winner]))                         ##disp result if win
            elif winner == -1: print('Draw.')                                                                       ##disp result if draw
        return winner                                                                                               ##return the result of the move
    def checkwin(self):                          
        '''Check for a winner. 1=O, 2=X, -1=Draw, 0=Not finished'''
        for i, j, k in straightlines():
            if 0 != self.board[i[0]][i[1]] and self.board[i[0]][i[1]] == self.board[j[0]][j[1]] == self.board[k[0]][k[1]]:       
                return self.board[i[0]][i[1]]
        if len(self.availlocs) == 0: return -1
        return 0
  
    
class IllegalMove(Exception):
    '''Illegal operation on tic-tac-toe board.'''

    def __init__(self, expression='', message=''):
        self.expression = expression
        self.message = message
    def __str__(self): return self.message


class tttai_rand:
    '''The stupid AI that performs random moves and only fill/block when necessary.'''

    def __init__(self, board = None):
        if board is None: self.board = tttboard()                                                                   ##instead of being on the same level, AIs now work on the class
        else: self.board = board
    def ness(self):
        """return a location if needed to immediately win/prevent losing"""
        for i, j, k in straightlines():                                                                             ##check for 1-move-wins
            if self.board.board[i[0]][i[1]] == self.board.board[j[0]][j[1]] == self.board.turn and self.board.board[k[0]][k[1]] == 0: return k
            if self.board.board[i[0]][i[1]] == self.board.board[k[0]][k[1]] == self.board.turn and self.board.board[j[0]][j[1]] == 0: return j
            if self.board.board[j[0]][j[1]] == self.board.board[k[0]][k[1]] == self.board.turn and self.board.board[i[0]][i[1]] == 0: return i
        for i, j, k in straightlines():                                                                             ##check for opponent 2-in-a-rows
            if 0 != self.board.board[i[0]][i[1]] == self.board.board[j[0]][j[1]] != self.board.turn and self.board.board[k[0]][k[1]] == 0: return k
            if 0 != self.board.board[i[0]][i[1]] == self.board.board[k[0]][k[1]] != self.board.turn and self.board.board[j[0]][j[1]] == 0: return j
            if 0 != self.board.board[j[0]][j[1]] == self.board.board[k[0]][k[1]] != self.board.turn and self.board.board[i[0]][i[1]] == 0: return i
        return None
    def makeaimove(self, disp = True):
        '''Proper way to invoke AI to make move. Return 1=O, 2=X, -1=Draw, 0=Not finished'''
        loc = self.ness()
        if loc is None:
            loc = self.board.availlocs[rand(len(self.board.availlocs))]
        return self.board.setpiece(loc, disp)


class tttai_recur:
    '''The smart AI that considers all subsequent moves and plays perfectly, sans strategies.'''

    def __init__(self, board = None):
        if board is None: self.board = tttboard()
        else: self.board = board
    def consider(self, board = None):
        '''Consideration process of the AI'''
        if board is None: board = tttboard(self.board.board, self.board.turn)
        if len(board.availlocs) == 9: return (rand(3), rand(3)), None                                               ##if board is empty, put anywhere to save computation time
        if len(board.availlocs) == 0: return None, -1                                                               ##if board is full and nobody win, return draw
        for i, j, k in straightlines():                                                                             ##iterate to find 1-move-wins
            if board.board[i[0]][i[1]] == board.board[j[0]][j[1]] == board.turn and board.board[k[0]][k[1]] == 0: return k, board.turn
            if board.board[i[0]][i[1]] == board.board[k[0]][k[1]] == board.turn and board.board[j[0]][j[1]] == 0: return j, board.turn
            if board.board[j[0]][j[1]] == board.board[k[0]][k[1]] == board.turn and board.board[i[0]][i[1]] == 0: return i, board.turn
        locwinnerpair = []                                                                                          ##score each available 
        for loc in board.availlocs:                                                                                 ##iterate through available locations to determine the perfect-move result for each
            newboard = tttboard(board.copyboard(), board.turn)                                                      ##create the board after placing a piece in the location
            newboard.setpiece(loc, disp = False)
            result = self.consider(newboard)                                                                        ##recursion to consider each location
            if result[1] == board.turn: return loc, board.turn                                                      ##if the loc results in a definite win, just go to that location and win
            locwinnerpair.append((loc, result[1]))                                                                  ##(loc, winner) pair for each location
        for i in locwinnerpair:                                                                                     ##if arrived at this location, it means that no definite-win move is available
            if i[1] == -1: return i                                                                                 ##just go to the first location that would result in a draw
        return locwinnerpair[0]                                                                                     ##if all moves result in a lose? well
    def makeaimove(self, disp = True):
        loc = self.consider(self.board)
        if loc[0] is not None: return self.board.setpiece(loc[0], disp)
    

class tttai_learn(tttboard):
    '''A learning AI that creates and utilizes a database of known board evolution to weigh its choices
    Database data structure in memory
    __name__ = self.bsdb        type: <class 'dict'>        reason: O(1) time for value lookup, which is the bulk of its operations
    key = repr(board)                                       no reorientation is used cite computation costs and that there are at most 3**9 = 19683
        board = [[0=empty|1=current|2=opponent]*row]*col    board stores information for the player of current turn. conversion is needed after placing each move
    value[0] = score                                        a score between 0 and 15 expressing the desirability of the current board for the player of current turn
    value[1] = [*parent boards]                             entries of parent boards that can lead to this board
    value[2] = [*[children boards, (row, col)]]             entries of children boards and move to make to achieve it

    Database in boardscore.db read on the initialization of the class, dynamically modified while the class places movement, and stored on destructor of class
    storage format:
    repr(board)                             +   '|'
    str(score)                              +   '|'
    repr([*parent boards])                  +   '|'
    repr([*[children boards, (row, col)]])  +   '\n' '''

    def __init__(self, board = None):
        if board is None: self.board = tttboard()
        else: self.board = board
        self.bsdb = {}                                                                                              ##initialize run-time database
        with open('boardscore.db', 'r') as f:                                                                       ##read from database in boardscore.db
            for line in f:
                elements = line.rstrip('\n').split('|')
                key = elements[0]
                score = int(elements[1])
                parentboards = eval(elements[2])
                children = eval(elements[3])
                self.bsdb[key] = [score, parentboards, children]                                                    ##write to memory
    def __enter__(self):                                                                                            ##'with' method
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        with open('boardscore.db', 'w') as f:                                                                       ##save runtime database to boardscore.db
            for key in self.bsdb.keys():                                                                            ##iterate through run-time database in the dict self.bsdb
                values = self.bsdb[key]
                f.write(key + '|')                                                                                  ##key is repr(board) so it is a string
                f.write(str(values[0]) + '|')                                                                       ##write score
                f.write(repr(values[1]) + '|')                                                                      ##write parentboards
                f.write(repr(values[2]) + '\n')                                                                     ##write children

    def consider(self):
        '''The logic of learning-AI is as followed:
        1: Check any move resulting in immediate win
        2: Check if there is any 2-in-a-row for opponent to block
        3: Consult database and availlocs to determine course of action
            3.1: go to 0-score children(meaning definite lose for opponent)
            3.2: probablistically choose between children boards with score less than 15, giving unscored an intial weight of 8 (minimax)
        At the end, the program returns a score. 
        15 if next move results in a win, 0 if 2+ 2-in-a-rows by the opponent
        otherwise, find max opponent new board score, substracting from 15 to get the score'''
        move = None
        for i, j, k in straightlines():                                                                             ##check for one-move-wins
            if self.board.board[i[0]][i[1]] == self.board.board[j[0]][j[1]] == self.board.turn and self.board.board[k[0]][k[1]] == 0: move = k
            if self.board.board[i[0]][i[1]] == self.board.board[k[0]][k[1]] == self.board.turn and self.board.board[j[0]][j[1]] == 0: move = j
            if self.board.board[j[0]][j[1]] == self.board.board[k[0]][k[1]] == self.board.turn and self.board.board[i[0]][i[1]] == 0: move = i
        if move is not None: return move, 15                                                                        ##if this is a board with a definite win scenario, give a score of 15
        for i, j, k in straightlines():                                                                             ##check for opponent 2-in-a-rows
            if 0 != self.board.board[i[0]][i[1]] == self.board.board[j[0]][j[1]] != self.board.turn and self.board.board[k[0]][k[1]] == 0: move = k
            if 0 != self.board.board[i[0]][i[1]] == self.board.board[k[0]][k[1]] != self.board.turn and self.board.board[j[0]][j[1]] == 0: move = j
            if 0 != self.board.board[j[0]][j[1]] == self.board.board[k[0]][k[1]] != self.board.turn and self.board.board[i[0]][i[1]] == 0: move = i
        if move is not None:                                                                                        ##forced to block opponent 2-in-a-rows
            newboard = tttboard(self.board.copyboard(), self.board.turn)                                            ##check the score of resulting board
            newboard.setpiece(move, disp = False)
            newboard.canonicalize()
            newboardentry = self.bsdb.get(repr(newboard.board))                                                     ##if resulting board for opponent exists in database
            if newboardentry is not None: return move, 15 - newboardentry[0]                                        ##return opposite score
            return move, 5                                                                                          ##else just return low score
        numofpos = len(self.board.availlocs)                                                                        ##iterate through available positions
        availlocscore = [0] * numofpos                                                                              ##and score each
        for i in range(numofpos):
            newboard = tttboard(self.board.copyboard(), self.board.turn)                                            ##by hypothesizing resulting scenarios
            newboard.setpiece(self.board.availlocs[i], disp = False)
            newboard.canonicalize()
            newboardentry = self.bsdb.get(repr(newboard.board))
            if newboardentry is not None: availlocscore[i] = 15 - newboardentry[0]                                  ##if entry eixsts return opposite score
            else: availlocscore[i] = 8                                                                              ##else return average score
            if availlocscore[i] == 15: return self.board.availlocs[i], 15                                           ##if that position results in sure win, go for it
        weight = list(accumulate(availlocscore))                                                                    ##weigh options by their scores and randomly select
        if weight[-1] > 0:                                                                                          ##just in case all options result in sure lose
            randnum = rand(weight[-1])
            for i in range(numofpos):
                if randnum < weight[i]:
                    return self.board.availlocs[i], max(availlocscore)                                              ##returns weighed random option and score the board with optimal opponent movement
        else: return self.board.availlocs[0], 0                                                                     ##if this else is reached, sure lose, score = 0
    def makeaimove(self, disp = True):
        '''Every time the program is called to make a move, the program performs the following:
        1. log the current board as a childboard of the lastboard w/ corresponding move
        2. consider the board, output score -> bsdb and loc to make next move
        3. invoke tttboard.setpiece(loc)
        4. checkwin and return result'''
        boardcopy = tttboard(self.board.copyboard(), self.board.turn)                                               ##log the canonicalized version
        boardcopy.canonicalize()
        currentboard = repr(boardcopy.board)                                                                        ##generate key for current board's entry
        lastboard = None
        lastentry = None
        if self.board.lastboard is not None:                                                                        ##if there has been a lastboard
            if self.board.turn == 2:
                lastboardcopy = [[loc for loc in row] for row in self.board.lastboard]                              ##mini copy function
            if self.board.turn == 1:
                lastboardcopy = [[{0:0, 1:2, 2:1}[loc] for loc in row] for row in self.board.lastboard]             ##and mini canonicalize function
            lastboard = repr(lastboardcopy)                                                                         ##generate key for last board's entry
            lastentry = self.bsdb.get(lastboard)                                                                    ##pointer to last board's entry (it should exist)
            if lastentry is not None:
                if [currentboard, self.board.lastmove] not in lastentry[2]:                                         ##if the current board is not logged as the child board of last board
                    lastentry[2].append([currentboard, self.board.lastmove])
        loc, score = self.consider()
        currententry = self.bsdb.get(currentboard)                                                                  ##pointer to current board's entry or None if there's none
        if currententry is None:
            if lastboard is not None: self.bsdb[currentboard] = [score, [lastboard], []]                            ##if there's no entry of the current board, log information
            else: self.bsdb[currentboard] = [score, [], []]
            currententry = self.bsdb.get(currentboard)
        else:
            currententry[0] = score                                                                                 ##refresh score
            if lastboard is not None:
                if lastboard not in currententry[1]: currententry[1].append(lastboard)                              ##log parent board if not already in there
        if score == 15:                                                                                             ##positive reinforcement
            for parent in currententry[1]:
                parententry = self.bsdb.get(parent)
                if parententry is not None:
                    if parententry[0] != 0 and parententry[0] != 15: parententry[0] = max(parententry[0] - 2, 1)
                    for grandparent in parententry[1]:
                        grandparententry = self.bsdb.get(grandparent)
                        if grandparententry is not None:
                            if grandparententry[0] != 0 and grandparententry[0] != 15: grandparententry[0] = min(grandparententry[0] + 1, 14)
        if score == 0:                                                                                             ##negative reinforcement
            for parent in currententry[1]:
                parententry = self.bsdb.get(parent)
                if parententry is not None:
                    if parententry[0] != 0 and parententry[0] != 15: parententry[0] = min(parententry[0] + 2, 14)
                    for grandparent in parententry[1]:
                        grandparententry = self.bsdb.get(grandparent)
                        if grandparententry is not None:
                            if grandparententry[0] != 0 and grandparententry[0] != 15: grandparententry[0] = max(grandparententry[0] - 1, 1)
        return self.board.setpiece(loc, disp)
    
