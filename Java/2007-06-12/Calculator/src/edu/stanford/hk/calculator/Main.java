/*
 * Main.java
 * 
 * Created on Jun 12, 2007, 2:20:11 PM
 * 
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package edu.stanford.hk.calculator;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

/**
 *
 * @author hk
 */
public class Main {

    /** Creates a new instance of Main */
    public Main() {
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        final JFrame frame = new CalculatorJFrame();
        frame.setTitle("Calculator");
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                frame.setVisible(true);
            }
        });
    }
}
