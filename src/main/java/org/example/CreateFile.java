package org.example;

import com.opencsv.CSVWriter;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class CreateFile {
    File eCSV = new File("src/main/DownloadLocal/t_unit.csv");
    FileWriter outputFile = new FileWriter(eCSV);
    Randomize random = new Randomize();
    eVars trait = new eVars();

    public CreateFile() throws IOException {
    }

    public void createEnemyCSV() throws IOException {
        random.RandomizeTraits();
        String[][] eStatsArray = random.geteStatsArray();

        for(int column = 0; column < eStatsArray.length; ++column) {
            for(int row = 0; row < eStatsArray[0].length; row++) {
                outputFile.write(eStatsArray[column][row]);
                if (row < eStatsArray[0].length - 1) {
                    outputFile.write(",");
                }
            }
            outputFile.write("\n");
        }
        outputFile.flush();

        File debug = new File("src/main/DownloadLocal/debug.txt");
        FileWriter debugFile = new FileWriter(debug);

        for(int column = 0; column < eStatsArray.length; ++column) {
                debugFile.write(column + ": ");
                if(eStatsArray[column][eVars.red] == "1") {
                    debugFile.write("Red");
                }if(eStatsArray[column][eVars.floating] == "1") {
                    debugFile.write("Floating");
                }if(eStatsArray[column][eVars.black] == "1") {
                    debugFile.write("Black");
                }if(eStatsArray[column][eVars.angel] == "1") {
                    debugFile.write("Angel");
                }if(eStatsArray[column][eVars.metal] == "1") {
                    debugFile.write("Metal");
                }if(eStatsArray[column][eVars.alien] == "1") {
                    debugFile.write("Alien");
                }if(eStatsArray[column][eVars.zombie] == "1") {
                    debugFile.write("Zombie");
                }if(eStatsArray[column][eVars.relic] == "1") {
                    debugFile.write("Relic");
                }if(eStatsArray[column][eVars.aku] == "1") {
                    debugFile.write("Aku");
                }if(eStatsArray[column][eVars.white] == "1") {
                    debugFile.write("White");
            }
            debugFile.write("\n");
        }
        debugFile.flush();
    }

}
