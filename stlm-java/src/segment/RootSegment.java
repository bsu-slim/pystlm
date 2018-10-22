package segment;

import sequence.Text;

public class RootSegment<T> extends InternalSegment {
	
    public Text<T> text;
	
    public RootSegment(Text<T> text) {
    	super(-1);
    	this.text = text;
    }
    
    public RootSegment() {
    	
    }
     
    public int getRight() {
    	return 0;
    }
    
    public void increment() {
    	
    }
    
    public double getCount() {
    	return text.size();
    }


}
