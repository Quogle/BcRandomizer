package org.example;

import java.util.Objects;


public class Randomize {


    //Enemy Stat Variables
    eVars eVar = new eVars();
    //Enemy Stats Array
    EnemyData baseArray = new EnemyData();
    String[][] eStatsArray = baseArray.getEnemyArray();
    //trait
    Trait trait = new Trait();

    public void RandomizeTraits() {
        //remove base trait from array if Can Randomize into Same Trait is not selected
        for(int column = 0; column < baseArray.getColumnSize(); column++) {
            trait.selectedTraits(); //reset valid trait array
            int newTraitAmount = 0; // reset new trait amount
            for(int pos = 0; pos < eVar.allTraits.length; pos++) {
                if (Objects.equals(eStatsArray[column][eVar.allTraits[pos]], "1")) {
                    int varValue = eVar.allTraits[pos];
                    trait.getSelectedTraits().remove(Integer.valueOf(varValue)); //remove original trait from array
                    eStatsArray[column][eVar.allTraits[pos]] = "0"; //remove original trait from enemy
                    newTraitAmount++;
                }
            }
            //Add new traits depending on number of old traits
            for (int i = 0; i < newTraitAmount; i++) {
                int newTraitPosition = (int) (Math.random() * (trait.getSelectedTraits().size())); //get new random trait
                eStatsArray[column][trait.selectedTraits.get(newTraitPosition)] = "1"; //sets the new trait
            }
        }
    }

    public String[][] geteStatsArray() {
        return eStatsArray;
    }
}
