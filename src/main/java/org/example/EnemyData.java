package org.example;

import com.opencsv.CSVReader;

import java.io.*;
import java.net.URISyntaxException;
import java.util.List;
import java.util.Objects;


public class EnemyData {
    String[][] enemyArray;

    // Load resource as InputStream
    {
        try (InputStream inputStream = Objects.requireNonNull(Thread.currentThread().getContextClassLoader().getResourceAsStream("t_unit.csv"));
             CSVReader reader = new CSVReader(new InputStreamReader(inputStream))) {

            List<String[]> records = reader.readAll();

            enemyArray = new String[records.size()][];

            for (int i = 0; i < records.size(); i++) {
                enemyArray[i] = records.get(i);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String[][] getEnemyArray() {
        return enemyArray;
    }

    public int getRowSize() {
        return enemyArray[0].length;
    }

    public int getColumnSize() {
        return enemyArray.length;
    }
}