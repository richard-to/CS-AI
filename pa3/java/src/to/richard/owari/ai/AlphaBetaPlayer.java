package to.richard.owari.ai;

import to.richard.owari.Owari;

/**
 * Author: Richard To
 * Date: 10/25/13
 */
public class AlphaBetaPlayer extends Player {

    public void makeMove(int[] board, int depth, int moveCount) {
        _startTime = System.currentTimeMillis();
        _elapsed = 0;

        int currentDepth = 0;
        int bestValue = Integer.MIN_VALUE;
        int bestMove = 0;
        int alpha = Integer.MIN_VALUE;
        int beta = Integer.MAX_VALUE;


        int moveValue = 0;
        int[] newBoard;
        for (int i = 0; i < 6; ++i) {
            newBoard = Owari.makeMoveP1(i, board);
            if (newBoard != null) {
                moveValue = minValue(newBoard, alpha, beta, currentDepth, depth);
                if (moveValue > bestValue) {
                    bestValue = moveValue;
                    bestMove = i;
                }

                if (bestValue >= beta) {
                    break;
                }

                if (bestValue > alpha) {
                    alpha = bestValue;
                }
            }
        }
        _elapsed = System.currentTimeMillis() - _startTime;
        _listener.movePerformed(bestMove);
    }

    public int minValue(int[] board, int alpha, int beta, int currentDepth, int maxDepth) {
        int status = Owari.checkForWinner(board);
        if (status == Owari.STATE_P2_WIN) {
            return -100;
        } else if (status == Owari.STATE_P1_WIN) {
            return 100;
        } else if (status == Owari.STATE_TIED) {
            return 0;
        } else if (currentDepth == maxDepth) {
            return -1 * (board[7] + board[8] + board[9] + board[10] + board[11] + board[12] + board[13]);
        } else {
            int bestValue = Integer.MAX_VALUE;
            int moveValue = 0;
            int[] newBoard;
            for (int i = 7; i < 14; ++i) {
                newBoard = Owari.makeMoveP2(i, board);
                if (newBoard != null) {
                    moveValue = maxValue(newBoard, alpha, beta, currentDepth + 1, maxDepth);
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

    public int maxValue(int[] board, int alpha, int beta, int currentDepth, int maxDepth) {
        int status = Owari.checkForWinner(board);
        if (status == Owari.STATE_P2_WIN) {
            return -100;
        } else if (status == Owari.STATE_P1_WIN) {
            return 100;
        } else if (status == Owari.STATE_TIED) {
            return 0;
        } else if (currentDepth == maxDepth) {
            return (board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6]);
        } else {
            int bestValue = Integer.MIN_VALUE;
            int moveValue = 0;
            int[] newBoard;
            for (int i = 0; i < 6; ++i) {
                newBoard = Owari.makeMoveP1(i, board);
                if (newBoard != null) {
                    moveValue = minValue(newBoard, alpha, beta, currentDepth + 1, maxDepth);
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
}
