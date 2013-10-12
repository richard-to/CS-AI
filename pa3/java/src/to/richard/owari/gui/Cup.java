package to.richard.owari.gui;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * Author: Richard To
 * Date: 10/11/13
 */
public class Cup extends JPanel {
    private static final String DEFAULT_SEEDS = "0";
    private JButton _button;
    private int _id;
    private IMoveHook _hook;

    public Cup(int id) {
        init(id, 0);
    }

    public Cup(int id, int seeds) {
        init(id, seeds);
    }

    private void init(int id, int seeds) {
        setLayout(new GridLayout(1, 1));
        _id = id;
        _button = new JButton(Integer.toString(seeds));
        _button.setEnabled(false);
        _button.addActionListener(new CupActionListener());
        add(_button);
    }

    public void setEnabled(boolean enabled) {
        _button.setEnabled(enabled);
    }

    public Cup setSeeds(int seeds) {
        _button.setText(Integer.toString(seeds));
        return this;
    }

    public Cup setMoveHook(IMoveHook hook) {
        _hook = hook;
        return this;
    }

    private class CupActionListener implements ActionListener {
        public void actionPerformed(ActionEvent event) {
            if (_hook != null) {
                _hook.movePerformed(_id);
            }
        }
    }
}
