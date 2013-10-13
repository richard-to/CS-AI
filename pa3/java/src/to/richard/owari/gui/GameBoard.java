package to.richard.owari.gui;

import to.richard.owari.Owari;

import javax.swing.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

/**
 * Author: Richard To
 * Date: 10/11/13
 */
public class GameBoard extends JFrame {

    public static final String TITLE = "Owari";
    public static final int WIDTH = 640;
    public static final int HEIGHT = 480;

    public static final String BLANK = "";
    public static final String P1_NAME = "Computer";
    public static final String P2_NAME = "Human";
    public static final String STATUS_GAME_START = "Game starting...\n";
    public static final String STATUS_PLAYER_TURN = "%s player's turn.\n";
    public static final String STATUS_DEPTH_CHANGED = "Depth changed to %d.\n";
    public static final String STATUS_MOVE_TIME = "Computer move took %.3f seconds\n";
    public static final String STATUS_MOVE = "Move %d: %s player selected cup %d.\n";
    public static final String STATUS_WIN = "You won!\n";
    public static final String STATUS_LOST = "You lost!\n";
    public static final String STATUS_TIED = "You tied!\n";

    public static final String START_BUTTON_TEXT = "Start Game";
    public static final String[] OPTION_TURN = {"Computer Goes First", "Human Goes First"};

    public static final int DEPTH_MIN = 0;
    public static final int DEPTH_MAX = 100;
    public static final int DEPTH_DEFAULT = 15;
    public static final int DEPTH_MAJOR_TICK = 5;
    public static final int DEPTH_MINOR_TICK = 1;

    private ArrayList<Cup> _cups;

    private JScrollPane _scrollPane;
    private JTextArea _infoTextarea;
    private JComboBox _turnComboBox;
    private JButton _startButton;
    private JSlider _depthSlider;

