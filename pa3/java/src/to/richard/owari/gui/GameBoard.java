package to.richard.owari.gui;

import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;

/**
 * Author: Richard To
 * Date: 10/11/13
 */
public class GameBoard extends JFrame {

    public static final String TITLE = "Owari";
    public static final int WIDTH = 550;
    public static final int HEIGHT = 300;
    public static final int SEEDS = 3;
    public static final int GOAL_SEEDS = 0;
    public static final int NUM_CUPS = 14;
    public static final int CUPS_PER_PLAYER = 6;
    public static final int[] PLAYER1_CUPS = {0, 5};
    public static final int PLAYER1_GOAL = 6;
    public static final int[] PLAYER2_CUPS = {7, 12};
    public static final int PLAYER2_GOAL = 13;
    public static final int DEFAULT_DEPTH = 5;

    private ArrayList<Cup> _cups;
    private JTextArea _infoTextarea;
    private JTextField _depthTextField;
    public GameBoard() {
        _cups = new ArrayList<Cup>();

        Panel player1Cups = new Panel();
        player1Cups.setLayout(new GridLayout(1, CUPS_PER_PLAYER));
        for (int i = 0; i < CUPS_PER_PLAYER; i++) {
            Cup cup = new Cup(SEEDS);
            player1Cups.add(cup);
            _cups.add(cup);
        }

        JPanel goalCups = new JPanel();
        goalCups.setLayout(new GridLayout(1, 2));
        Cup player1GoalCup = new Cup(GOAL_SEEDS);
        player1GoalCup.setEnabled(false);
        _cups.add(player1GoalCup);
        goalCups.add(player1GoalCup);

        Panel player2Cups = new Panel();
        player2Cups.setLayout(new GridLayout(1, CUPS_PER_PLAYER));
        for (int i = 0; i < CUPS_PER_PLAYER; i++) {
            Cup cup = new Cup(SEEDS);
            player2Cups.add(cup);
            _cups.add(cup);
        }

        Cup player2GoalCup = new Cup(GOAL_SEEDS);
        player2GoalCup.setEnabled(false);
        _cups.add(player2GoalCup);
        goalCups.add(player2GoalCup);

        _infoTextarea = new JTextArea();
        _infoTextarea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(
                _infoTextarea,
                JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
                JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);

        JPanel optionsPane = new JPanel();
        optionsPane.setLayout(new FlowLayout());

        String[] values = {"Computer", "Human"};
        JComboBox comboBox = new JComboBox(values);
        JLabel depthLabel = new JLabel("Depth");
        depthLabel.setHorizontalAlignment(SwingConstants.RIGHT);
        optionsPane.add(depthLabel);

        _depthTextField = new JTextField(DEFAULT_DEPTH);
        optionsPane.add(_depthTextField);
        JLabel turnLabel = new JLabel("Player Turn");
        turnLabel.setHorizontalAlignment(SwingConstants.RIGHT);
        optionsPane.add(turnLabel);
        optionsPane.add(comboBox);
        optionsPane.add(new JButton("Start Game"));


        JPanel mainPane = new JPanel();
        mainPane.setLayout(new BoxLayout(mainPane, BoxLayout.Y_AXIS));
        mainPane.add(player1Cups);
        mainPane.add(goalCups);
        mainPane.add(player2Cups);
        mainPane.add(scrollPane);

        Container contentPane = getContentPane();
        contentPane.setLayout(new BorderLayout(0, 0));
        contentPane.add(optionsPane, BorderLayout.NORTH);
        contentPane.add(mainPane, BorderLayout.CENTER);

        setTitle(TITLE);
        setSize(WIDTH, HEIGHT);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }
}
