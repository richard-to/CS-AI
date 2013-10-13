package to.richard.owari.ai;

import to.richard.owari.Owari;

/**
 * Author: Richard To
 * Date: 10/12/13
 */
public class AlphaBetaPlayer extends Player {

    protected int _bestValueOverall;
    protected int _bestMoveOverall;
    protected int _branchesReturned;
    protected int _branches;

    public void makeMove(int[] board, int depth) {
        _startTime = System.currentTimeMillis();
        _elapsed = 0;

        _bestValueOverall = Integer.MIN_VALUE;
        _bestMoveOverall = 0;
        _branchesReturned = 0;
        _branches = 6;

        int[] newBoard;
        for (int i = 0; i < 6; ++i) {
            newBoard = Owari.makeMoveP1(i, board);
            if (newBoard != null) {
                Thread thread = new Thread(new RunAlphaBeta(i, board, depth));
                thread.start();
            } else {
                _branchesReturned++;
            }
        }
        checkResult();
    }

    public synchronized void checkResult() {
        if (_branchesReturned == _branches) {
            _elapsed = System.currentTimeMillis() - _startTime;
            _listener.movePerformed(_bestMoveOverall);
        }
    }

    public synchronized void returnResult(int bestMove, int bestValue) {
        _branchesReturned++;
        if (bestValue > _bestValueOverall) {
            _bestMoveOverall = bestMove;
            _bestValueOverall = bestValue;
        }
        checkResult();
    }

    private class RunAlphaBeta implements Runnable {
        private int[] _board;
        private int _maxDepth;
        private int _moveId;

        public RunAlphaBeta(int moveId, int[] board, int maxDepth) {
            _moveId = moveId;
            _board = board;
            _maxDepth = maxDepth;
        }

        public void run() {
            int currentDepth = 0;
            int bestMoveValue = Integer.MAX_VALUE;
            int bestMove = 0;

            int alpha = Integer.MIN_VALUE;
            int beta = Integer.MAX_VALUE;
            int moveValue = 0;
            int[] newBoard;
            for (int i = 7; i < 14; ++i) {
                newBoard = Owari.makeMoveP2(i, _board);
                if (newBoard != null) {
                    moveValue = maxValue(newBoard, alpha, beta, currentDepth, _maxDepth);
                    if (moveValue < bestMoveValue) {
                        bestMoveValue = moveValue;
                        bestMove = i;
                    }
                }
            }
            returnResult(_moveId, bestMoveValue);
        }

        public int minValue(int[] board, int alpha, int beta, int currentDepth, int maxDepth) {
            int status = Owari.checkForWinner(board);
            if (status == 0) {
                return -100;
            } else if (status == 1) {
                return 100;
            } else if (status == 2) {
                return 50;
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
                        moveValue = maxValue(newBoard, alpha, beta, currentDepth + 1, maxDepth);
                        if (moveValue < bestMoveValue) {
                            bestMoveValue = moveValue;
                        }

                        if (bestMoveValue <= alpha) {
                            return bestMoveValue;
                        }

                        if (bestMoveValue < beta) {
                            beta = bestMoveValue;
                        }
                    }
                }
                return bestMoveValue;
            }
        }

        public int maxValue(int[] board, int alpha, int beta, int currentDepth, int maxDepth) {
            int status = Owari.checkForWinner(board);
            if (status == 0) {
                return -100;
            } else if (status == 1) {
                return 100;
            } else if (status == 2) {
                return -50;
            } else if (currentDepth == maxDepth) {
                return ((board[7] + board[8] + board[9] + board[10] + board[11] + board[12] + board[13]) -
                        (board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6]));
            } else {
                int bestMoveValue = Integer.MIN_VALUE;
                int moveValue = 0;
                int[] newBoard;
                for (int i = 0; i < 6; ++i) {
                    newBoard = Owari.makeMoveP1(i, board);
                    if (newBoard != null) {
                        moveValue = minValue(newBoard, alpha, beta, currentDepth + 1, maxDepth);
                        if (moveValue > bestMoveValue) {
                            bestMoveValue = moveValue;
                        }

                        if (bestMoveValue >= beta) {
                            return bestMoveValue;
                        }

                        if (bestMoveValue > alpha) {
                            alpha = bestMoveValue;
                        }
                    }
                }
                return bestMoveValue;
            }
        }
    }
}