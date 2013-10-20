package to.richard.owari.ai;

/**
 * Author: Richard To
 * Date: 10/11/13
 */
public interface IComputerAi {
    public void setMoveListener(IMoveListener listener);
    public void makeMove(int[] board, int depth, int moveCount);
    public double getElapsedTime();
}
