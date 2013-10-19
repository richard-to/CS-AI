package to.richard.owari;

import java.util.ArrayList;

/**
 * Author: Richard To
 * Date: 10/11/13
 */
public class Owari {
    public static final int[] BOARD = {3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0};

    public static final int SEEDS = 3;
    public static final int GOAL_SEEDS = 0;

    public static final int NUM_CUPS = 14;
    public static final int CUPS_EACH = 6;

    public static final int[] P1_CUPS = {0, 5};
    public static final int P1_GOAL = 6;

    public static final int[] P2_CUPS = {7, 12};
    public static final int P2_GOAL = 13;

    public static final int CPU_PLAYER = 0;
    public static final int HUMAN_PLAYER = 1;

    public static final int STATE_P2_WIN = 0;
    public static final int STATE_P1_WIN = 1;
    public static final int STATE_TIED = 2;
    public static final int STATE_CONTINUE = 3;

    public static int[] createBoard() {
        return BOARD.clone();
    }

    public static final int calcScoreDiff(int[] board) {
        int p1Score = board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6];
        int p2Score = board[7] + board[8] + board[9] + board[10] + board[11] + board[12] + board[13];
        return p2Score - p1Score;
    }

    public static final int checkForWinner(int[] board) {
        int p1SeedSum = board[0] + board[1] + board[2] + board[3] + board[4] + board[5];
        int p2SeedSum = board[7] + board[8] + board[9] + board[10] + board[11] + board[12];
        if (p1SeedSum == 0 || p2SeedSum == 0) {
            int p1Score = p1SeedSum + board[6];
            int p2Score = p2SeedSum + board[13];
            if (p2Score > p1Score) {
                return 0;
            } else if (p1Score > p2Score) {
                return 1;
            } else {
                return 2;
            }
        } else {
            return 3;
        }
    }

    public static final int[] makeMoveP1(int move, int[] board) {
        if (board[move] == 0) {
            return null;
        }
        int[] newBoard = board.clone();
        int next = (move + 1) % 14;
        int seeds = newBoard[move];
        newBoard[move] = 0;
        while (seeds > 0) {
            if (next != 13) {
                newBoard[next] += 1;
                if (seeds == 1 && newBoard[next] == 1 && next >= 0 && next <= 5) {
                    newBoard[6] += newBoard[12 - next];
                    newBoard[12 - next] = 0;
                }
                seeds -= 1;
            }
            next = (next + 1) % 14;
        }
        return newBoard;
    }

    public static final int[] makeMoveP2(int move, int[] board) {
        if (board[move] == 0) {
            return null;
        }
        int[] newBoard = board.clone();
        int next = (move + 1) % 14;
        int seeds = newBoard[move];
        newBoard[move] = 0;
        while (seeds > 0) {
            if (next != 6) {
                newBoard[next] += 1;
                if (seeds == 1 && newBoard[next] == 1 && next >= 7 && next <= 12) {
                    newBoard[13] += newBoard[12 - next];
                    newBoard[12 - next] = 0;
                }
                seeds -= 1;
            }
            next = (next + 1) % 14;
        }
        return newBoard;
    }
}
