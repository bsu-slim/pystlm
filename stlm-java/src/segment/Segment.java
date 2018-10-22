package segment;

public class Segment {
	
	/*
	 * Segments make up the tree. There is a base segment, then a root segment, then the tree expands into internal segments, until it gets to leaf segments. 
	 * These segment types make it easier to traverse the tree during building and during evaluation
	 */
	
	public int left;
	public int right;
	public Segment link;
	
    public Segment() {
    	this.left = 0;
    }
    
    public Segment(int l) {
    	this.left = l;
    }
    
    public void setLink(Segment link) {
    	this.link = link;
    }
    
    
    public Segment getLink() {
    	return this.link;
    }
    
    public int getLeft() {
    	return left;
    }
    
    public  int getRight() {
    	return -1;
    }
    
    public Segment put(Segment branch, int w) {
    	return null;
    }
    
    public int findIndex(int word) {
    	return 0;
    }
    
    public Segment findBranch(int ind) {
    	return null;
    }
    
    public void setCount(double d) {
    	
    }
    
    public void setCount() {
    	
    }
    
    public double getCount() {
    	return 0.0;
    }
    
    public int span() {
    	return getRight() - getLeft();
    }
    
    public void increment() {
    	 
    }
    
    public void increment(double d) {
    	
    }
     
    public int numChildren() {
    	return 0;
    }
	
}
