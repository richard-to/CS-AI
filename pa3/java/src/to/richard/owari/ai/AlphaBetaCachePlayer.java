package to.richard.owari.ai;

import to.richard.owari.Owari;

import java.sql.*;
import java.util.Arrays;
import java.util.HashMap;

/**
 * Author: Richard To
 * Date: 10/12/13
 */
public class AlphaBetaCachePlayer extends Player {
    public static final String INSERT_SQL = "INSERT INTO owari_cache (state, outcome) VALUE(?, ?)";
    public static final String SELECT_SQL = "SELECT state, outcome FROM owari_cache";

    protected Connection _conn;
    protected HashMap<String, Integer> _cache;

    public AlphaBetaCachePlayer(String connectionString) {
        try {
            _conn = DriverManager.getConnection(connectionString);
            _cache = new HashMap<String, Integer>();
            loadCache();
        } catch (SQLException ex) {
            System.out.println("SQLException: " + ex.getMessage());
            System.out.println("SQLState: " + ex.getSQLState());
            System.out.println("VendorError: " + ex.getErrorCode());
        }
    }

    protected void loadCache() {
        Statement stmt = null;
        ResultSet rs = null;
        try {
            stmt = _conn.createStatement();
            rs = stmt.executeQuery(SELECT_SQL);
            while (rs.next()) {
                _cache.put(rs.getString(1), rs.getInt(2));
            }
        } catch (SQLException ex) {
        } finally {
            if (rs != null) {
                try {
                    rs.close();
                } catch (SQLException sqlEx) { }
                rs = null;
            }

            if (stmt != null) {
                try {
                    stmt.close();
                } catch (SQLException sqlEx) { }
                stmt = null;
            }
        }
    }

    protected int checkCache(int[] board) {
        String key = Arrays.toString(board);
        if (_cache.containsKey(key)) {
            return _cache.get(key);
        }
        return 1000;
    }

    protected void saveCache(int[] board, int score) {
        String key = Arrays.toString(board);
        if (_cache.containsKey(key)) {
            return;
        }
        PreparedStatement stmt = null;
        try {
            stmt = _conn.prepareStatement(INSERT_SQL);
            stmt.clearParameters();
            stmt.setObject(1, key);
            stmt.setObject(2, score);
            stmt.executeUpdate();
            _cache.put(key, score);
        } catch (SQLException ex) {

        } finally {
            if (stmt != null) {
                try {
                    stmt.close();
                } catch (SQLException sqlEx) { }
                stmt = null;
            }
        }
    }

    public void makeMove(int[] board, int depth) {
        _startTime = System.currentTimeMillis();
        _elapsed = 0;

        int currentDepth = 0;
        int bestValue = Integer.MAX_VALUE;
        int bestMove = 0;

        int alpha = Integer.MIN_VALUE;
        int beta = Integer.MAX_VALUE;
        int moveValue = 0;
        int[] newBoard;
        int[] bestBoard = null;
        for (int i = 0; i < 6; ++i) {
            newBoard = Owari.makeMoveP1(i, board);
            if (newBoard != null) {
                if (newBoard != null) {
                    moveValue = minValue(newBoard, alpha, beta, currentDepth, depth);
                    if (moveValue > bestValue) {
                        bestBoard = newBoard;
                        bestValue = moveValue;
                        bestMove = i;
                    }
                }
            }
        }
        _elapsed = System.currentTimeMillis() - _startTime;
        saveCache(bestBoard, bestValue);
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
            return (board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6]) -
                    (board[7] + board[8] + board[9] + board[10] + board[11] + board[12] + board[13]);
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
            return (board[0] + board[1] + board[2] + board[3] + board[4] + board[5] + board[6]) -
                    (board[7] + board[8] + board[9] + board[10] + board[11] + board[12] + board[13]);
        } else {
            int cachedMoveValue = checkCache(board);
            if (cachedMoveValue != 1000) {
                return cachedMoveValue;
            } else {
                int bestValue = Integer.MIN_VALUE;
                int moveValue = 0;
                int[] newBoard = null;
                int[] bestBoard = null;
                for (int i = 0; i < 6; ++i) {
                    newBoard = Owari.makeMoveP1(i, board);
                    if (newBoard != null) {
                        moveValue = minValue(newBoard, alpha, beta, currentDepth + 1, maxDepth);
                        if (moveValue > bestValue) {
                            bestValue = moveValue;
                            bestBoard = newBoard;
                        }

                        if (bestValue >= beta) {
                            saveCache(newBoard, bestValue);
                            return bestValue;
                        }

                        if (bestValue > alpha) {
                            alpha = bestValue;
                        }
                    }
                }
                saveCache(bestBoard, bestValue);
                return bestValue;
            }
        }
    }
}