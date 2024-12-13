package org.example;

import com.opencsv.CSVReader;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.List;
import java.util.Objects;


public class EnemyData {
    File enemy;
    String[][] enemyArray;

    {
        try {
            enemy = new File(Objects.requireNonNull(Thread.currentThread().getContextClassLoader().getResource("t_unit.csv")).toURI());
        } catch (URISyntaxException e) {
            throw new RuntimeException(e);
        }
    }
    String csvFilePath = enemy.getPath();
    {
        try (
                CSVReader reader = new CSVReader(new FileReader(csvFilePath))) {
            List<String[]> records = reader.readAll();

            enemyArray = new String[records.size()][];

            for (int i = 0; i < records.size(); i++) {
                enemyArray[i] = records.get(i);
            }
        } catch (
                IOException e) {
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
