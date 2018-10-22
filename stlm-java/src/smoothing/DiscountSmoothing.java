package smoothing;

import segment.Segment;
import suffixtree.SuffixTree;

public class DiscountSmoothing<T> extends Smoothing<T> {
	
	public DiscountSmoothing(SuffixTree<T> t) {
		super(t);
	}
	
	double disc = 0.1;
	
    public double wordHereMultChild(Segment parent, Segment child) {
    	
    	if (parent == null || child == null || parent.getLeft() == -2 || child.getLeft() == -2)
    		return 1.0;
    	
    	double lambda = disc / parent.getCount() * parent.numChildren();
    	Segment newChild = parent.findBranch(trie.getText().at(child.getLeft()));
    	return (Math.max(0.0, child.getCount() - disc) / parent.getCount())+(lambda) * this.wordHereMultChild(parent.getLink(),  newChild);
	}
    
    public double wordHereOneChild(int offset) {
		double count = current.getCount();
		return (count - (disc)) / count;		
	}
    
    public void updateUnk() {
    	unk =  disc / current.getCount();
    }

}
