package to.richard.owari.gui;

import javax.swing.*;
import java.awt.*;

/**
 * Author: Richard To
 * Date: 10/11/13
 */
public class Cup extends JPanel {
    private JButton _button;
    public Cup(int seeds) {
        setLayout(new GridLayout(1, 1));
        _button = new JButton(Integer.toString(seeds));
        add(_button);
    }
}
