package sequence;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.Set;

public class Text<T> {
	
	/*
	 * Holds the "vocabulary" for the tree
	 */

	public LinkedList<Integer> items;
	HashMap<T,Integer> vocab;
    int index;

    
    public Text() {
    	vocab = new HashMap<T,Integer>();
    	items = new LinkedList<Integer>();
    	this.index = 0;
    	//vocab.put((T)Constants.ROOT, index++);
    }
    
    public Set<T> getVocabulary() {
    	return vocab.keySet();
    }
    
    public void pushFront(int item) {
    	items.addFirst(item);
    }
    
    public void pushBack(int item) {
    	items.add(item);
    }
    
    public void put(T word, int i) {
    	vocab.put(word, i);
    	index++;
    }
    
    public int pop() {
    	return items.pop();
    }
    
    public void cut() {
    	items.removeFirst();
    }
    
    public int size() {
    	return this.items.size();
    }
    
    public void clear() {
    	this.items.clear();
    }
    
    public int at(int i) {
    	if (size() == 0) return 0;
    	if (i == -1) i = size() -1;
    	return items.get(i);
    }
    
    public void print() {
    	
    }
    
    public int offer(T word) {
    	if (get(word) == -1){
    		vocab.put(word, index);
    		return index++;
    	}
    	return vocab.get(word);
    }
    
    public int get(T word) {
    	if (vocab.containsKey(word)) {
    		return vocab.get(word);
    	}
    	return -1;
    }
    
    public boolean has(T word) {
    	if (get(word) == -1) 
    		return false;
    	return true;
    }
    
    public int vocabSize() {
    	return this.vocab.size();
    }
    
    public T getWordFromVocabIndex(int ind) {
    	for (T word : vocab.keySet()) {
    		if (vocab.get(word) == ind)
    			return word;
    	}
    	//return (T)Constants.UNK;
    	return null;
    }
    
    public T getWordFromIndex(int ind) {

    	for (T word : vocab.keySet()) {
    		if (vocab.get(word) == this.at(ind))
    			return word;
    	}
    	//return (T)Constants.UNK;
    	return null;
    }    
    

}
