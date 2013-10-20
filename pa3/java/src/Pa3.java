import to.richard.owari.GameEngine;
import to.richard.owari.Owari;
import to.richard.owari.ai.*;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

/**
 * Author: Richard To
 * Date: 10/11/13
 */
public class Pa3 {
    public static final boolean USE_CACHE_PLAYER = false;

    public static final String CONFIG = "db.properties";
    public static final String CONFIG_PROP_CONN_STRING = "connection_string";

    public static void main(String[] args) {
        if (USE_CACHE_PLAYER) {
            runAlphaBetaCachePlayer();
        } else {
            IComputerAi ai = new AlphaBetaPlayerID();
            GameEngine gameEngine = new GameEngine(ai);
        }
    }

    public static void runAlphaBetaCachePlayer() {
        Properties prop = new Properties();
        String connectionString = null;
        try {
            prop.load(new FileInputStream(CONFIG));
            connectionString = prop.getProperty(CONFIG_PROP_CONN_STRING);
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        IComputerAi ai = new AlphaBetaCachePlayer(connectionString);
        GameEngine gameEngine = new GameEngine(ai);
    }
}
