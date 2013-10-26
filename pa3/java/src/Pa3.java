import to.richard.owari.GameEngine;
import to.richard.owari.ai.*;

import java.io.FileInputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.channels.SocketChannel;
import java.util.Properties;

/**
 * Author: Richard To
 * Date: 10/11/13
 */
public class Pa3 {
    public static final int CACHE_SOCKET_PORT = 5007;

    public static final String CONFIG = "db.properties";
    public static final String CONFIG_PROP_CONN_STRING = "connection_string";

    public static void main(String[] args) throws IOException {
        //runNormal();
        //runThreaded();
        runWithIterativeDeepening();
    }

    public static void runNormal() {
        IComputerAi ai = new AlphaBetaPlayer();
        GameEngine gameEngine = new GameEngine(ai);
    }

    public static void runThreaded() {
        IComputerAi ai = new AlphaBetaPlayerThreaded();
        GameEngine gameEngine = new GameEngine(ai);
    }

    public static void runWithIterativeDeepening() {
        IComputerAi ai = new AlphaBetaPlayerID();
        GameEngine gameEngine = new GameEngine(ai);
    }

    public static void runWithTranspositionTable() throws IOException {
        SocketChannel[] scs = new SocketChannel[6];
        for (int i = 0; i < scs.length; i++) {
            SocketChannel sc = null;
            sc = SocketChannel.open();
            sc.configureBlocking(false);
            sc.connect(new InetSocketAddress(5007));
            while (!sc.finishConnect()) {
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            scs[i] = sc;
        }

        IComputerAi ai = new AlphaBetaPlayerTT(scs);
        GameEngine gameEngine = new GameEngine(ai);
    }

    public static void runWithSqlLiteCache() {
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
