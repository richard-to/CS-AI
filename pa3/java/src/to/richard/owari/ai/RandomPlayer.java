package to.richard.owari.ai;

import to.richard.owari.Owari;

import java.util.ArrayList;
import java.util.Random;

/**
 * Author: Richard To
 * Date: 10/11/13
 */
public class RandomPlayer implements IComputerAi {
    private Random _rand;

    public RandomPlayer() {
        _rand = new Random();
    }

    public int makeMove(int[] board, int depth) {
        ArrayList<Integer> moves = new ArrayList<Integer>();
        for (int i = Owari.P1_CUPS[0]; i <= Owari.P1_CUPS[1]; ++i) {
            if (board[i] > 0) {
                moves.add(i);
            }
        }
        return moves.get(_rand.nextInt(moves.size()));
    }
}
