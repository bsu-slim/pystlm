package smoothing;

import segment.Segment;
import suffixtree.SuffixTree;

public class AddOneSmoothing<T> extends Smoothing<T> {

	public AddOneSmoothing(SuffixTree<T> t) {
		super(t);
	}
	
	public double wordHereMultChild(Segment parent, Segment child) {
		double prob = (1.0 + child.getCount()) / (parent.numChildren() + parent.getCount());
		
		
		return prob;
	}
	
	public void updateUnk() {
		unk = 1.0 / current.numChildren(); 
	}
	
	

}
