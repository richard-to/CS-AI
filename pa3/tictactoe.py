import sqlite3

conn = sqlite3.connect('tictactoe.db')
c = conn.cursor()

try:
    c.execute('''CREATE TABLE ttt_cache (state text, outcome integer, PRIMARY KEY(state))''')
    conn.commit()
except:
    pass


cache = []

def storeCache(cache):
    for m in cache:
        try:
            c.execute("INSERT INTO ttt_cache VALUES (\'" + str(m[0]) + "'," + str(m[1]) + ")")
        except:
            pass
    conn.commit()


def checkCache(state):
    c.execute('SELECT * FROM ttt_cache WHERE state = ?', (str(state),))
    result = c.fetchone()
    if result:
        return result[1]
    else:
        return None


def writeCacheToFile(cache):
    movesFile = 'output.txt'
    with open(movesFile, 'w') as f:
        for m in cache:
            f.write(str(m))
            f.write("\n")


class TicTacToeMiniMax(object):
    def __init__(self, min=1, max=2):
        self.min = min
        self.max = max
        self.cache = []

    def decision(self, state):
        bestMove = float("-inf")
        move = 0
        for a in self.actionsMax(state):
            result = checkCache(a)
            if result is not None:
                predictedMove = result
            else:
                predictedMove = self.minValue(a, 0)
                self.cache.append([a, predictedMove, 0])

            if predictedMove > bestMove:
                bestMove = predictedMove
                move = a

        storeCache(self.cache)

        for row in xrange(3):
            for col in xrange(3):
                if move[row][col] != state[row][col]:
                    return 3 * row + col

        return move

    def maxValue(self, state, d):
        if self.terminalTest(state):
            return self.utility(state)
        else:
            result = checkCache(state)
            if result is not None:
                return result
            else:
                v = float("-inf")
                aBest = None
                for a in self.actionsMax(state):
                    predicted = self.minValue(a, d + 1)
                    if predicted > v:
                        v = predicted
                        aBest = [a, v, d]
                self.cache.append(aBest)
                return v

    def minValue(self, state, d):
        if self.terminalTest(state):
            return self.utility(state)
        else:
            v = float("inf")
            for a in self.actionsMin(state):
                v = self.findMin(v, self.maxValue(a, d + 1))
            return v

    def terminalTest(self, state):
        result = determineWinner(self.min, state)
        if result == 0:
            result = determineWinner(self.max, state)

        if result == 0:
            return False
        else:
            return True


    def utility(self, state):
        result = determineWinner(self.min, state)
        if result == 0:
            result = determineWinner(self.max, state)

        if result == self.min:
            return -1
        elif result == self.max:
            return 1
        else:
            return 0


    def actionsMax(self, state):
        nextMoves = []
        for move in xrange(9):
            newState = makeMove(self.max, move, state)
            if newState:
                nextMoves.append(newState)
        return nextMoves


    def actionsMin(self, state):
        nextMoves = []
        for move in xrange(9):
            newState = makeMove(self.min, move, state)
            if newState:
                nextMoves.append(newState)
        return nextMoves


    def findMax(self, current, new):
        if new > current:
            return new
        else:
            return current


    def findMin(self, current, new):
        if new < current:
            return new
        else:
            return current


def getComputerPlayerMove(player, board):
    ai = TicTacToeMiniMax()
    start = time.time()
    result = ai.decision(board)
    print (time.time() - start)
    return result


def printBoard(board):
    for row in board:
        print row


def getWhoMovesFirst():
    decision = raw_input("Do you want to go first (Y/n)? ")
    return True if decision == 'Y' else False


def getHumanPlayerMove(playerSymbol, board):
    validMoveAsStr = [str(i) for i in xrange(9)]
    validMove = False
    move = None
    while validMove is False:
        input = (raw_input("Make your move: [0, 1, 2], [3, 4, 5], [6, 7, 8]: ")).strip()
        if input in validMoveAsStr:
            move = int(input)
            row = move / 3
            col = move % 3
            if board[row][col] == 0:
                validMove = True
            else:
                print "Please select square that has not been marked"
        else:
            print "Please select a move between 0 and 8!"
    return move


def makeMove(player, move, board):
    row = move / 3
    col = move % 3
    if board[row][col] == 0:
        newBoard = [r[:] for r in board]
        newBoard[row][col] = player
        return newBoard
    else:
        return None


def determineWinner(player, board):

    for r in xrange(len(board)):
        # Check horizonal winner
        if board[r][0] == board[r][1] == board[r][2] == player:
            return player

        # Check vertical winner
        if board[0][r] == board[1][r] == board[2][r] == player:
            return player

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return player

    if board[0][2] == board[1][1] == board[2][0] == player:
        return player

    # Check draw
    for row in board:
        for col in row:
            if col == 0:
                return 0
    return 3


def main():
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    player1 = 1
    player2 = 2

    playerOrder = [
        [player1, getHumanPlayerMove],
        [player2, getComputerPlayerMove]
    ]

    if getWhoMovesFirst() is False:
        playerOrder.reverse()

    status = 0
    while status == 0:
        for player, moveFunc in playerOrder:
            printBoard(board)

            move = moveFunc(player, board)
            board = makeMove(player, move, board)

            status = determineWinner(player, board)
            if status > 0:
                break

    printBoard(board)

    if status == player1:
        print "You won!"
    elif status == player2:
        print "You lost!"
    else:
        print "You tied!"


if __name__ == '__main__':
    main()