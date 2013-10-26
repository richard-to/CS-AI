#include <iostream>
#include <stdio.h>
#include <time.h>
#include <cstring>
#include <ctime>

using namespace std;

#define PLAYER_1 0
#define PLAYER_2 1

#define INVALID_MOVE 16

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

#define ALPHA_MIN 0
#define BETA_MAX 256

#define COST_P1_WIN 32
#define COST_P2_WIN 128
#define COST_TIE 64

#define MSG_WELCOME "Welcome to Owari!"
#define MSG_WIN "Player 1 Won!"
#define MSG_LOST "Player 1 Lost!"
#define MSG_TIED "Player 1 Lost!"

unsigned int OwariAlphaBetaMinValue(unsigned int board[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth);
unsigned int OwariAlphaBetaDIMinValue(unsigned int board[], unsigned int kmoves[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth);

unsigned int checkForWinner(unsigned int board[]) {
    unsigned int p1score = 0;
    unsigned int p2score = 0;
    unsigned int p1seeds = board[0] + board[1] + board[2] + board[3] + board[4] + board[5];
    unsigned int p2seeds = board[7] + board[8] + board[9] + board[10] + board[11] + board[12];

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

bool makeMoveP2(unsigned int move, unsigned int board[], unsigned int newBoard[]) {
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

    unsigned int seeds = newBoard[move];
    newBoard[move] = 0;
    ++move;
    if (move > P2_GOAL_PIT) {
        move = 0;
    }
    while (seeds > 1) {
        if (move != P1_GOAL_PIT) {
            ++newBoard[move];
            --seeds;
        }
        ++move;
        if (move > P2_GOAL_PIT) {
            move = 0;
        }
    }
    ++newBoard[move];
    if (move > P1_GOAL_PIT && move < P2_GOAL_PIT && newBoard[move] < 2) {
        newBoard[P2_GOAL_PIT] += newBoard[P2_MAX_PIT - move];
        newBoard[P2_MAX_PIT - move] = 0;
    }
    return true;
}

bool makeMoveP1(unsigned int move, unsigned int board[], unsigned int newBoard[]) {
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

    unsigned int seeds = newBoard[move];
    newBoard[move] = 0;
    ++move;
    if (move > P2_GOAL_PIT) {
        move = 0;
    }
    while (seeds > 1) {
        ++newBoard[move];
        --seeds;
        ++move;
        if (move > P2_MAX_PIT) {
            move = 0;
        }
    }

    ++newBoard[move];
    if (move < P1_GOAL_PIT && newBoard[move] < 2) {
        newBoard[P1_GOAL_PIT] += newBoard[P2_MAX_PIT - move];
        newBoard[P2_MAX_PIT - move] = 0;
    }
    return true;
}

unsigned int OwariAlphaBetaDIFindMove(unsigned int board[], unsigned int kmoves[], unsigned int depth) {
    unsigned int maxDepth = depth + 1;
    unsigned int mdepth = 8;
    unsigned int remDepth = depth - mdepth;
    unsigned int cdepth = 0;
    unsigned int alpha;
    unsigned int beta;
    unsigned int bestValue;
    unsigned int bestMove;
    unsigned int moveValue;
    unsigned int nextMove;

    unsigned int newBoard[BOARD_SIZE];
    while (mdepth < maxDepth) {
        alpha = ALPHA_MIN;
        bestValue = ALPHA_MIN;
        beta = BETA_MAX;
        bestMove = kmoves[cdepth];
        nextMove = P1_MIN_PIT;

        if (bestMove < INVALID_MOVE) {
            if (makeMoveP1(nextMove, board, newBoard)) {
                moveValue = OwariAlphaBetaDIMinValue(newBoard, kmoves, alpha, beta, cdepth, mdepth);
                bestValue = moveValue;

                if (bestValue > alpha) {
                    alpha = bestValue;
                }
            }
        }

        for (; nextMove < P1_GOAL_PIT; ++nextMove) {
            if (nextMove != bestMove && makeMoveP1(nextMove, board, newBoard)) {
                moveValue = OwariAlphaBetaDIMinValue(newBoard, kmoves, alpha, beta, cdepth, mdepth);
                if (moveValue > bestValue) {
                    bestValue = moveValue;
                    bestMove = nextMove;
                }

                if (bestValue > alpha) {
                    alpha = bestValue;
                }
            }
        }
        kmoves[cdepth] = bestMove;
        mdepth += remDepth;
    }
    return bestMove;
}

unsigned int OwariAlphaBetaDIMaxValue(unsigned int board[], unsigned int kmoves[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth) {
    unsigned int bestValue;
    unsigned int moveValue;
    unsigned int newBoard[BOARD_SIZE];
    unsigned int status = checkForWinner(board);
    unsigned int ndepth = cdepth + 1;
    unsigned int killerMove = kmoves[cdepth];
    unsigned int nextMove;
    if (status == STATE_P1_WIN) {
        return COST_P1_WIN;
    } else if (status == STATE_P2_WIN) {
        return COST_P2_WIN;
    } else if (status == STATE_TIED) {
        return COST_TIE;
    } else if (cdepth == mdepth) {
        return COST_TIE + board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6];
    } else {
        bestValue = ALPHA_MIN;
        if (killerMove < INVALID_MOVE) {
            if (makeMoveP1(killerMove, board, newBoard)) {
                moveValue = OwariAlphaBetaDIMinValue(newBoard, kmoves, alpha, beta, ndepth, mdepth);
                bestValue = moveValue;

                if (bestValue >= beta) {
                    return bestValue;
                }

                if (bestValue > alpha) {
                    alpha = bestValue;
                }
            }
        }
        nextMove = P1_MIN_PIT;
        for (; nextMove < P1_GOAL_PIT; ++nextMove) {
            if (nextMove != killerMove && makeMoveP1(nextMove, board, newBoard)) {
                moveValue = OwariAlphaBetaDIMinValue(newBoard, kmoves, alpha, beta, ndepth, mdepth);
                if (moveValue > bestValue) {
                    bestValue = moveValue;
                }

                if (bestValue >= beta) {
                    kmoves[cdepth] = nextMove;
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

unsigned int OwariAlphaBetaDIMinValue(unsigned int board[], unsigned int kmoves[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth) {
    unsigned int nextMove = P2_MIN_PIT;
    unsigned int bestValue = BETA_MAX;
    unsigned int moveValue = 0;
    bool moveResult = false;
    unsigned int newBoard[BOARD_SIZE];
    unsigned int status = checkForWinner(board);
    unsigned int ndepth = cdepth + 1;
    if (status == STATE_P1_WIN) {
        return COST_P1_WIN;
    } else if (status == STATE_P2_WIN) {
        return COST_P2_WIN;
    } else if (status == STATE_TIED) {
        return COST_TIE;
    } else if (cdepth == mdepth) {
        return COST_TIE - board[7] - board[8] - board[9] - board[10] - board[11] - board[12] - board[13];
    } else {
        for (; nextMove < P2_GOAL_PIT; ++nextMove) {
            if (makeMoveP2(nextMove, board, newBoard)) {
                moveValue = OwariAlphaBetaDIMaxValue(newBoard, kmoves, alpha, beta, ndepth, mdepth);
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

unsigned int OwariAlphaBetaFindMove(unsigned int board[], unsigned int depth) {
    unsigned int alpha = ALPHA_MIN;
    unsigned int beta = BETA_MAX;

    unsigned int bestValue = ALPHA_MIN;
    unsigned int bestMove = INVALID_MOVE;

    unsigned int moveValue = ALPHA_MIN;
    unsigned int nextMove = P1_MIN_PIT;

    unsigned int newBoard[BOARD_SIZE];

    for (; nextMove < P1_GOAL_PIT; ++nextMove) {
        if (makeMoveP1(nextMove, board, newBoard)) {
            moveValue = OwariAlphaBetaMinValue(newBoard, alpha, beta, 0, depth);
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

unsigned int OwariAlphaBetaMaxValue(unsigned int board[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth) {
    unsigned int nextMove = P1_MIN_PIT;
    unsigned int bestValue = ALPHA_MIN;
    unsigned int moveValue = 0;
    bool moveResult = false;
    unsigned int newBoard[BOARD_SIZE];
    unsigned int status = checkForWinner(board);
    unsigned int ndepth = cdepth + 1;
    if (status == STATE_P1_WIN) {
        return COST_P1_WIN;
    } else if (status == STATE_P2_WIN) {
        return COST_P2_WIN;
    } else if (status == STATE_TIED) {
        return COST_TIE;
    } else if (cdepth == mdepth) {
        return COST_TIE + board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6];
    } else {
        for (; nextMove < P1_GOAL_PIT; ++nextMove) {
            if (makeMoveP1(nextMove, board, newBoard)) {
                moveValue = OwariAlphaBetaMinValue(newBoard, alpha, beta, ndepth, mdepth);
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

unsigned int OwariAlphaBetaMinValue(unsigned int board[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth) {
    unsigned int nextMove = P2_MIN_PIT;
    unsigned int bestValue = BETA_MAX;
    unsigned int moveValue = 0;
    bool moveResult = false;
    unsigned int newBoard[BOARD_SIZE];
    unsigned int status = checkForWinner(board);
    unsigned int ndepth = cdepth + 1;
    if (status == STATE_P1_WIN) {
        return COST_P1_WIN;
    } else if (status == STATE_P2_WIN) {
        return COST_P2_WIN;
    } else if (status == STATE_TIED) {
        return COST_TIE;
    } else if (cdepth == mdepth) {
        return COST_TIE - board[7] - board[8] - board[9] - board[10] - board[11] - board[12] - board[13];
    } else {
        for (; nextMove < P2_GOAL_PIT; ++nextMove) {
            if (makeMoveP2(nextMove, board, newBoard)) {
                moveValue = OwariAlphaBetaMaxValue(newBoard, alpha, beta, ndepth, mdepth);
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

unsigned int getWhoMovesFirst() {
    return rand() % 2;
}

unsigned int getHumanMove(unsigned int board[], unsigned int validPits[]) {
    bool validMove = false;
    unsigned int i = 0;
    unsigned int move = INVALID_MOVE;
    unsigned int input = INVALID_MOVE;
    while (validMove == false) {
        printf("Pick a pit (%d, %d, %d, %d, %d, %d)? ",
            validPits[0], validPits[1], validPits[2], validPits[3], validPits[4], validPits[5]);
        cin >> input;

        for (i = 0; i < 6; ++i) {
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

unsigned int getHumanP1Move(unsigned int board[], unsigned int depth) {
    unsigned int validPits[] = {0, 1, 2, 3, 4, 5};
    return getHumanMove(board, validPits);
}

unsigned int getHumanP2Move(unsigned int board[], unsigned int depth) {
    unsigned int validPits[] = {12, 11, 10, 9, 8, 7};
    return getHumanMove(board, validPits);
};

void printBoard(unsigned int board[]) {
    printf("North: | %2d | %2d | %2d | %2d | %2d | %2d | %2d |    |\n",
        board[13], board[12], board[11], board[10], board[9], board[8], board[7]);

    printf("South: |    | %2d | %2d | %2d | %2d | %2d | %2d | %2d |\n",
        board[0], board[1], board[2], board[3], board[4], board[5], board[6]);
}

void printScore(unsigned int board[]) {
    unsigned int p1score = board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6];
    unsigned int p2score = board[7] + board[8] + board[9] + board[10] + board[11] + board[12] + board[13];
    printf("Score: %d %d\n", p2score, p1score);
}

void printStatus(unsigned int board[], unsigned int move, unsigned int turn, unsigned int moveCount) {
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

    unsigned int maxDepth = 18;

    unsigned int kmoves[100];
    unsigned int board[] = {3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0};
    unsigned int moveCount = 0;
    unsigned int turn = 0;
    unsigned int status = STATE_CONTINUE;

    fill(kmoves, kmoves+100, INVALID_MOVE);

    cout << MSG_WELCOME << endl;
    printBoard(board);

    while (true) {
        unsigned int move = INVALID_MOVE;

        if (turn == PLAYER_1) {

            begin = clock();
            move = OwariAlphaBetaDIFindMove(board, kmoves, maxDepth);
            //move = OwariAlphaBetaFindMove(board, maxDepth);
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