package smoothing;

import segment.Segment;
import suffixtree.SuffixTree;

public class Smoothing<T> {
	
	/*
	 * Not the best way to handle smoothing, but here it is. This is where word probabilities are computed "on the fly" which allows the model to be "dynamic" in that
	 * it can be built and used simultaneously. In other words, it's always ready to be used.
	 */
    double unk;
    double highestDepth;
    SuffixTree<T> trie;
    double depth;
    double maxDepth;
    Segment current;
    double disc;
    double sentPosition;
    double uniweight;
    
    public void setMaxDepth(double d) {
    	this.maxDepth = d;
    }
    
    public double getDepth() {
    	return this.depth;
    }
    
    public double getMaxDepth() {
    	return this.maxDepth;
    }
    
    public void setDepth(double d) {
    	this.depth = d;
    }
	
    public Smoothing() {
    	
	}
    public Smoothing(SuffixTree<T> t) {
    	this.trie = t;
    	this.reset();
    	this.disc = 0.1;
    	this.uniweight = 0.5;
	}
    
    public double wordHereMultChild(Segment parent, Segment child) {
    	//System.out.println(depth + " " + child.getCount() + " " + parent.getCount() + " " + parent.numChildren() + " " + unk);
    	//double prob = (child.getCount()-(disc/parent.numChildren())) / parent.getCount();
    	double prob = (child.getCount() - (disc)) / (parent.getCount());
    	
    	//when we back off, apply the BOW
    	/*
    	if (depth < maxDepth) {
    		prob *=(unk) / ((disc / parent.getCount()));
    	}
    	if (depth <= 1) {
    		prob = prob * uniweight + (1.0-uniweight)* child.numChildren() / parent.numChildren();
    	}
    	*/
    	
    	return prob;
	}
    
    public double wordHereOneChild(int offset) {
		double count = current.getCount();
		double prob = (count - (disc)) / count;
		/*
    	if (depth < maxDepth) {
    		prob *= unk / (disc / count);
    	}
    	if (depth <= 1) {
    		prob = prob * uniweight + (1.0-uniweight)/ current.numChildren();
    	}    	*/
    	return prob;		
	}
    
    public void updateUnk() {
    	//if (unk == 1.0)

    	unk = (disc) / current.getCount();
	}
    
    public double getUnk(Segment parent) {
		return unk;
    	//return 0.0;
	}
    
    public void setCurrent(Segment c) {
    	this.current = c;
	}
    
    public void incDepth() {
    	this.depth++;
    	if (this.depth > this.maxDepth) 
    		this.maxDepth = this.depth;
	}
    public void decDepth() {
    	this.depth--;
	}
    public void reset() {
    	this.depth = 0;
    	this.maxDepth = 0;
    	this.unk = 1.0;
	}
    public void resetUnk() {
    	unk = 1.0;
    	maxDepth = depth;
	}
    public double weight() {
		return 1.0;
	}
    public void incSentPosition() {
    	this.sentPosition++;
	}


}
