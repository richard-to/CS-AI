import time
import MySQLdb as mdb

from warnings import filterwarnings

import config

filterwarnings('ignore', category = mdb.Warning)

conn = mdb.connect(*config.db)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS owari_cache (id bigint unsigned not null primary key auto_increment, state char(60), outcome tinyint, index(state))''')
conn.commit()

memcache = {}

recordsCommitLimit = 5000
recordsInserted = 0

def storeCache(state, score):
    global memcache
    global c
    global conn
    global recordsInserted
    global recordsCommitLimit

    if checkCache(state) is None:
        try:
            c.execute("INSERT INTO owari_cache(state,outcome) VALUES (\'" + str(state) + "'," + str(score) + ")")
            memcache[str(state)] = score
            recordsInserted += 1
            if recordsInserted >= recordsCommitLimit:
                conn.commit()
                recordsInserted = 0
                memcache = {}
        except:
            pass


def checkCache(state):
    global memcache
    if str(state) in memcache:
        return memcache[str(state)]
    else:
        c.execute("""SELECT state, outcome FROM owari_cache where WHERE state = %s""", (str(state),))
        r = c.fetchone()
        if r is not None:
            return r[1]
        else:
            return None


class OwariAlphaBeta(object):
    def decision(self, board):
        bestMove = -1000
        bestBoard = None
        move = 0
        alpha = -1000
        beta = 1000
        for nextMove in xrange(6):
            newBoard = makeMoveP1(nextMove, board)
            if newBoard:
                predictedMove = self.minValue(newBoard, alpha, beta, 0, 10)
                if predictedMove > bestMove:
                    bestMove = predictedMove
                    move = nextMove
                    bestBoard = newBoard

            break
        return bestBoard

    def maxValue(self, board, alpha, beta, currentDepth, maxDepth=None):
        status = checkForWinner(board)
        if status == 0:
            return -1
        elif status == 1:
            return 1
        elif status == 2:
            return 0
        else:
            cachedMoveValue = checkCache(board)
            if cachedMoveValue is not None:
                return cachedMoveValue
            else:
                bestMoveValue = -1000
                moveValue = 0
                bestCache = []
                for i in xrange(6):
                    newBoard = makeMoveP1(i, board)
                    if newBoard is not None:
                        moveValue = self.minValue(newBoard, alpha, beta, currentDepth + 1, maxDepth)
                        if moveValue > bestMoveValue:
                            bestMoveValue = moveValue
                            bestCache = [newBoard, bestMoveValue]

                        if bestMoveValue >= beta:
                            storeCache(bestCache[0], bestCache[1])
                            return bestMoveValue

                        if bestMoveValue > alpha:
                            alpha = bestMoveValue

                storeCache(bestCache[0], bestCache[1])
                return bestMoveValue

    def minValue(self, board, alpha, beta, currentDepth, maxDepth=None):
        status = checkForWinner(board)
        if status == 0:
            return -1
        elif status == 1:
            return 1
        elif status == 2:
            return 0
        else:
            bestMoveValue = 1000
            moveValue = 0
            for i in xrange(7, 13):
                newBoard = makeMoveP2(i, board)
                if newBoard is not None:
                    moveValue = self.maxValue(newBoard, alpha, beta, currentDepth + 1, maxDepth)
                    if moveValue < bestMoveValue:
                        bestMoveValue = moveValue

                    if bestMoveValue <= alpha:
                        return bestMoveValue

                    if bestMoveValue < beta:
                        beta = bestMoveValue
            return bestMoveValue


def getComputerPlayerMove(player, board):
    start = time.time()
    ai = OwariAlphaBeta()
    result = ai.decision(board)
    print time.time() - start
    return result


def makeMoveP2(move, board):
    if board[move] == 0:
        return None

    newBoard = board[:]
    next = (move + 1) % 14
    seeds = newBoard[move]
    newBoard[move] = 0

    while seeds > 0:
        if next != 6:
            newBoard[next] += 1;
            if seeds == 1 and newBoard[next] == 1 and next >= 7 and next <= 12:
                newBoard[13] += newBoard[12 - next]
                newBoard[12 - next] = 0
            seeds -= 1
        next = (next + 1) % 14
    return newBoard


def makeMoveP1(move, board):
    if board[move] == 0:
        return None

    newBoard = board[:]
    next = (move + 1) % 14
    seeds = newBoard[move]
    newBoard[move] = 0

    while seeds > 0:
        if next != 13:
            newBoard[next] += 1;
            if seeds == 1 and newBoard[next] == 1 and next >= 0 and next <= 5:
                newBoard[6] += newBoard[12 - next]
                newBoard[12 - next] = 0
            seeds -= 1
        next = (next + 1) % 14
    return newBoard


def calcScoreDiff(board):
    p1Score = board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6]
    p2Score = board[7] + board[8] + board[9] + board[10] + board[11] + board[12] + board[13]
    return p2Score - p1Score


def checkForWinner(board):
    p1SeedSum = board[0] + board[1] + board[2] + board[3] + board[4] + board[5]
    p2SeedSum = board[7] + board[8] + board[9] + board[10] + board[11] + board[12]
    if p1SeedSum == 0 or p2SeedSum == 0:
        p1Score = p1SeedSum + board[6]
        p2Score = p2SeedSum + board[13]
        if p1Score < p2Score:
            return 0
        elif p1Score > p2Score:
            return 1
        else:
            return 2

    else:
        return 3


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
