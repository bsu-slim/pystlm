package smoothing;

import segment.Segment;
import suffixtree.SuffixTree;

public class WittenBellSmoothing<T> extends Smoothing<T> {
	
	public WittenBellSmoothing(SuffixTree<T> t) {
		super(t);
	}

	
    public double wordHereMultChild(Segment parent, Segment child) {
    	
    	if (parent == null || child == null || parent.getLeft() == -2 || child.getLeft() == -2)
    		return 1.0;
   
    	double lambda = parent.numChildren() / (parent.numChildren() + parent.getCount());
    	Segment newChild = parent.findBranch(trie.getText().at(child.getLeft()));
    	return (child.getCount() / parent.getCount())+(1-lambda) * this.wordHereMultChild(parent.getLink(),  newChild);
	}
    
    public void updateUnk() {
    	unk =  current.numChildren() / (current.getCount() + current.numChildren());
    }
    
}
