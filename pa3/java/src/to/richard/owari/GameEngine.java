package to.richard.owari;

import to.richard.owari.ai.IComputerAi;
import to.richard.owari.ai.IMoveListener;
import to.richard.owari.gui.GameBoard;
import to.richard.owari.gui.IMoveHook;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * Author: Richard To
 * Date: 10/11/13
 */
public class GameEngine {
    protected int[] _board;
    protected GameBoard _gameBoard;
    protected int _playerTurn = Owari.CPU_PLAYER;
    protected IComputerAi _ai;

    public GameEngine(IComputerAi ai) {
        _ai = ai;
        _ai.setMoveListener(new MoveListener());
        _board = Owari.createBoard();
        _gameBoard = new GameBoard(_board, new HumanMoveHook());
        _gameBoard.addStartButtonListener(new StartButtonListener());
    }

    public void makeComputerMove() {
        _ai.makeMove(_board, _gameBoard.getDepth());
    }

    private class MoveListener implements IMoveListener {
        public void movePerformed(int move) {
            _board = Owari.makeMoveP1(move, _board);
            _gameBoard.displayMoveStatusP1(move).updateState(_board);
            int status = Owari.checkForWinner(_board);
            if (status < Owari.STATE_CONTINUE) {
                _gameBoard.displayEndGameStatus(status).endGame();
            } else {
                _gameBoard.displayTurnStatusP2().enableHumanMove(_board);
            }
        }
    }
    private class HumanMoveHook implements IMoveHook {
        public void movePerformed(int move) {
            _gameBoard.disableHumanMove();

            _board = Owari.makeMoveP2(move, _board);
            _gameBoard.displayMoveStatusP2(move).updateState(_board);

            int status = Owari.checkForWinner(_board);
            if (status < Owari.STATE_CONTINUE) {
                _gameBoard.displayEndGameStatus(status).endGame();
            } else {
                _gameBoard.displayTurnStatusP1();
                makeComputerMove();
            }
        }
    }

    private class StartButtonListener implements ActionListener {
        public void actionPerformed(ActionEvent event) {
            _gameBoard.startGame();
            _playerTurn = _gameBoard.getPlayerStart();
            if (_playerTurn == Owari.HUMAN_PLAYER) {
                _gameBoard.displayTurnStatusP2().enableHumanMove(_board);
            } else {
                _gameBoard.displayTurnStatusP1();
                makeComputerMove();
            }
        }
    }
}
