package smoothing;

import segment.Segment;
import suffixtree.SuffixTree;

public class AdditiveSmoothing<T> extends Smoothing<T> {
	
	double disc = 1.0;

	public AdditiveSmoothing(SuffixTree<T> t) {
		super(t);
	}
	
    public double wordHereMultChild(Segment parent, Segment child) {
    	double prob = (disc + child.getCount()) / (parent.numChildren() * disc + parent.getCount()); 
    	
		return prob;
	}
    
    public void updateUnk() {
    	unk = disc / (current.numChildren() * disc + current.getCount()); 
    }
	
}
