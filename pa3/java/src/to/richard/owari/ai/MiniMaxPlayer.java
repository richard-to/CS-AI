package to.richard.owari.ai;

import to.richard.owari.Owari;

/**
 * Author: Richard To
 * Date: 10/12/13
 */
public class MiniMaxPlayer implements IComputerAi {
    public int makeMove(int[] board, int depth) {
        int currentDepth = 0;
        int bestMoveValue = Integer.MIN_VALUE;
        int bestMove = 0;

        int moveValue = 0;
        int[] newBoard;
        for (int i = 0; i < 6; ++i) {
            newBoard = Owari.makeMoveP1(i, board);
            if (newBoard != null) {
                moveValue = minValue(newBoard, currentDepth, depth);
                if (moveValue > bestMoveValue) {
                    bestMoveValue = moveValue;
                    bestMove = i;
                }
            }
        }
        return bestMove;
    }

    public int minValue(int[] board, int currentDepth, int maxDepth) {
        int status = Owari.checkForWinner(board);
        if (status == 0) {
            return -100;
        } else if (status == 1) {
            return 100;
        } else if (status == 2) {
            return 0;
        } else if (currentDepth == maxDepth) {
            return ((board[7] + board[8] + board[9] + board[10] + board[11] + board[12] + board[13]) -
                (board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6]));
        } else {
            int bestMoveValue = Integer.MAX_VALUE;
            int moveValue = 0;
            int[] newBoard;
            for (int i = 7; i < 14; ++i) {
                newBoard = Owari.makeMoveP2(i, board);
                if (newBoard != null) {
                    moveValue = maxValue(newBoard, currentDepth + 1, maxDepth);
                    if (moveValue < bestMoveValue) {
                        bestMoveValue = moveValue;
                    }
                }
            }
            return bestMoveValue;
        }
    }

    public int maxValue(int[] board, int currentDepth, int maxDepth) {
        int status = Owari.checkForWinner(board);
        if (status == 0) {
            return -100;
        } else if (status == 1) {
            return 100;
        } else if (status == 2) {
            return 0;
        } else if (currentDepth == maxDepth) {
            return ((board[7] + board[8] + board[9] + board[10] + board[11] + board[12] + board[13]) -
                    (board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6]));
        } else {
            int bestMoveValue = Integer.MIN_VALUE;
            int moveValue = 0;
            int[] newBoard;
            for (int i = 0; i < 6; ++i) {
                newBoard = Owari.makeMoveP2(i, board);
                if (newBoard != null) {
                    moveValue = minValue(newBoard, currentDepth + 1, maxDepth);
                    if (moveValue > bestMoveValue) {
                        bestMoveValue = moveValue;
                    }
                }
            }
            return bestMoveValue;
        }
    }
}
