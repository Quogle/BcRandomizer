package org.example;

import java.util.stream.Stream;
import java.util.ArrayList;

public class Trait {
    //Included Trait Flags
    private static boolean red = true;
    private static boolean floating = true;
    private static boolean black = true;
    private static boolean angel = true;
    private static boolean metal = false;
    private static boolean alien = true;
    private static boolean zombie = true;
    private static boolean relic = true;
    private static boolean aku = true;
    private static boolean white = true;

    public static ArrayList<Integer> selectedTraits = new ArrayList<Integer>();

    public static void selectedTraits() {
        selectedTraits.clear();
        selectedTraits.trimToSize();

        if(red) selectedTraits.add(eVars.red);
        if(floating) selectedTraits.add(eVars.floating);
        if(black) selectedTraits.add(eVars.black);
        if(angel) selectedTraits.add(eVars.angel);
        if(metal) selectedTraits.add(eVars.metal);
        if(alien) selectedTraits.add(eVars.alien);
        if(zombie) selectedTraits.add(eVars.zombie);
        if(relic) selectedTraits.add(eVars.relic);
        if(aku) selectedTraits.add(eVars.aku);
        if(white) selectedTraits.add(eVars.white);
    }



    public boolean getRed() {
        return red;
    }

    public static void setRed(boolean red) {
        Trait.red = red;
    }

    public boolean getFloating() {
        return floating;
    }

    public static void setFloating(boolean floating) {
        Trait.floating = floating;
    }

    public boolean getBlack() {
        return black;
    }

    public static void setBlack(boolean black) {
        Trait.black = black;
    }

    public boolean getAngel() {
        return angel;
    }

    public static void setAngel(boolean angel) {
        Trait.angel = angel;
    }

    public boolean getMetal() {
        return metal;
    }

    public static void setMetal(boolean metal) {
        Trait.metal = metal;
    }

    public boolean getAlien() {
        return alien;
    }

    public static void setAlien(boolean alien) {
        Trait.alien = alien;
    }

    public boolean getZombie() {
        return zombie;
    }

    public static void setZombie(boolean zombie) {
        Trait.zombie = zombie;
    }

    public boolean getRelic() {
        return relic;
    }

    public static void setRelic(boolean relic) {
        Trait.relic = relic;
    }

    public boolean getAku() {
        return aku;
    }

    public static void setAku(boolean aku) {
        Trait.aku = aku;
    }

    public boolean getTraitless() {
        return white;
    }

    public static void setTraitless(boolean traitless) {
        Trait.white = traitless;
    }

    public static ArrayList<Integer> getSelectedTraits() {
        return selectedTraits;
    }
}
