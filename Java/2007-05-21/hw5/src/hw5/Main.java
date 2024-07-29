package hw5;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.InputMismatchException;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;
import java.util.logging.StreamHandler;

public class Main {
    public static void main(String... args) {
        Logger.getLogger(Logger.GLOBAL_LOGGER_NAME).addHandler(
                new StreamHandler(System.err, new SimpleFormatter()));
        
        // read 10 integers from the console
        System.out.println("Enter 10 integers: ");
        final List<Integer> inputData = new ArrayList<Integer>(10);
        while (inputData.size() < 10) {
            Scanner scanner = null;
            try {
                scanner = new Scanner(System.console().readLine());
                while(scanner.hasNextInt() && inputData.size() < 10)
                    inputData.add(scanner.nextInt());
            } finally {
                if(scanner != null)
                    scanner.close();
            }
        }
        
        // write the ints to a file
        final String filename = "input.txt";
        PrintWriter printWriter = null;
        try {
            printWriter = new PrintWriter(filename);
            for(int i: inputData)
                printWriter.println(i);
        } catch (final FileNotFoundException ex) {
            Logger.getLogger(Logger.GLOBAL_LOGGER_NAME)
                    .log(Level.SEVERE, "Can't open file", ex);
        } finally {
            if(printWriter != null)
                printWriter.close();
        }
        
        // read the data from the file again
        final List<Integer> fileData = new ArrayList<Integer>(10);
        Scanner scanner = null;
        try {
            scanner = new Scanner(new BufferedReader(
                    new FileReader(filename)));
            for(int i = 0; i < 10; i++)
                fileData.add(scanner.nextInt());
        } catch (final FileNotFoundException ex) {
            Logger.getLogger(Logger.GLOBAL_LOGGER_NAME)
                    .log(Level.SEVERE, "Can't open file", ex);
        } catch (final InputMismatchException ex) {
            Logger.getLogger(Logger.GLOBAL_LOGGER_NAME)
                    .log(Level.SEVERE, "Incorrect format", ex);
        } catch (final NoSuchElementException ex) {
            Logger.getLogger(Logger.GLOBAL_LOGGER_NAME)
                    .log(Level.SEVERE, "File too short", ex);
        } finally {
            if(scanner != null)
                scanner.close();
        }
        
        // sort the array in increasing order
        Collections.sort(fileData);
        
        // write the data into a text file
        final String sortedFilename = "output.txt";
        PrintWriter sortedPrintWriter = null;
        try {
            sortedPrintWriter = new PrintWriter(sortedFilename);
            for(int i: fileData)
                sortedPrintWriter.println(i);
        } catch (final FileNotFoundException ex) {
            Logger.getLogger(Logger.GLOBAL_LOGGER_NAME)
                    .log(Level.SEVERE, "Can't open file", ex);
        } finally {
            if(sortedPrintWriter!=null)
                sortedPrintWriter.close();
        }
        
        // print the data onto the console
        System.out.println(fileData);
    }
}
