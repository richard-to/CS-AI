import to.richard.owari.GameEngine;
import to.richard.owari.ai.AlphaBetaPlayer;
import to.richard.owari.ai.IComputerAi;
import to.richard.owari.ai.MinimaxPlayer;

/**
 * Author: Richard To
 * Date: 10/11/13
 */
public class Pa3 {
    public static void main(String[] args) {
        IComputerAi ai = new AlphaBetaPlayer();
        GameEngine gameEngine = new GameEngine(ai);
    }
}
