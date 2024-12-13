package org.example;

import com.jtattoo.plaf.graphite.GraphiteLookAndFeel;

import javax.swing.*;
import java.awt.*;

public class SetGUI {
    public void setDarkGUI() {
        // Set global background color for consistency across components
        UIManager.put("Panel.background", new Color(45, 45, 45));   // Dark background for panels
        UIManager.put("Button.background", new Color(70, 70, 70));   // Dark button background
        UIManager.put("Label.background", new Color(45, 45, 45));    // Dark label background
        UIManager.put("TextField.background", new Color(45, 45, 45)); // Dark text field background
        UIManager.put("RadioButton.background", new Color(45, 45, 45)); // Dark background for RadioButton
        UIManager.put("RadioButton.select", new Color(100, 100, 100)); // Change selected color of RadioButton
        UIManager.put("RadioButton.foreground", new Color(236, 224, 212 ));// Change text color of RadioButton
        UIManager.put("TitledBorder.titleColor", new Color(236, 224, 212 ));  // Set title color to white for all JPanels
        UIManager.put("TextField.foreground", new Color(236, 224, 212 ));
        UIManager.put("TextField.caretForeground", new Color(236, 224, 212));

        try {
            UIManager.setLookAndFeel(new GraphiteLookAndFeel());

            UIManager.put("TabbedPane.background", new Color(10, 10, 10));  // Background for the entire tabbed pane
            UIManager.put("TabbedPane.foreground", new Color(250, 236, 226 ));  // Background for the entire tabbed pane

        } catch (UnsupportedLookAndFeelException e) {
            e.printStackTrace();
        }
    }
}
