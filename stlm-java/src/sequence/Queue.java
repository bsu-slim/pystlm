package sequence;

import java.util.LinkedList;

public class Queue<T> {
	
	/*
	 * Wrapper around a linked list 
	 */
	
    LinkedList<T> items;
	
    public Queue() {
    	items = new LinkedList<T>();
    }
    
    public void pushFront(T item) {
    	this.items.addFirst(item);
    }
    
    public void pushBack(T item) {
    	this.items.add(item);
    }
    
    public T pop() {
    	return this.items.pop();
    }
    
    public void cut() {
    	this.items.removeFirst();
    }
    
    public int size() {
    	return this.items.size();
    }
    
    
    public void clear() {
    	items.clear();
    }
    
    public T at(int i) {
    	return this.items.get(i);
    }
    
    public boolean isEmpty() {
    	return this.items.isEmpty();
    }
    
    public String toString() {
    	String string = "";
    	for (T item : items) {
    		string += item.toString() + " ";
    	}
    	return string.trim();
    }

    
}
