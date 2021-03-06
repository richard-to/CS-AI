package to.richard.owari.ai;

import to.richard.owari.Owari;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.IntBuffer;
import java.nio.channels.SocketChannel;
import java.util.Arrays;

/**
 * Author: Richard To
 * Date: 10/12/13
 */
public class AlphaBetaPlayerTT extends Player {

    public int _bestValueOverall;
    public int _bestMoveOverall;
    public int _branchesReturned;
    public int _branches;
    public int[] _killerMoves;
    public RunAlphaBeta[] _alphaBetaJobs;

    public AlphaBetaPlayerTT(SocketChannel[] scs) {
        _alphaBetaJobs = new RunAlphaBeta[6];
        for (int i = 0; i < 6; i++) {
            _alphaBetaJobs[i] = new RunAlphaBeta(scs[i]);
        }
        _killerMoves = new int[100];
        Arrays.fill(_killerMoves, -1);
    }

    public void makeMove(int[] board, int depth, int moveCount) {
        _startTime = System.currentTimeMillis();
        _elapsed = 0;

        _bestValueOverall = Integer.MIN_VALUE;
        _bestMoveOverall = 0;
        _branchesReturned = 0;
        _branches = 6;

        int[] newBoard;
        Thread[] threads =  new Thread[6];
        for (int i = 0; i < 6; ++i) {
            newBoard = Owari.makeMoveP1(i, board);
            if (newBoard != null) {
                _alphaBetaJobs[i].setup(i, newBoard, depth, moveCount, _killerMoves.clone());
                Thread thread = new Thread(_alphaBetaJobs[i]);
                thread.start();
                threads[i] = thread;
            } else {
                _branchesReturned++;
            }
        }

        //Thread threadStopperThread = new Thread(new ThreadStopper(threads));
        //threadStopperThread.start();

        checkResult();
    }

