
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
    return move


def makeMove(move, board):
    seeds = board[move]
    board[move] = 0
    size = len(board)
    next = (move + 1) % size
    while seeds > 0:
        board[next] += 1
        next = (next + 1) % size
        seeds -= 1
    return board


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
    return p1Score > p0Score


def main():
    board = [3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0]

    player0Pits = [0, 1, 2, 3, 4, 5]
    player0Goal = 6
    player1Pits = [7, 8, 9, 10, 11, 12]
    player1Goal = 13

    playerOrder = [
        [player0Pits, getHumanPlayerMove],
        [player1Pits, getHumanPlayerMove]
    ]

    if getWhoMovesFirst():
        playerOrder.reverse()

    player1Winner = False
    while True:
        for playerPits, moveFunc in playerOrder:
            printBoard(board)

            move = moveFunc(playerPits, board)
            board = makeMove(move, board)

            player0Score = calcScore(player0Goal, player0Pits, board)
            player1Score = calcScore(player1Goal, player1Pits, board)
            printScore(player0Score, player1Score)

            if checkEmptyPits(playerPits, board):
                player1Winner = determineWinner(player0Score, player1Score)
                break


    if player1Winner:
        print "You won!"
    else:
        print "You lost!"


if __name__ == '__main__':
    main()