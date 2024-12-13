package org.example.library.forms;
import org.example.*;

import javax.swing.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

public class EnemyStatsGUI extends JFrame {
    protected JPanel contentPane;
    private JCheckBox thisIsCheckBox;
    private JCheckBox aTestCheckBox;
    private JTabbedPane tabbedPane1;
    private JRadioButton eTraitRB;
    private JRadioButton eTraitSwapRB;
    private JRadioButton eRandomTraitRB;
    private JRadioButton eStatsUnchangedRB;
    private JRadioButton eStatsRevelantRB;
    private JRadioButton eStatsRandomRB;
    private JButton openCSVFileButton;
    private JTabbedPane tabbedPane2;
    private JCheckBox redCheckBox;
    private JCheckBox floatingCheckBox;
    private JCheckBox blackCheckBox;
    private JCheckBox angelCheckBox;
    private JCheckBox metalCheckBox;
    private JCheckBox alienCheckBox;
    private JCheckBox zombieCheckBox;
    private JCheckBox relicCheckBox;
    private JCheckBox akuCheckBox;
    private JCheckBox traitlessCheckBox;
    private JTabbedPane tabbedPane3;
    private JCheckBox speedDecreaseCheckBox;
    private JCheckBox waveImmuneCheckBox;
    private JCheckBox waveBlockCheckBox;
    private JCheckBox surgeImmuneCheckBox;
    private JCheckBox surgeReflectCheckBox1;
    private JTextField textField1;
    private JTextField textField3;
    private JTextField textField4;
    private JTextField textField5;
    private JCheckBox speedIncreaseCheckBox;
    private JTextField textField6;
    private JTextField textField7;
    private JCheckBox knockbackIncreaseCheckBox;
    private JCheckBox burrowCheckBox;
    private JTextField textField8;
    private JCheckBox reviveCheckBox;
    private JTextField textField9;
    private JCheckBox savageBlowCheckBox;
    private JTextField textField10;
    private JCheckBox explosionCheckBox;
    private JTextField textField11;
    private JTextField textField12;
    private JTextField textField13;
    private JCheckBox slowCheckBox;
    private JTextField textField14;
    private JCheckBox freezeCheckBox;
    private JCheckBox weakenCheckBox;
    private JCheckBox lethalCheckBox;
    private JCheckBox strengthenCheckBox;
    private JCheckBox baseDestroyerCheckBox;
    private JTextField textField15;
    private JCheckBox knockbackCheckBox;
    private JCheckBox critCheckBox;
    private JTextField textField16;
    private JCheckBox waveCheckBox;
    private JCheckBox surgeCheckBox;
    private JCheckBox toxicCheckBox;
    private JCheckBox multihitCheckBox;
    private JTextField textField2;
    private JTextField textField17;
    private JCheckBox knockbackDecreaseCheckBox;
    private JCheckBox healthNerfCheckBox;
    private JTextField textField18;
    private JCheckBox sageCheckBox;
    private JTextField textField19;
    private JPanel enemies;
    private JPanel units;
    private JPanel misc;
    private JPanel enemyTraits;
    private JPanel enemyStats;
    private JPanel enemyAdvanced;
    private JPanel etraitsAdvanced;
    private JPanel eIncludedTraits;
    private JPanel eTraitAbilities;
    private JRadioButton unchangedRadioButton;
    private JRadioButton shuffledRadioButton;
    private JButton generateCSVFilesButton;
    private JCheckBox canRandomizeIntoSameCheckBox;

    //Enemy Stat Variables
    eVars eVar = new eVars();
    //Enemy Stats Array
    EnemyData baseArray = new EnemyData();
    String[][] eStatsArray = baseArray.getEnemyArray();

    //trait
    Randomize randomizeTrait = new Randomize();

    public EnemyStatsGUI() {

        //Button variables
        setContentPane(contentPane);

        //Enemies
        //Enemy Traits
        ButtonGroup eTraitG = new ButtonGroup();
        eTraitG.add(eTraitRB);
        eTraitG.add(eTraitSwapRB);
        eTraitG.add(eRandomTraitRB);

        //Enemy Stats
        ButtonGroup eStatsG = new ButtonGroup();
        eStatsG.add(eStatsUnchangedRB);
        eStatsG.add(eStatsRevelantRB);
        eStatsG.add(eStatsRandomRB);


        //Trait Checkboxes
        redCheckBox.addActionListener(e -> {
            Trait.setRed(redCheckBox.isSelected());
        });
        floatingCheckBox.addActionListener(e -> {
            Trait.setFloating(floatingCheckBox.isSelected());
        });
        blackCheckBox.addActionListener(e -> {
            Trait.setBlack(blackCheckBox.isSelected());
        });
        angelCheckBox.addActionListener(e -> {
            Trait.setAngel(angelCheckBox.isSelected());
        });
        metalCheckBox.addActionListener(e -> {
            Trait.setMetal(metalCheckBox.isSelected());
        });
        alienCheckBox.addActionListener(e -> {
            Trait.setAlien(alienCheckBox.isSelected());
        });
        zombieCheckBox.addActionListener(e -> {
            Trait.setZombie(zombieCheckBox.isSelected());
        });
        relicCheckBox.addActionListener(e -> {
            Trait.setRelic(relicCheckBox.isSelected());
        });
        akuCheckBox.addActionListener(e -> {
            Trait.setAku(akuCheckBox.isSelected());
        });
        traitlessCheckBox.addActionListener(e -> {
            Trait.setTraitless(traitlessCheckBox.isSelected());
        });

        //Trait Option Buttons
        eTraitRB.addActionListener(e -> {
//            trait.settUnchanged(eTraitRB.isSelected());
        });
        eTraitSwapRB.addActionListener(e -> {
            //           trait.settSwapped(eTraitSwapRB.isSelected());
        });
        eRandomTraitRB.addActionListener(e -> {
            //         trait.settRandom(eRandomTraitRB.isSelected());
        });


        //Generate the CSV Files with correct settings
        generateCSVFilesButton.addActionListener(e ->{
            try {
                new CreateFile().createEnemyCSV();
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        });
    }
}