import time
import random


def createBoard():
    board = [3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0]
    return board[:]


def getWhoMovesFirst():
    return random.randint(0, 1)


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


class OwariAlphaBeta(object):
    def findMove(self, board, depth):
        bestValue = -1000
        bestMove = None
        bestBoard = None

        alpha = -1000
        beta = 1000

        for nextMove in xrange(6):
            newBoard = makeMoveP1(nextMove, board)
            if newBoard:
                moveValue = self.minValue(newBoard, alpha, beta, 0, depth)
                if moveValue > bestValue:
                    bestValue = moveValue
                    bestMove = nextMove
                    bestBoard = newBoard
        return bestMove

    def maxValue(self, board, alpha, beta, cDepth, mDepth):
        status = checkForWinner(board)
        if status == 0:
            return 100
        elif status == 1:
            return -100
        elif status == 2:
            return 0
        elif cDepth == mDepth:
            return ((board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6]) -
                (board[7] + board[8] + board[9] + board[10] + board[11] + board[12] + board[13]))
        else:
            bestValue = -1000
            moveValue = 0
            for i in xrange(6):
                newBoard = makeMoveP1(i, board)
                if newBoard is not None:
                    moveValue = self.minValue(newBoard, alpha, beta, cDepth + 1, mDepth)
                    if moveValue > bestValue:
                        bestValue = moveValue

                    if bestValue >= beta:
                        return bestValue

                    if bestValue > alpha:
                        alpha = bestValue
            return bestValue

    def minValue(self, board, alpha, beta, cDepth, mDepth):
        status = checkForWinner(board)
        if status == 0:
            return 100
        elif status == 1:
            return -100
        elif status == 2:
            return 0
        elif cDepth == mDepth:
            return ((board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6]) -
                (board[7] + board[8] + board[9] + board[10] + board[11] + board[12] + board[13]))
        else:
            bestValue = 1000
            moveValue = 0
            for i in xrange(7, 13):
                newBoard = makeMoveP2(i, board)
                if newBoard is not None:
                    moveValue = self.maxValue(newBoard, alpha, beta, cDepth + 1, mDepth)
                    if moveValue < bestValue:
                        bestValue = moveValue

                    if bestValue <= alpha:
                        return bestValue

                    if bestValue < beta:
                        beta = bestValue
            return bestValue


def getComputerP1Move(board, depth):
    ai = OwariAlphaBeta()
    move = ai.findMove(board, depth)
    return move


def getComputerP2Move(board, depth):
    fBoard = board[7:14] + board[0:7]
    move = getComputerP1Move(fBoard, depth)
    fMove = move + 7
    return fMove


def printStatus(board, move, turn, moveCount):
    print "\nWaiting for player {}'s move".format(str(turn + 1))
    print "Move {}: Player {} selected pit {}".format(str(moveCount), str(turn + 1), str(move))
    print "Current Board State:"
    printBoard(board)
    printScore(board)


def printBoard(board):
    print ''.join(["North: ", str(list(reversed(board[7:14])))])
    print ''.join(["South: ", str(board[0:7])])


def printScore(board):
    p1Score = board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6]
    p2Score = board[7] + board[8] + board[9] + board[10] + board[11] + board[12] + board[13]
    print "Score: {} {}".format(str(p1Score), str(p2Score))



def simulateOwari():
    MAX_DEPTH = 10

    PLAYER_1 = 0
    PLAYER_2 = 1

    STATE_WIN = 0
    STATE_LOST = 1
    STATE_TIED = 2
    STATE_CONTINUE = 3

    MSG_WELCOME = "\nWelcome to Owari!"
    MSG_WIN = "\nPlayer 1 Won!"
    MSG_LOST = "\nPlayer 1 Lost!"
    MSG_TIED = "\nPlayer 1 Lost!"

    board = createBoard()

    players = [
        [makeMoveP1, getComputerP1Move],
        [makeMoveP2, getComputerP2Move]
    ]

    moveCount = 0
    status = STATE_CONTINUE
    turn = getWhoMovesFirst()

    print MSG_WELCOME
    printBoard(board)

    while True:
        makeMove, findMove = players[turn]
        move = findMove(board, MAX_DEPTH)
        board = makeMove(move, board)
        status =checkForWinner(board)

        printStatus(board, move, turn, moveCount)

        if status == STATE_CONTINUE:
            turn = (turn + 1) % 2
            moveCount += 1
        else:
            break

    if status == STATE_WIN:
        print MSG_WIN
    elif status == STATE_LOST:
        print MSG_LOST
    else:
        print MSG_TIED


if __name__ == '__main__':
    simulateOwari()