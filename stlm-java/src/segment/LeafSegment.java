package segment;

import sequence.Text;

public class LeafSegment extends Segment {
	
    Text text;
    
    public LeafSegment() {
    	
    }
    
    public LeafSegment(Text t, int l) {
    	super(l);
    	text = t;
    }
    
    public int getRight() {
    	return this.text.size();
    }
    
    public int numChildren() {
    	return 0;
    }
    
    public int findIndex(int word) {
    	return -2;
    }
    
    public double getCount() {
    	return 1.0;
    }
    
    public Segment findBranch(int word) {
    	return null;
    }
    


}
