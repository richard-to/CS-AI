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
#define BETA_MAX 128

#define COST_P1_WIN 100
#define COST_P2_WIN 28
#define COST_TIE 64

#define SEEDS_TIE 18

#define MSG_WELCOME "Welcome to Owari!"
#define MSG_WIN "Player 1 Won!"
#define MSG_LOST "Player 2 Won!"
#define MSG_TIED "Tie Game!"

#define DEPTH_INCREMENT 5
#define DEPTH_LOOPS 2

#define TTABLE_SIZE 524287
#define TTABLE_DATA_LEN 16

unsigned int *cachehit = new unsigned int;
unsigned int (*ttable)[TTABLE_DATA_LEN] = new unsigned int[TTABLE_SIZE][TTABLE_DATA_LEN];

unsigned int OwariAlphaBetaMinValue(unsigned int board[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth);
unsigned int OwariAlphaBetaDIMinValue(unsigned int board[], unsigned int kmoves[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth);
unsigned int OwariAlphaBetaTTMinValue(unsigned int board[], unsigned int kmoves[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth);

// Hash function for transposition table. Uses a modified version of
// Jenkins One at a Time Hash from: http://en.wikipedia.org/wiki/Jenkins_hash_function.
// The main modification is passing in an unsigned int array. Additionally,
// the modulus step for the hash to table is combined here
unsigned int ttable_hasher(unsigned int key[]) {
    unsigned int hash, i;
    for (hash = i = 0; i < 14; ++i) {
        hash += key[i];
        hash += (hash << 10);
        hash ^= (hash >> 6);
    }
    hash += (hash << 3);
    hash ^= (hash >> 11);
    hash += (hash << 15);

    if (hash < TTABLE_SIZE) {
        return hash;
    } else {
        return hash % TTABLE_SIZE;
    }
}

// Checks the board for a winner
// A winner is declared when one side has no more seeds.
// The winner is the one with the most seeds.
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

// Make a move for player 2. For speed this function does minimal validation of
// valid moves. The only case that we really check is if the selected pit has no
// seeds left. This is necessary for running alpha-beta or minimax algorithms.
//
// For P2, we distribute seeds in a counter-clockwise manner and skip P1's goal
// pit. If P2 lands on an empty pit that it owns, we can take the adjacent seeds.
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
    if (move == P1_GOAL_PIT) {
        ++newBoard[++move];
    } else {
        ++newBoard[move];
    }
    if (move > P1_GOAL_PIT && move < P2_GOAL_PIT && newBoard[move] < 2) {
        newBoard[P2_GOAL_PIT] += newBoard[P2_MAX_PIT - move];
        newBoard[P2_MAX_PIT - move] = 0;
    }
    return true;
}

// Make a move for player 1. For speed this function does minimal validation of
// valid moves. The only case that we really check is if the selected pit has no
// seeds left. This is necessary for running alpha-beta or minimax algorithms.
//
// For P1, we distribute seeds in a counter-clockwise manner and skip P2's goal
// pit. If P1 lands on an empty pit that it owns, we can take the adjacent seeds.
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
    if (move > P2_MAX_PIT) {
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

// Implementation of Alpha Beta with Aspiration Windows. Essentially the same as the
// the version with Iterative Deepening and Killer move heuristic.
//
// Basically adjust the window on each iteration based on the best value found.
// For instance, if the best value is 40 and the window is 5, then alpha equals 40 - 5 and
// beta equals 40 + 5.
unsigned int OwariAlphaBetaAWFindMove(unsigned int board[], unsigned int kmoves[], unsigned int depth) {
    unsigned int maxDepth = depth + 1;
    unsigned int mdepth = 0;
    unsigned int cdepth = 0;
    unsigned int alpha = ALPHA_MIN;
    unsigned int beta = BETA_MAX;
    unsigned int window = 3;
    unsigned int bestValue;
    unsigned int bestMove;
    unsigned int moveValue;
    unsigned int nextMove;
    unsigned int newBoard[BOARD_SIZE];

    if (depth > DEPTH_INCREMENT * DEPTH_LOOPS) {
        mdepth = depth - DEPTH_INCREMENT * DEPTH_LOOPS;
    } else {
        mdepth = depth;
    }

    while (mdepth < maxDepth) {
        bestValue = ALPHA_MIN;
        bestMove = kmoves[cdepth];
        nextMove = P1_MIN_PIT;

        if (bestMove < INVALID_MOVE) {
            if (makeMoveP1(bestMove, board, newBoard)) {
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

        if (bestValue < alpha || bestValue > beta) {
            alpha = ALPHA_MIN;
            beta = BETA_MAX;
        } else {
            alpha = bestValue - window;
            beta = bestValue + window;
            mdepth += DEPTH_INCREMENT;
        }
    }

    return bestMove;
}

// Failed implementation of Alpha Beta using a transposition table. Not much to
// say here since this basically a copy and paste of the iterative deepening function.
// Only difference is we call the transposition table versions of the min and max functions.
unsigned int OwariAlphaBetaTTFindMove(unsigned int board[], unsigned int kmoves[], unsigned int depth) {
    unsigned int maxDepth = depth + 1;
    unsigned int mdepth = 0;
    unsigned int cdepth = 0;
    unsigned int alpha;
    unsigned int beta;
    unsigned int bestValue;
    unsigned int bestMove;
    unsigned int moveValue;
    unsigned int nextMove;
    unsigned int newBoard[BOARD_SIZE];

    if (depth > DEPTH_INCREMENT * DEPTH_LOOPS) {
        mdepth = depth - DEPTH_INCREMENT * DEPTH_LOOPS;
    } else {
        mdepth = depth;
    }

    while (mdepth < maxDepth) {
        alpha = ALPHA_MIN;
        bestValue = ALPHA_MIN;
        beta = BETA_MAX;
        bestMove = kmoves[cdepth];
        nextMove = P1_MIN_PIT;

        if (bestMove < INVALID_MOVE) {
            if (makeMoveP1(bestMove, board, newBoard)) {
                moveValue = OwariAlphaBetaTTMinValue(newBoard, kmoves, alpha, beta, cdepth, mdepth);
                bestValue = moveValue;

                if (bestValue > alpha) {
                    alpha = bestValue;
                }
            }
        }

        for (; nextMove < P1_GOAL_PIT; ++nextMove) {
            if (nextMove != bestMove && makeMoveP1(nextMove, board, newBoard)) {
                moveValue = OwariAlphaBetaTTMinValue(newBoard, kmoves, alpha, beta, cdepth, mdepth);
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
        mdepth += DEPTH_INCREMENT;
    }
    return bestMove;
}

// Alpha Beta max value function implementation that uses a transposition table.
// Again, basically the same as the iterative deepening version, except we need to
// check if the board state is in the cache and at the appropriate depth. If it is
// we will stop here and use that value instead.
//
// Additionally we will store the best value and depth all our branches have returned or
// we hit a cut off.
unsigned int OwariAlphaBetaTTMaxValue(unsigned int board[], unsigned int kmoves[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth) {
    unsigned int bestValue = ALPHA_MIN;
    unsigned int moveValue;
    unsigned int newBoard[BOARD_SIZE];
    unsigned int status = checkForWinner(board);
    unsigned int ndepth = cdepth + 1;
    unsigned int killerMove = kmoves[cdepth];
    unsigned int nextMove = P1_MIN_PIT;
    unsigned int hash = ttable_hasher(board);
    unsigned int *p = ttable[hash];
    if (status == STATE_P1_WIN) {
        return COST_P1_WIN;
    } else if (status == STATE_P2_WIN) {
        return COST_P2_WIN;
    } else if (status == STATE_TIED) {
        return COST_TIE;
    } else if (cdepth == mdepth) {
        return COST_TIE + board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6] -
            board[7] - board[8] - board[9] - board[10] - board[11] - board[12] - board[13];
    } else {
        if (p[14] >= mdepth &&
                p[13] == board[13] && p[12] == board[12] &&
                p[11] == board[11] && p[10] == board[10] &&
                p[9] == board[9] && p[8] == board[8] &&
                p[7] == board[7] && p[6] == board[6] &&
                p[5] == board[5] && p[4] == board[4] &&
                p[3] == board[3] && p[2] == board[2] &&
                p[1] == board[1] && p[0] == board[0]) {
            return p[15];
        }

        if (killerMove < INVALID_MOVE) {
            if (makeMoveP1(killerMove, board, newBoard)) {
                moveValue = OwariAlphaBetaTTMinValue(newBoard, kmoves, alpha, beta, ndepth, mdepth);
                bestValue = moveValue;

                if (bestValue >= beta) {
                    return bestValue;
                }

                if (bestValue > alpha) {
                    alpha = bestValue;
                }
            }
        }
        for (; nextMove < P1_GOAL_PIT; ++nextMove) {
            if (nextMove != killerMove && makeMoveP1(nextMove, board, newBoard)) {
                moveValue = OwariAlphaBetaTTMinValue(newBoard, kmoves, alpha, beta, ndepth, mdepth);
                if (moveValue > bestValue) {
                    bestValue = moveValue;
                }

                if (bestValue >= beta) {
                    kmoves[cdepth] = nextMove;
                    if (mdepth > ttable[hash][14]) {
                        std::copy(&board[0], &board[13], p);
                        ttable[hash][14] = mdepth;
                        ttable[hash][15] = bestValue;
                    }
                    return bestValue;
                }

                if (bestValue > alpha) {
                    alpha = bestValue;
                }
            }
        }

        if (mdepth > ttable[hash][14]) {
            std::copy(&board[0], &board[13], p);
            ttable[hash][14] = mdepth;
            ttable[hash][15] = bestValue;
        }
        return bestValue;
    }
}

// Baisically the same function as the regular min value function except we call the
// transposition table version of max.
unsigned int OwariAlphaBetaTTMinValue(unsigned int board[], unsigned int kmoves[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth) {
    unsigned int nextMove = P2_MIN_PIT;
    unsigned int bestValue = BETA_MAX;
    unsigned int moveValue = 0;
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
        return COST_TIE + board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6] -
            board[7] - board[8] - board[9] - board[10] - board[11] - board[12] - board[13];
    } else {
        for (; nextMove < P2_GOAL_PIT; ++nextMove) {
            if (makeMoveP2(nextMove, board, newBoard)) {
                moveValue = OwariAlphaBetaTTMaxValue(newBoard, kmoves, alpha, beta, ndepth, mdepth);
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

// Iterative Deepening version of alpha beta with killer move heuristic
//
// For the iterative deepening we don't do increment by increase by one ply. Instead we
// will do three iterations. The first will be depth - 10, then depth - 5, and finally depth.
// This seems to work well, maybe due to the number of branches to take. More fine grained incrementing
// tends to be slower.
//
// Killer move heuristic is also implemented. We only store one best move for each depth. Basically
// we will try the killer move first before attempting the other moves.
unsigned int OwariAlphaBetaDIFindMove(unsigned int board[], unsigned int kmoves[], unsigned int depth) {
    unsigned int maxDepth = depth + 1;
    unsigned int mdepth = 0;
    unsigned int cdepth = 0;
    unsigned int alpha;
    unsigned int beta;
    unsigned int bestValue;
    unsigned int bestMove;
    unsigned int moveValue;
    unsigned int nextMove;
    unsigned int newBoard[BOARD_SIZE];

    if (depth > DEPTH_INCREMENT * DEPTH_LOOPS) {
        mdepth = depth - DEPTH_INCREMENT * DEPTH_LOOPS;
    } else {
        mdepth = depth;
    }

    while (mdepth < maxDepth) {
        alpha = ALPHA_MIN;
        bestValue = ALPHA_MIN;
        beta = BETA_MAX;
        bestMove = kmoves[cdepth];
        nextMove = P1_MIN_PIT;

        if (bestMove < INVALID_MOVE) {
            if (makeMoveP1(bestMove, board, newBoard)) {
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
        mdepth += DEPTH_INCREMENT;
    }
    return bestMove;
}

// This version of max basically adds the killer move heuristic. This is only used on max.
// For some reason we some slow down if we implement use this on min too.
unsigned int OwariAlphaBetaDIMaxValue(unsigned int board[], unsigned int kmoves[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth) {
    unsigned int bestValue = ALPHA_MIN;
    unsigned int moveValue;
    unsigned int newBoard[BOARD_SIZE];
    unsigned int status = checkForWinner(board);
    unsigned int ndepth = cdepth + 1;
    unsigned int killerMove = kmoves[cdepth];
    unsigned int nextMove = P1_MIN_PIT;
    if (status == STATE_P1_WIN) {
        return COST_P1_WIN;
    } else if (status == STATE_P2_WIN) {
        return COST_P2_WIN;
    } else if (status == STATE_TIED) {
        return COST_TIE;
    } else if (cdepth == mdepth) {
        return COST_TIE + board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6] -
            board[7] - board[8] - board[9] - board[10] - board[11] - board[12] - board[13];
    } else {
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

// Basically the regular alpha beta version of min with th exception that we call the
// iterative deepening version of max.
unsigned int OwariAlphaBetaDIMinValue(unsigned int board[], unsigned int kmoves[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth) {
    unsigned int nextMove = P2_MIN_PIT;
    unsigned int bestValue = BETA_MAX;
    unsigned int moveValue;
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
        return COST_TIE + board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6] -
            board[7] - board[8] - board[9] - board[10] - board[11] - board[12] - board[13];
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

// Baseline alpha beta version for performance comparison
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

            if (bestValue > alpha) {
                alpha = bestValue;
            }
        }
    }
    return bestMove;
}

// Baseline alpha beta version max value function
unsigned int OwariAlphaBetaMaxValue(unsigned int board[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth) {
    unsigned int nextMove = P1_MIN_PIT;
    unsigned int bestValue = ALPHA_MIN;
    unsigned int moveValue = 0;
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
        return COST_TIE + board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6] -
            board[7] - board[8] - board[9] - board[10] - board[11] - board[12] - board[13];
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

// Baseline alpha beta version min value function
unsigned int OwariAlphaBetaMinValue(unsigned int board[], unsigned int alpha, unsigned int beta, unsigned int cdepth, unsigned int mdepth) {
    unsigned int nextMove = P2_MIN_PIT;
    unsigned int bestValue = BETA_MAX;
    unsigned int moveValue = 0;
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
        return COST_TIE + board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6] -
            board[7] - board[8] - board[9] - board[10] - board[11] - board[12] - board[13];
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

// A basic way to select who goes first. Press any value other than 2
// will default to player 1 going first.
unsigned int getWhoMovesFirst() {
    unsigned int input = 0;
    cout << "Who is going first? (1/2): ";
    cin >> input;
    if (input == 2) {
        input = 1;
    } else {
        input = 0;
    }
    return input;
}

// This functions gets the user input for what move to select.
//
// There is a quick hack to allow the user to change the search depth in
// in mid-game. This can be done by specifying a value over 100.
//
// The depth will then be calculated by taking the input modulus 100. Probably
// shouldn't go here, but it works for now.
unsigned int getHumanMove(unsigned int board[], unsigned int validPits[]) {
    bool validMove = false;
    unsigned int i = 0;
    unsigned int move = INVALID_MOVE;
    unsigned int input = INVALID_MOVE;
    while (validMove == false) {
        printf("Pick a pit (%d, %d, %d, %d, %d, %d)? ",
            validPits[0], validPits[1], validPits[2], validPits[3], validPits[4], validPits[5]);
        cin >> input;

        if (input > 100) {
            return input;
        }

        for (i = 0; i < 6; ++i) {
            if (input == validPits[i] && board[input] > 0) {
                validMove = true;
                move = input;
                break;
            }
        }

        if (validMove == false) {
            cout << "Please select a valid pit!" << endl;
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

// Print board state. It is a bit hard to read and is confusing. Mainly
// formatted like this for in-class tournament.
void printBoard(unsigned int board[]) {
    cout << "       |    |  5 |  4 |  3 |  2 |  1 |  0 |    |" << endl;
    cout << "       |    | 12 | 11 | 10 |  9 |  8 |  7 |    |" << endl;
    cout << "------------------------------------------------" << endl;
    printf("North: | %2d | %2d | %2d | %2d | %2d | %2d | %2d |    |\n",
        board[13], board[12], board[11], board[10], board[9], board[8], board[7]);

    printf("South: |    | %2d | %2d | %2d | %2d | %2d | %2d | %2d |\n",
        board[0], board[1], board[2], board[3], board[4], board[5], board[6]);
    cout << "------------------------------------------------" << endl;
    cout << "       |    |  0 |  1 |  2 |  3 |  4 |  5 |    |" << endl;
    cout << "       |    |  7 |  8 |  9 | 10 | 11 | 12 |    |" << endl;
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

// For matches where it is computer versus computer, we need to
// flip the board since the alpha-beta implementations assume the
// computer is always player 1 or south.
void reverseBoard(unsigned int board[], unsigned int rboard[]) {
    rboard[0] = board[7];
    rboard[1] = board[8];
    rboard[2] = board[9];
    rboard[3] = board[10];
    rboard[4] = board[11];
    rboard[5] = board[12];
    rboard[6] = board[13];
    rboard[7] = board[0];
    rboard[8] = board[1];
    rboard[9] = board[2];
    rboard[10] = board[3];
    rboard[11] = board[4];
    rboard[12] = board[5];
    rboard[13] = board[6];
}

// Main game loop implementation. Needs to be cleaned up, but good
// enough for now.
void runOwari() {
    srand(time(NULL));

    clock_t begin;
    clock_t end;

    bool invalidMove = true;

    unsigned int p1mdepth = 19;
    unsigned int p2mdepth = 19;
    unsigned int p1kmoves[100];
    unsigned int p2kmoves[100];
    unsigned int board[] = {3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0};
    unsigned int rboard[] = {3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0};

    unsigned int moveCount = 0;
    unsigned int turn = 0;
    unsigned int status = STATE_CONTINUE;

    fill(p1kmoves, p1kmoves + 100, INVALID_MOVE);
    fill(p2kmoves, p2kmoves + 100, INVALID_MOVE);

    cout << MSG_WELCOME << endl;

    turn = getWhoMovesFirst();

    printBoard(board);

    while (true) {
        unsigned int move = INVALID_MOVE;

        if (turn == PLAYER_1) {
            begin = clock();
            move = OwariAlphaBetaDIFindMove(board, p1kmoves, p1mdepth);
            //move = OwariAlphaBetaAWFindMove(board, p1kmoves, p1mdepth);
            end = clock();
            cout << "Elapsed time: " << double(end - begin) / CLOCKS_PER_SEC << endl;
            makeMoveP1(move, board, board);
        } else {

            /*
            begin = clock();
            reverseBoard(board, rboard);
            move = P2_MIN_PIT + OwariAlphaBetaDIFindMove(rboard, p2kmoves, p2mdepth);
            //move = P2_MIN_PIT + OwariAlphaBetaAWFindMove(rboard, p2kmoves, p2mdepth);
            reverseBoard(rboard, board);
            end = clock();
            cout << "Elapsed time: " << double(end - begin) / CLOCKS_PER_SEC << endl;
            */
            invalidMove = true;

            while (invalidMove) {
                move = getHumanP2Move(board, p2mdepth);
                if (move >= 100) {
                    p1mdepth = move % 100;
                    cout << "Depth changed to " << p1mdepth << "!" << endl;
                } else {
                    invalidMove = false;
                }
            }

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
