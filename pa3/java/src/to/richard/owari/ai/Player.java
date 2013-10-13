package to.richard.owari.ai;

/**
 * Author: Richard To
 * Date: 10/12/13
 */
public abstract class Player implements IComputerAi {
    public static final double MILLIS_IN_SEC = 1000.0;

    protected IMoveListener _listener;
    protected long _startTime;
    protected long _elapsed;

    public void setMoveListener(IMoveListener listener) {
        _listener = listener;
    }

    public double getElapsedTime() {
        return _elapsed / MILLIS_IN_SEC;
    }
}
