
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
    board[row][col] = player
    return board


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
        [player2, getHumanPlayerMove]
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