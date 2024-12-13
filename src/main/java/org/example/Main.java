package org.example;

import org.example.library.forms.EnemyStatsGUI;

import javax.swing.*;

// Press Shift twice to open the Search Everywhere dialog and type `show whitespaces`,
// then press Enter. You can now see whitespace characters in your code.
public abstract class Main {

    public static void main(String[] args) {

        //Enemy Stat Variables
        eVars eStat = new eVars();
        //Enemy Stats Array
        EnemyData baseArray = new EnemyData();
        String[][] eStatsArray = baseArray.getEnemyArray();

        //make UI Dark mode
        new SetGUI().setDarkGUI();

        //Launch GUI
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                EnemyStatsGUI enemyStatsGUI  = new EnemyStatsGUI();
                enemyStatsGUI.setTitle("The Battle Cats Randomizer");
                enemyStatsGUI.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

                // Ensure proper size and layout
                enemyStatsGUI.pack();  // Adjust size based on components
                enemyStatsGUI.setVisible(true);  // Make the frame visible
            }
        });

    }

}