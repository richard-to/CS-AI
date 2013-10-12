import time
import sqlite3

conn = sqlite3.connect('owari2.db')
c = conn.cursor()

memcache = {}

try:
    c.execute('''CREATE TABLE owari_cache (state text, outcome integer, PRIMARY KEY(state))''')
    conn.commit()
except:
    pass


def storeCache(cache):
    for m in cache:
        if checkCache(m[0]) == None:
            try:
                c.execute("INSERT INTO owari_cache VALUES (\'" + str(m[0]) + "'," + str(m[1]) + ")")
                memcache[str(m[0])] = m[1]
            except:
                print m
                pass
    conn.commit()


def checkCache(state):
    if str(state) in memcache:
        return memcache[str(state)]
    else:
        c.execute('SELECT * FROM owari_cache WHERE state = ?', (str(state),))
        result = c.fetchone()
        if result:
            memcache[result[0]] = result[1]
            return result[1]
        else:
            return None


class OwariMiniMax(object):
    def __init__(self):
        self.player0Pits = [0, 1, 2, 3, 4, 5]
        self.player0Goal = 6
        self.player1Pits = [7, 8, 9, 10, 11, 12]
        self.player1Goal = 13

    def decision(self, state):
        bestMove = float("-inf")
        move = 0

        nextMoves = []
        for move in xrange(6):
            newState = makeMove(move, state)
            if newState:
                nextMoves.append(newState)

        for a in nextMoves:
            predictedMove = self.minValue(a, 0)
            if predictedMove > bestMove:
                bestMove = predictedMove
                move = a

        return move

    def maxValue(self, state, d):
        if checkEmptyPits(self.player0Pits, state) or checkEmptyPits(self.player1Pits, state):
            player0Score = calcScore(self.player0Goal, self.player0Pits, state)
            player1Score = calcScore(self.player1Goal, self.player1Pits, state)
            result = determineWinner(player0Score, player1Score)
            if result == 1:
                return -1
            elif result == 0:
                return 1
            else:
                return 0
        else:
            result = checkCache(state)
            if result is not None:
                return result
            else:
                v = float("-inf")
                aBest = None

                nextMoves = []
                for move in xrange(6):
                    newState = makeMove(move, state)
                    if newState:
                        nextMoves.append(newState)

                for a in nextMoves:
                    predicted = self.minValue(a, d + 1)
                    if predicted > v:
                        v = predicted
                        aBest = [a, v, d]

                storeCache([aBest])
                return v

    def minValue(self, state, d):
        if checkEmptyPits(self.player0Pits, state) or checkEmptyPits(self.player1Pits, state):
            player0Score = calcScore(self.player0Goal, self.player0Pits, state)
            player1Score = calcScore(self.player1Goal, self.player1Pits, state)
            result = determineWinner(player0Score, player1Score)
            if result == 1:
                return -1
            elif result == 0:
                return 1
            else:
                return 0
        else:
            v = float("inf")
            nextMoves = []
            for move in xrange(7, 13):
                newState = makeMove(move, state)
                if newState:
                    nextMoves.append(newState)

            for a in nextMoves:
                predicted = self.maxValue(a, d + 1)
                if predicted < v:
                    v = predicted
            return v
    """
    def terminalTest(self, state):
        if checkEmptyPits(self.player0Pits, state) or checkEmptyPits(self.player1Pits, state):
            return True
        else:
            return False

    def utility(self, state):
        player0Score = calcScore(self.player0Goal, self.player0Pits, state)
        player1Score = calcScore(self.player1Goal, self.player1Pits, state)
        result = determineWinner(player0Score, player1Score)
        if result == 1:
            return -1
        elif result == 0:
            return 1
        else:
            return 0

    def actionsMax(self, state):
        nextMoves = []
        for move in xrange(6):
            newState = makeMove(move, state)
            if newState:
                nextMoves.append(newState)
        return nextMoves

    def actionsMin(self, state):
        nextMoves = []
        for move in xrange(7, 13):
            newState = makeMove(move, state)
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
    """

def getComputerPlayerMove(player, board):
    start = time.time()
    ai = OwariMiniMax()
    result = ai.decision(board)
    print time.time() - start
    return result


def printBoard(board):
    print ''.join(["North: ", str(list(reversed(board[7:14])))])
    print ''.join(["South: ", str(board[0:7])])


def printScore(p0Score, p1Score):
    print ' '.join(["Score:", str(p0Score), str(p1Score)])


def getWhoMovesFirst():
    decision = raw_input("Do you want to go first (Y/n)? ")
    return True if decision == 'Y' else False


def getHumanPlayerMove(validPits, board):
    validPitsAsStr = [str(pitNum) for pitNum in validPits]
    validMove = False
    move = None
    while validMove is False:
        input = (raw_input(''.join(["Pick a pit ", str(validPits), "? "]))).strip()
        if input in validPitsAsStr:
            move = int(input)
            if board[move] > 0:
                validMove = True
            else:
                print "Please select pit with seeds in it!"
        else:
            print "Please select a pit that belongs to you!"
    return makeMove(move, board)


def makeMove(move, board):
    if move < 6:
        goal = 6
        skip = 13
        min = 0
        max = 5
    else:
        goal = 13
        skip = 6
        min = 7
        max = 12

    newBoard = board[:]
    if newBoard[move] == 0:
        return None

    seeds = newBoard[move]
    newBoard[move] = 0
    size = len(newBoard)
    next = (move + 1) % size

    while seeds > 0:
        if next != 13:
            newBoard[next] += 1
            if seeds == 1 and newBoard[next] == 1 and next >= min and next <= max:
                newBoard[goal] += newBoard[12 - next]
                newBoard[12 - next] = 0
            seeds -= 1
        next = (next + 1) % size
    return newBoard


def checkEmptyPits(pPits, board):
    for pit in pPits:
        if board[pit] > 0:
            return False
    return True


def calcScore(playerGoal, playerPits, board):
    score = board[playerGoal]
    for pit in playerPits:
        score += board[pit]
    return score


def determineWinner(p0Score, p1Score):
    if p1Score > p0Score:
        return 1
    elif p0Score > p1Score:
        return 0
    else:
        return 2


def main():
    board = [3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0]
    player0Pits = [0, 1, 2, 3, 4, 5]
    player0Goal = 6
    player1Pits = [7, 8, 9, 10, 11, 12]
    player1Goal = 13

    playerOrder = [
        [player0Pits, getComputerPlayerMove],
        [player1Pits, getHumanPlayerMove]
    ]

    if getWhoMovesFirst():
        playerOrder.reverse()

    while True:
        for playerPits, moveFunc in playerOrder:
            printBoard(board)

            board = moveFunc(playerPits, board)
            player0Score = calcScore(player0Goal, player0Pits, board)
            player1Score = calcScore(player1Goal, player1Pits, board)
            printScore(player0Score, player1Score)

            if checkEmptyPits(playerPits, board):
                break

        if checkEmptyPits(playerPits, board):
            break

    status = determineWinner(player0Score, player1Score)
    if status == 1:
        print "You won!"
    elif status == 0:
        print "You lost!"
    else:
        print "You tied!"


if __name__ == '__main__':
    main()