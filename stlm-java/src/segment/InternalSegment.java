package segment;

import java.util.HashMap;

public class InternalSegment extends Segment {

	public double count;
	public HashMap<Integer,Segment> children;
	
    public InternalSegment() {
    	children = new HashMap<Integer,Segment>();
    	setCount(0.0);
    }
	 
    public InternalSegment(int l) {
    	super(l);
    	children = new HashMap<Integer,Segment>();
    	setCount(0.0);
    }
    
    public Segment findBranch(int w) {
    	if (children.isEmpty()) return null;
    	int i = findIndex(w);
    	if (i == -2) return null;
    	return children.get(i);
    }
    
    public int findIndex(int i) {
    	if (children.containsKey(i))
    		return i;
    	return -2;
    }
    
    public int getRight() {
    	return this.children.get(right).getLeft();
    }
    
    public void setCount() {
    	setCount(0.0);
    	for (Integer s : children.keySet()) {
    		increment(children.get(s).getCount());
    	}
    }
    
    public double getCount() {
    	return count;
    }
    
    public void setCount(double d) {
    	count = d;
    }
    
    public  void increment(double d) {
    	count += d;
    }
    
    public void increment() {
    	count++;
    }
    
    public int numChildren() {
    	return this.children.size();
    }
    
    public Segment put(Segment branch, int w) {
    	int i = findIndex(w);
    	if (i == -2) {
    		if (children.isEmpty()) right = w;
    		children.put(w, branch);
    		return null;
    	}
    	else {
    		Segment old = children.get(w);
    		children.put(w, branch);
    		return old;
    	}
    }
}
