#include <iostream>
#include <stdio.h>
#include <time.h>
#include <cstring>

using namespace std;

#define PLAYER_1 0
#define PLAYER_2 1

#define STATE_WIN 0
#define STATE_LOST 1
#define STATE_TIED 2
#define STATE_CONTINUE 3

#define BOARD_SIZE 14

#define P1_MIN_PIT 0
#define P1_MAX_PIT 5
#define P1_GOAL_PIT 6

#define P2_MIN_PIT 7
#define P2_MAX_PIT 12
#define P2_GOAL_PIT 13

#define MSG_WELCOME "Welcome to Owari!"
#define MSG_WIN "Player 1 Won!"
#define MSG_LOST "Player 1 Lost!"
#define MSG_TIED "Player 1 Lost!"

int checkForWinner(int board[]) {
    int p1score = 0;
    int p2score = 0;
    int p1seeds = board[0] + board[1] + board[2] + board[3] + board[4] + board[5];
    int p2seeds = board[7] + board[8] + board[9] + board[10] + board[11] + board[12];

    if (p1seeds == 0 || p2seeds == 0) {
        p1score = p1seeds + board[P1_GOAL_PIT];
        p2score = p2seeds + board[P2_GOAL_PIT];
        if (p2score > p1score) {
            return 0;
        } else if (p1score > p2score) {
            return 1;
        } else {
            return 2;
        }
    } else {
        return 3;
    }
}

bool makeMoveP2(int move, int board[], int newBoard[]) {
    if (board[move] == 0) {
        return false;
    }

    newBoard[0] = board[0];
    newBoard[1] = board[1];
    newBoard[2] = board[2];
    newBoard[3] = board[3];
    newBoard[4] = board[4];
    newBoard[5] = board[5];
    newBoard[6] = board[6];
    newBoard[7] = board[7];
    newBoard[8] = board[8];
    newBoard[9] = board[9];
    newBoard[10] = board[10];
    newBoard[11] = board[11];
    newBoard[12] = board[12];
    newBoard[13] = board[13];

    int next = (move + 1) % BOARD_SIZE;
    int seeds = newBoard[move];
    newBoard[move] = 0;

    while (seeds > 0) {
        if (next != P1_GOAL_PIT) {
            newBoard[next] += 1;
            if (seeds == 1 && newBoard[next] == 1 && next >= P2_MIN_PIT and next <= P2_MAX_PIT) {
                newBoard[P2_GOAL_PIT] += newBoard[12 - next];
                newBoard[12 - next] = 0;
            }
            --seeds;
        }
        next = (next + 1) % BOARD_SIZE;
    }
    return true;
}

bool makeMoveP1(int move, int board[], int newBoard[]) {
    if (board[move] == 0) {
        return false;
    }

    newBoard[0] = board[0];
    newBoard[1] = board[1];
    newBoard[2] = board[2];
    newBoard[3] = board[3];
    newBoard[4] = board[4];
    newBoard[5] = board[5];
    newBoard[6] = board[6];
    newBoard[7] = board[7];
    newBoard[8] = board[8];
    newBoard[9] = board[9];
    newBoard[10] = board[10];
    newBoard[11] = board[11];
    newBoard[12] = board[12];
    newBoard[13] = board[13];

    int next = (move + 1) % BOARD_SIZE;
    int seeds = newBoard[move];
    newBoard[move] = 0;

    while (seeds > 0) {
        if (next != P2_GOAL_PIT) {
            newBoard[next] += 1;
            if (seeds == 1 && newBoard[next] == 1 && next >= P1_MIN_PIT and next <= P2_MIN_PIT) {
                newBoard[P1_GOAL_PIT] += newBoard[12 - next];
                newBoard[12 - next] = 0;
            }
            --seeds;
        }
        next = (next + 1) % BOARD_SIZE;
    }
    return true;
}

int getWhoMovesFirst() {
    return rand() % 2;
}

int getHumanMove(int board[], int validPits[]) {
    bool validMove = false;
    int i = 0;
    int move = -1;
    int input = -1;
    while (validMove == false) {
        printf("Pick a pit (%d, %d, %d, %d, %d, %d)? ",
            validPits[0], validPits[1], validPits[2], validPits[3], validPits[4], validPits[5]);
        cin >> input;

        for (i = 5; i > -1; --i) {
            if (input == validPits[i] && board[input] > 0) {
                validMove = true;
                move = input;
                break;
            }
        }

        if (validMove == false) {
            cout << "Pleae select a valid pit!" << endl;
        }
    }
    return move;
}

int getHumanP1Move(int board[], int depth) {
    int validPits[] = {0, 1, 2, 3, 4, 5};
    return getHumanMove(board, validPits);
}

int getHumanP2Move(int board[], int depth) {
    int validPits[] = {12, 11, 10, 9, 8, 7};
    return getHumanMove(board, validPits);
};

void printBoard(int board[]) {
    printf("North: | %2d | %2d | %2d | %2d | %2d | %2d | %2d |    |\n",
        board[13], board[12], board[11], board[10], board[9], board[8], board[7]);

    printf("South: |    | %2d | %2d | %2d | %2d | %2d | %2d | %2d |\n",
        board[0], board[1], board[2], board[3], board[4], board[5], board[6]);
}

void printScore(int board[]) {
    int p1score = board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6];
    int p2score = board[7] + board[8] + board[9] + board[10] + board[11] + board[12] + board[13];
    printf("Score: %d %d\n", p1score, p2score);
}

void printStatus(int board[], int move, int turn, int moveCount) {
    printf("Waiting for player %d's move\n", turn + 1);
    printf("Move %d: Player %d selected pit %d\n", moveCount, turn + 1, move);
    cout << "Current Board State:" << endl;
    printBoard(board);
    printScore(board);
}

void runOwari() {
    srand(time(NULL));

    int maxDepth = 15;

    int board[] = {3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0};
    int moveCount = 0;
    int turn = getWhoMovesFirst();
    int status = STATE_CONTINUE;

    cout << MSG_WELCOME << endl;
    printBoard(board);

    while (true) {
        int move = -1;

        if (turn == PLAYER_1) {
            move = getHumanP1Move(board, maxDepth);
            makeMoveP1(move, board, board);
        } else {
            move = getHumanP2Move(board, maxDepth);
            makeMoveP2(move, board, board);
        }

        status = checkForWinner(board);

        printStatus(board, move, turn, moveCount);

        if (status == STATE_CONTINUE) {
            turn = (turn + 1) % 2;
            moveCount += 1;
        } else {
            break;
        }
    }

    if (status == STATE_WIN) {
        cout << MSG_WIN << endl;
    } else if (status == STATE_LOST) {
        cout << MSG_LOST << endl;
    } else {
        cout << MSG_TIED << endl;
    }
}

int main() {
    runOwari();
    return 0;
}