    public synchronized void checkResult() {
        if (_branchesReturned == _branches) {
            _elapsed = System.currentTimeMillis() - _startTime;
            _listener.movePerformed(_bestMoveOverall);
            for (RunAlphaBeta job : _alphaBetaJobs) {
                if (job._moveId == _bestMoveOverall) {
                    System.out.println(job._endDepth);
                    _killerMoves = job._killerMoves.clone();
                    break;
                }
            }
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

    private class ThreadStopper implements Runnable {
        private Thread[] _threads;
        public ThreadStopper(Thread[] threads) {
            _threads = threads;
        }

        public void run() {
            try {
                Thread.sleep(20000);
                for (Thread thread : _threads) {
                    if (thread != null) {
                        thread.interrupt();
                    }
                }
            } catch (InterruptedException e) {

            }
        }
    }

    private class RunAlphaBeta implements Runnable {
        public int[] _board;
        public int _maxDepth;
        public int _moveId;
        public int[] _killerMoves;
        public int _moveCount;
        public int _currentBestValue;
        public int _endDepth;
        public SocketChannel _sc;
        public ByteBuffer _readBuffer;
        public ByteBuffer _writeBuffer;
        public IntBuffer _intBuffer;
        public byte[] _readBytes;

        public RunAlphaBeta(SocketChannel sc) {
            _sc = sc;
            _readBytes = new byte[] {0, 0, 0};
            _readBuffer = ByteBuffer.wrap(_readBytes);
            _writeBuffer= ByteBuffer.allocate(16 * 4);
            _intBuffer = _writeBuffer.asIntBuffer();
        }

        public void setup(int moveId, int[] board, int maxDepth, int moveCount, int[] killerMoves) {
            _moveId = moveId;
            _board = board;
            _maxDepth = maxDepth;
            _killerMoves = killerMoves;
            _moveCount = moveCount;
        }

        public void run() {
            _endDepth = 0;
            _currentBestValue = 0;
            int currentDepth = 0;
            int bestValue = Integer.MAX_VALUE;
            int bestMove = _killerMoves[currentDepth + _moveCount];
            int alpha = Integer.MIN_VALUE;
            int beta = Integer.MAX_VALUE;
            int moveValue = 0;
            int[] newBoard;

            int status = Owari.checkForWinner(_board);
            if (status == Owari.STATE_P2_WIN) {
                bestValue = 100;
            } else if (status == Owari.STATE_P1_WIN) {
                bestValue = 300;
            } else if (status == Owari.STATE_TIED) {
                bestValue = 200;
            } else {
                for (int d = 1; d <= _maxDepth; d++) {
                    d += 2;

                    if (d > _maxDepth) {
                        d = _maxDepth;
                    }
                    currentDepth = 0;
                    bestValue = Integer.MAX_VALUE;
                    alpha = Integer.MIN_VALUE;
                    beta = Integer.MAX_VALUE;
                    moveValue = 0;

                    if (bestMove > -1) {
                        newBoard = Owari.makeMoveP2(bestMove, _board);
                        if (newBoard != null) {
                            moveValue = maxValue(newBoard, alpha, beta, currentDepth, d);
                            bestValue = moveValue;

                            if (bestValue <= alpha) {
                                break;
                            }

                            if (bestValue < beta) {
                                beta = bestValue;
                            }
                        }
                    }

                    for (int i = 7; i < 14; ++i) {
                        if (i != bestMove) {
                            newBoard = Owari.makeMoveP2(i, _board);
                            if (newBoard != null) {
                                moveValue = maxValue(newBoard, alpha, beta, currentDepth, d);
                                if (Thread.currentThread().isInterrupted()) {
                                    break;
                                }

                                if (moveValue < bestValue) {
                                    bestValue = moveValue;
                                    bestMove = i;
                                }
                                if (bestValue <= alpha) {
                                    break;
                                }

                                if (bestValue < beta) {
                                    beta = bestValue;
                                }
                            }
                        }
                    }

                    if (!Thread.currentThread().isInterrupted()) {
                        _currentBestValue = bestValue;
                        _endDepth = d;
                    } else {
                        break;
                    }

                }
            }
            returnResult(_moveId, _currentBestValue);
        }

        public int minValue(int[] board, int alpha, int beta, int currentDepth, int maxDepth) {
            if (Thread.currentThread().isInterrupted()) {
                return -2000;
            }

            int i = 7;
            int bestValue = Integer.MAX_VALUE;
            int moveValue = 0;
            int[] newBoard;
            int killerMove = _killerMoves[currentDepth + _moveCount];
            int status = Owari.checkForWinner(board);
            int result = 0;

            if (status == Owari.STATE_P2_WIN) {
                return 100;
            } else if (status == Owari.STATE_P1_WIN) {
                return 300;
            } else if (status == Owari.STATE_TIED) {
                return 100;
            } else if (currentDepth == maxDepth) {
                return 200 - board[7] - board[8] - board[9] - board[10] - board[11] - board[12] - board[13];
            } else {
                try {
                    _readBuffer.position(0);
                    _writeBuffer.position(0);
                    _intBuffer.position(0);
                    _intBuffer.put(board);
                    _intBuffer.put(maxDepth);
                    _intBuffer.put(0);
                    _sc.write(_writeBuffer);
                    _sc.configureBlocking(true);
                    _sc.read(_readBuffer);
                    _sc.configureBlocking(false);

                    result = (_readBytes[0] - 48) * 100 + (_readBytes[1] - 48) * 10 + _readBytes[2] - 48;
                    if (result > 0) {
                        return result;
                    }


                    if (killerMove > -1) {
                        newBoard = Owari.makeMoveP2(killerMove, board);
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


                    for (i = 7; i < 14; ++i) {
                        if (i != killerMove) {
                            newBoard = Owari.makeMoveP2(i, board);
                            if (newBoard != null) {
                                moveValue = maxValue(newBoard, alpha, beta, currentDepth + 1, maxDepth);
                                if (moveValue < bestValue) {
                                    bestValue = moveValue;
                                }

                                if (bestValue <= alpha) {
                                    _writeBuffer.position(0);
                                    _intBuffer.position(14);
                                    _intBuffer.put(maxDepth);
                                    _intBuffer.put(bestValue);
                                    _sc.write(_writeBuffer);
                                    _killerMoves[currentDepth + _moveCount] = i;
                                    return bestValue;
                                }

                                if (bestValue < beta) {
                                    beta = bestValue;
                                }
                            }
                        }
                    }

                    _writeBuffer.position(0);
                    _intBuffer.position(14);
                    _intBuffer.put(maxDepth);
                    _intBuffer.put(bestValue);
                    _sc.write(_writeBuffer);
                } catch(IOException e) {
                    e.printStackTrace();
                }
                return bestValue;
            }
        }

        public int maxValue(int[] board, int alpha, int beta, int currentDepth, int maxDepth) {
            if (Thread.currentThread().isInterrupted()) {
                return -2000;
            }

            int i = 0;

            int bestValue = Integer.MIN_VALUE;
            int moveValue = 0;
            int[] newBoard;

            int status = Owari.checkForWinner(board);
            if (status == Owari.STATE_P2_WIN) {
                return 100;
            } else if (status == Owari.STATE_P1_WIN) {
                return 300;
            } else if (status == Owari.STATE_TIED) {
                return 200;
            } else if (currentDepth == maxDepth) {
                return 200 + board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6];
            } else {
                for (i = 0; i < 6; ++i) {
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
}