import to.richard.owari.GameEngine;
import to.richard.owari.ai.IComputerAi;
import to.richard.owari.ai.RandomPlayer;
import to.richard.owari.gui.*;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * Author: Richard To
 * Date: 10/11/13
 */
public class Pa3 {
    public static void main(String[] args) {
        IComputerAi ai = new RandomPlayer();
        GameEngine gameEngine = new GameEngine(ai);
    }
}
