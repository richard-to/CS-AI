package to.richard.owari.ai;

/**
 * Author: Richard To
 * Date: 10/12/13
 */
public abstract class Player implements IComputerAi {
    protected IMoveListener _listener;
    public void setMoveListener(IMoveListener listener) {
        _listener = listener;
    }
}
