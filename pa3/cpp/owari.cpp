#include <iostream>
#include <stdio.h>
#include <time.h>
#include <cstring>
#include <ctime>

using namespace std;

#define PLAYER_1 0
#define PLAYER_2 1

#define STATE_P1_WIN 0
#define STATE_P2_WIN 1
#define STATE_TIED 2
#define STATE_CONTINUE 3

#define BOARD_SIZE 14

#define P1_MIN_PIT 0
#define P1_MAX_PIT 5
#define P1_GOAL_PIT 6

#define P2_MIN_PIT 7
#define P2_MAX_PIT 12
#define P2_GOAL_PIT 13

#define ALPHA_MIN -256
#define BETA_MAX 256

#define COST_WIN -128
#define COST_LOST 128
#define COST_TIE 0

#define MSG_WELCOME "Welcome to Owari!"
#define MSG_WIN "Player 1 Won!"
#define MSG_LOST "Player 1 Lost!"
#define MSG_TIED "Player 1 Lost!"

class OwariAlphaBeta {
public:
    int findMove(int board[], int depth);
    int maxValue(int board[], int alpha, int beta, int cdepth, int mdepth);
    int minValue(int board[], int alpha, int beta, int cdepth, int mdepth);
};

int checkForWinner(int board[]) {
    int p1score = 0;
    int p2score = 0;
    int p1seeds = board[0] + board[1] + board[2] + board[3] + board[4] + board[5];
    int p2seeds = board[7] + board[8] + board[9] + board[10] + board[11] + board[12];

    if (p1seeds == 0 || p2seeds == 0) {
        p1score = p1seeds + board[P1_GOAL_PIT];
        p2score = p2seeds + board[P2_GOAL_PIT];
        if (p2score > p1score) {
            return STATE_P2_WIN;
        } else if (p1score > p2score) {
            return STATE_P1_WIN;
        } else {
            return STATE_TIED;
        }
    } else {
        return STATE_CONTINUE;
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
            ++newBoard[next];
            if (seeds == 1 && newBoard[next] == 1 && next >= P2_MIN_PIT && next <= P2_MAX_PIT) {
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
            ++newBoard[next];
            if (seeds == 1 && newBoard[next] == 1 && next >= P1_MIN_PIT && next <= P1_MIN_PIT) {
                newBoard[P1_GOAL_PIT] += newBoard[12 - next];
                newBoard[12 - next] = 0;
            }
            --seeds;
        }
        next = (next + 1) % BOARD_SIZE;
    }
    return true;
}

int OwariAlphaBeta::findMove(int board[], int depth) {
    int alpha = ALPHA_MIN;
    int beta = BETA_MAX;

    int bestValue = ALPHA_MIN;
    int bestMove = -1;

    int moveValue = ALPHA_MIN;
    int nextMove = P1_MIN_PIT;

    int newBoard[BOARD_SIZE];

    for (; nextMove < P1_GOAL_PIT; ++nextMove) {
        if (makeMoveP1(nextMove, board, newBoard)) {
            moveValue = minValue(newBoard, alpha, beta, 0, depth);
            if (moveValue > bestValue) {
                bestValue = moveValue;
                bestMove = nextMove;
            }

            if (bestValue >= beta) {
                break;
            }

            if (bestValue > alpha) {
                alpha = bestValue;
            }
        }
    }
    return bestMove;
}

int OwariAlphaBeta::maxValue(int board[], int alpha, int beta, int cdepth, int mdepth) {
    int nextMove = P1_MIN_PIT;
    int bestValue = ALPHA_MIN;
    int moveValue = 0;
    bool moveResult = false;
    int newBoard[BOARD_SIZE];
    int status = checkForWinner(board);
    int ndepth = cdepth + 1;
    if (status == STATE_P1_WIN) {
        return COST_WIN;
    } else if (status == STATE_P2_WIN) {
        return COST_LOST;
    } else if (status == STATE_TIED) {
        return COST_TIE;
    } else if (cdepth == mdepth) {
        return board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6];
    } else {
        for (; nextMove < P1_GOAL_PIT; ++nextMove) {
            if (makeMoveP1(nextMove, board, newBoard)) {
                moveValue = minValue(newBoard, alpha, beta, ndepth, mdepth);
                if (moveValue > bestValue) {
                    bestValue = moveValue;
                }

                if (bestValue >= beta) {
                    return bestValue;
                }

                if (bestValue > alpha) {
                    alpha = bestValue;
                }
            }
        }
        return bestValue;
    }
}

int OwariAlphaBeta::minValue(int board[], int alpha, int beta, int cdepth, int mdepth) {
    int nextMove = P2_MIN_PIT;
    int bestValue = BETA_MAX;
    int moveValue = 0;
    bool moveResult = false;
    int newBoard[BOARD_SIZE];
    int status = checkForWinner(board);
    int ndepth = cdepth + 1;
    if (status == STATE_P1_WIN) {
        return COST_WIN;
    } else if (status == STATE_P2_WIN) {
        return COST_LOST;
    } else if (status == STATE_TIED) {
        return COST_TIE;
    } else if (cdepth == mdepth) {
        return 0 - board[7] - board[8] - board[9] - board[10] - board[11] - board[12] - board[13];
    } else {
        for (; nextMove < P2_GOAL_PIT; ++nextMove) {
            if (makeMoveP2(nextMove, board, newBoard)) {
                moveValue = maxValue(newBoard, alpha, beta, ndepth, mdepth);
                if (moveValue < bestValue) {
                    bestValue = moveValue;
                }

                if (bestValue <= alpha) {
                    return bestValue;
                }

                if (bestValue < beta) {
                    beta = bestValue;
                }
            }
        }
        return bestValue;
    }
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
    printf("Score: %d %d\n", p2score, p1score);
}

void printStatus(int board[], int move, int turn, int moveCount) {
    printf("Waiting for player %d's move\n", turn + 1);
    printf("Move %d: Player %d selected pit %d\n", moveCount, turn + 1, move);
    cout << endl << "Current Board State:" << endl;
    printBoard(board);
    printScore(board);
}

void runOwari() {
    srand(time(NULL));

    clock_t begin;
    clock_t end;

    OwariAlphaBeta aiPlayer;
    int maxDepth = 19;

    int board[] = {3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0};
    int moveCount = 0;
    int turn = 0; //getWhoMovesFirst();
    int status = STATE_CONTINUE;

    cout << MSG_WELCOME << endl;
    printBoard(board);

    while (true) {
        int move = -1;

        if (turn == PLAYER_1) {

            begin = clock();
            move = aiPlayer.findMove(board, maxDepth);
            end = clock();
            cout << "Elapsed time: " << double(end - begin) / CLOCKS_PER_SEC << endl;
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

    if (status == STATE_P1_WIN) {
        cout << MSG_WIN << endl;
    } else if (status == STATE_P2_WIN) {
        cout << MSG_LOST << endl;
    } else {
        cout << MSG_TIED << endl;
    }
}

int main() {
    runOwari();
    return 0;
}