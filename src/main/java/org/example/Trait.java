package org.example;

import java.util.stream.Stream;
import java.util.ArrayList;

public class Trait {
    //Included Trait Flags
    private boolean red;
    private boolean floating;
    private boolean black;
    private boolean angel;
    private boolean metal;
    private boolean alien;
    private boolean zombie;
    private boolean relic;
    private boolean aku;
    private boolean white;

    public ArrayList<Integer> selectedTraits = new ArrayList<Integer>();

    public void selectedTraits() {

        if (red) selectedTraits.add(eVars.red);
        if (floating) selectedTraits.add(eVars.floating);
        if (black) selectedTraits.add(eVars.black);
        if (angel) selectedTraits.add(eVars.angel);
        if (metal) selectedTraits.add(eVars.metal);
        if (alien) selectedTraits.add(eVars.alien);
        if (zombie) selectedTraits.add(eVars.zombie);
        if (relic) selectedTraits.add(eVars.relic);
        if (aku) selectedTraits.add(eVars.aku);
        if (white) selectedTraits.add(eVars.white);
    }



    public boolean getRed() {
        return red;
    }

    public void setRed(boolean red) {
        this.red = red;
    }

    public boolean getFloating() {
        return floating;
    }

    public void setFloating(boolean floating) {
        this.floating = floating;
    }

    public boolean getBlack() {
        return black;
    }

    public void setBlack(boolean black) {
        this.black = black;
    }

    public boolean getAngel() {
        return angel;
    }

    public void setAngel(boolean angel) {
        this.angel = angel;
    }

    public boolean getMetal() {
        return metal;
    }

    public void setMetal(boolean metal) {
        this.metal = metal;
    }

    public boolean getAlien() {
        return alien;
    }

    public void setAlien(boolean alien) {
        this.alien = alien;
    }

    public boolean getZombie() {
        return zombie;
    }

    public void setZombie(boolean zombie) {
        this.zombie = zombie;
    }

    public boolean getRelic() {
        return relic;
    }

    public void setRelic(boolean relic) {
        this.relic = relic;
    }

    public boolean getAku() {
        return aku;
    }

    public void setAku(boolean aku) {
        this.aku = aku;
    }

    public boolean getTraitless() {
        return white;
    }

    public void setTraitless(boolean traitless) {
        this.white = traitless;
    }

    public ArrayList<Integer> getSelectedTraits() {
        return selectedTraits;
    }
}