    public GameBoard(int[] board, IMoveHook moveHook) {
        _cups = new ArrayList<Cup>();
        for (int i = 0; i < Owari.NUM_CUPS; i++) {
            _cups.add(new Cup(i, board[i]));
        }

        Panel p1Pane = new Panel();
        p1Pane.setLayout(new GridLayout(1, Owari.CUPS_EACH));
        for (int i = Owari.P1_CUPS[0]; i <= Owari.P1_CUPS[1]; i++) {
            Cup cup = _cups.get(i);
            p1Pane.add(cup);
        }

        Panel p2Pane = new Panel();
        p2Pane.setLayout(new GridLayout(1, Owari.CUPS_EACH));
        for (int i = Owari.P2_CUPS[1]; i >= Owari.P2_CUPS[0]; i--) {
            Cup cup = _cups.get(i);
            cup.setMoveHook(moveHook);
            p2Pane.add(cup);
        }

        Cup p2GoalCup = _cups.get(Owari.P2_GOAL);
        Cup p1GoalCup = _cups.get(Owari.P1_GOAL);

        JPanel goalPane = new JPanel();
        goalPane.setLayout(new GridLayout(1, 2));
        goalPane.add(p2GoalCup);
        goalPane.add(p1GoalCup);

        _infoTextarea = new JTextArea();
        _infoTextarea.setEditable(false);
        _infoTextarea.setRows(8);
        _scrollPane = new JScrollPane(
                _infoTextarea,
                JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
                JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        JPanel optionsPane = new JPanel();
        optionsPane.setLayout(new FlowLayout());

        _turnComboBox = new JComboBox(OPTION_TURN);
        optionsPane.add(_turnComboBox);

        _startButton = new JButton(START_BUTTON_TEXT);

        optionsPane.add(_startButton);

        _depthSlider = new JSlider(JSlider.HORIZONTAL,
                DEPTH_MIN, DEPTH_MAX, DEPTH_DEFAULT);
        _depthSlider.addChangeListener(new DepthChangeListener());
        _depthSlider.setMajorTickSpacing(DEPTH_MAJOR_TICK);
        _depthSlider.setMinorTickSpacing(DEPTH_MINOR_TICK);
        _depthSlider.setPaintTicks(true);
        _depthSlider.setPaintLabels(true);

        JPanel mainPane = new JPanel();
        mainPane.setLayout(new BoxLayout(mainPane, BoxLayout.Y_AXIS));
        mainPane.add(p2Pane);
        mainPane.add(goalPane);
        mainPane.add(p1Pane);
        mainPane.add(_scrollPane);

        Container contentPane = getContentPane();
        contentPane.setLayout(new BorderLayout(0, 0));
        contentPane.add(optionsPane, BorderLayout.NORTH);
        contentPane.add(mainPane, BorderLayout.CENTER);
        contentPane.add(_depthSlider, BorderLayout.SOUTH);

        setTitle(TITLE);
        setSize(WIDTH, HEIGHT);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }

    public GameBoard addStartButtonListener(ActionListener listener) {
        _startButton.addActionListener(listener);
        return this;
    }

    public GameBoard startGame() {
        _infoTextarea.append(STATUS_GAME_START);
        _startButton.setEnabled(false);
        _turnComboBox.setEnabled(false);
        return this;
    }

    public GameBoard endGame() {
        _depthSlider.setEnabled(false);
        return this;
    }

    public GameBoard setDepth(int depth) {
        _depthSlider.setValue(depth);
        return this;
    }

    public int getDepth() {
        return _depthSlider.getValue();
    }

    public int getPlayerStart() {
        int index = _turnComboBox.getSelectedIndex();
        return index;
    }

    public GameBoard disableHumanMove() {
        for (int i = Owari.P2_CUPS[1]; i >= Owari.P2_CUPS[0]; --i) {
            _cups.get(i).setEnabled(false);
        }
        return this;
    }

    public GameBoard enableHumanMove(int[] board) {
        for (int i = Owari.P2_CUPS[1]; i >= Owari.P2_CUPS[0]; --i) {
            if (board[i] > 0) {
                _cups.get(i).setEnabled(true);
            }
        }
        return this;
    }

    public GameBoard updateState(int[] board) {
        for (int i = 0; i < Owari.NUM_CUPS; ++i) {
            _cups.get(i).setSeeds(board[i]);
        }
        revalidate();
        repaint();
        return this;
    }

    public GameBoard clearStatus() {
        _infoTextarea.setText(BLANK);
        return this;
    }

    public GameBoard scrollGameLogToBottom() {
        JScrollBar vertical = _scrollPane.getVerticalScrollBar();
        vertical.setValue(vertical.getMaximum());
        return this;
    }

    public GameBoard displayMoveStatusP1(int moveCount, int move) {
        _infoTextarea.append(String.format(STATUS_MOVE, moveCount, P1_NAME, move));
        scrollGameLogToBottom();
        return this;
    }

    public GameBoard displayMoveStatusP2(int moveCount, int move) {
        _infoTextarea.append(String.format(STATUS_MOVE, moveCount, P2_NAME, move));
        scrollGameLogToBottom();
        return this;
    }

    public GameBoard displayTurnStatusP2() {
        _infoTextarea.append(String.format(STATUS_PLAYER_TURN, P2_NAME));
        scrollGameLogToBottom();
        return this;
    }

    public GameBoard displayTurnStatusP1() {
        _infoTextarea.append(String.format(STATUS_PLAYER_TURN, P1_NAME));
        scrollGameLogToBottom();
        return this;
    }

    public GameBoard displayMoveTime(double time) {
        _infoTextarea.append(String.format(STATUS_MOVE_TIME, time));
        scrollGameLogToBottom();
        return this;
    }

    public GameBoard displayEndGameStatus(int status) {
        String statusText = STATUS_WIN;
        if (status == Owari.STATE_LOST) {
            statusText = STATUS_LOST;
        } else if (status == Owari.STATE_TIED) {
            statusText = STATUS_TIED;
        }
        _infoTextarea.append(statusText);
        scrollGameLogToBottom();
        return this;
    }

    public GameBoard displayDepthChangedStatus() {
        _infoTextarea.append(String.format(STATUS_DEPTH_CHANGED, _depthSlider.getValue()));
        scrollGameLogToBottom();
        return this;
    }

    private class DepthChangeListener implements ChangeListener {
        public void stateChanged(ChangeEvent e) {
            if (!_depthSlider.getValueIsAdjusting() && _startButton.isEnabled() == false) {
                displayDepthChangedStatus();
            }
        }
    }
}
