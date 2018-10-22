package io;

import java.io.File;
import java.io.FileNotFoundException;

import sequence.Queue;
import sequence.Sequence;

public class Scanner {

	/*
	 * Scanner may not have been the best choice in names, but it does what is needed and returns the right objects.
	 */
	
    Queue<String> words;
    boolean sentMode;
    java.util.Scanner scanner;

    public Scanner() {

    }
    
    public Scanner(String path) throws FileNotFoundException {
    	openFile(path);
    	sentMode = false;
    }
    
    public Scanner(String path, boolean s) throws FileNotFoundException {
    	openFile(path);
    	sentMode = s;
    }
    
    
    public void openFile(String path) throws FileNotFoundException {
    	scanner = new java.util.Scanner(new File(path));
    }

    
    public void set(String path, boolean s) throws FileNotFoundException {
    	openFile(path);
    	sentMode = s;
    }
    
    public boolean moreSentences() {
    	return this.scanner.hasNext();
    }
    
    /*
     * Reads in a line, splits it, and puts it into a STSentence object
     */
    public Sequence nextSentence() {
    	Sequence sentence = new Sequence();
    	String line = scanner.nextLine().trim();
    	if (!line.isEmpty()){
    		String[] sline = line.split(" ");
	    	for (int i=0; i<sline.length; i++) {
	    		sentence.pushBack(sline[i].trim());
	    	}
	    	
	    	return sentence;
    	}
    	return null;
    }
    
    public void close() {
    	scanner.close();
    }
    

    
}
