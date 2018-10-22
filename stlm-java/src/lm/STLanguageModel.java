package lm;

import java.util.HashMap;
import java.util.LinkedList;

import model.Constants;
import io.Scanner;
import segment.InternalSegment;
import segment.LeafSegment;
import segment.Segment;
import sequence.Queue;
import sequence.Sequence;
import sequence.Text;
import smoothing.AddOneSmoothing;
import smoothing.AdditiveSmoothing;
import smoothing.DiscountSmoothing;
import smoothing.Smoothing;
import smoothing.WittenBellSmoothing;
import suffixtree.SuffixTree;

public class STLanguageModel<T> {
	
	private SuffixTree<T> trie;
    Text<T> offset;
    Segment current;
    Segment branch;
    Segment arc; //this may not be necessary....try using the branch instead
    Smoothing<T> smoother;
    double numMult;
    double numOne;
    double numUnk;
    double numBO;
    int maxDepthReached;
    
    //for incremental stuff
	double incProb = 0.0;
	int incWord;
   // private LogMath logMath;
    public STLanguageModel() {
	}
    public STLanguageModel(SuffixTree<T> tree) {
    	this.setTrie(tree);
    	setSmoothing(new DiscountSmoothing<T>(getTrie()));
    	offset = new Text<T>();
    	//logMath = new LogMath();
	}
    
    /*
     * starts things over - begin the chain rule from the root node
     */
    public void startNewUtterance() {
    	this.smoother.resetUnk();
		this.smoother.reset();
		this.current = getTrie().getRoot();
		this.smoother.setCurrent(this.current);
		this.offset.clear();
		this.incProb = 0.0;
		this.incWord = 0;
		this.maxDepthReached = 0;
    }
    
    /*
     * get logProb for this prefix of the sentence
     */
    public double logProbPrefix(T increment) {
    	this.smoother.resetUnk();
    	incWord = getTrie().getText().get(increment);
    	this.smoother.incSentPosition();
    	double p = getProb(incWord);
    	this.incProb += Math.log10(p);
    	return incProb;
    }
    
    public double prob(Queue<T> sent) {
    	 // double unigramWeight = 0.7;
    	this.startNewUtterance();
		double prob = 1.0;
		int word;
		
		for (int i=0; i<sent.size(); i++) {
			this.smoother.resetUnk();
			word = getTrie().getText().get(sent.at(i));
			this.smoother.incSentPosition();
			double p = getProb(word);
			prob *= p;
		}

		return prob;
    }
    
    /*
     * Returns the logProb for a sentence
     */
    public double logProb(Queue<T> sent) {
       // double unigramWeight = 0.7;
    	this.startNewUtterance();
		double prob = 1.0;
		int word;
		
		for (int i=0; i<sent.size(); i++) {
			this.smoother.resetUnk();
			word = getTrie().getText().get(sent.at(i));
			this.smoother.incSentPosition();
			double p = getProb(word);
			
			//System.out.println(sent + " "+ p);
			
			prob += Math.log10(p);
			 
			//This commented out stuff below handles cases when you want the depth to be limited. We're not doing that here.
			/*
			if (smoother.getDepth() == 1) {
				float logUniformProbability = -logMath.linearToLog(trie.getRoot().getCount());
		        float logUnigramWeight = logMath.linearToLog(unigramWeight);
		        float inverseLogUnigramWeight = logMath
			                .linearToLog(1.0 - unigramWeight);				
                float p1 = (float)p + logUnigramWeight;
                float p2 = logUniformProbability + inverseLogUnigramWeight;
                prob += logMath.addAsLinear(p1, p2);
			}
			else {
			*/
				
			//}
			//System.out.println(sent.at(i) + " " + p);
			
			if (Constants.DEF_ORDER != -1) {
				while (this.smoother.getDepth() >= Constants.DEF_ORDER) {
					if (current.getLeft() > -1) {
						current = current.getLink();
						if (current.getLeft() <= -1)
							smoother.setMaxDepth(2);
					}
					else {
						if (offset.size()  > 0) {
							offset.cut();
						}
					}
					this.smoother.setMaxDepth(smoother.getMaxDepth() -1);
					this.smoother.decDepth();
				}
			}
			
		}

		return prob;
		
	}
    
    /*
     * Returns the probability of a word in context from the suffix tree. The probs are based on the smoothing model.
     * A sentence starts at the root node, then gets the unigram probability there, then moves into the tree for each word
     * in the sentence. If a word sequence is not represented, it backs off by following the suffix link and checks there.
     */
    public double getProb(int word) {
		if (smoother.getDepth() > this.maxDepthReached) {
			this.maxDepthReached = (int)smoother.getDepth();
		}
		
		double prob = 0.0;
		//if we're moving into a word sequence....
		if (offset.size() > 0) {
			arc = current;
			if (arc.getLeft() + offset.size() > arc.getRight()) {
				current = findPrefixArc(offset.at(0));
				smoother.setCurrent(current);
				offset.clear();
			}
		}
		
		//otherwise, the parent node has the child word
		if (wordIsHere(word)) {
			smoother.incDepth();
			//the child is either direct...
			if (offset.size() == 0) {
				Segment child = findPrefixArc(word);
				prob = smoother.wordHereMultChild(current, child);
				//System.out.println("multchild " + prob); 
				numMult++;
				if (child.span() > 1) {
					offset.pushBack(word);
				}
				else {
					current = child;
					smoother.setCurrent(current);
				}
			}
			//... or part of the offset
			else {
				prob = smoother.wordHereOneChild(offset.size());
				//System.out.println("onechild " + prob); 
				numOne++;
				offset.pushBack(word);
			}
			//smoother.incDepth();
		}
		else {
			//When the child node doesn't exist, back off (handle offsets, etc)
			smoother.updateUnk();
			numBO++;
			
			if (current.getLeft() > -1) {
				if (offset.size() > 0) {
					smoother.setDepth(smoother.getDepth() - offset.size() -1);
					offset.clear();
				}
				else {
					smoother.decDepth();
				}
				current = current.getLink();
				if (current.getLeft() == -1) {
					smoother.setDepth(0);
				}
				smoother.setCurrent(current);
				prob = getProb(word);
			}
			else {
				if (offset.size() > 0) {
					offset.cut();
					smoother.decDepth();
					prob = getProb(word);
				}
				else {
					smoother.setDepth(0);
					prob = smoother.getUnk(current);
					//System.out.println("gotunk " + prob); 
					numUnk++;
				}
			}
		}

		return prob;
	}
    
    public int getMaxDepthReached() {
    	return this.maxDepthReached;
    }
    
    /*
     * Offsets make things messy but fast, a word exists if it is somewhere within a range
     */
    public boolean wordIsHere(int word) {
		if (offset.size() == 0) {
			return findPrefixArc(word) != null;
		}
		else {
			branch = findPrefixArc(offset.at(0));
			if (branch.getLeft() + offset.size() <= getTrie().getText().size()) 
				if (getTrie().getText().at(branch.getLeft() + offset.size()) == word) // -1 or not?
					return true;
			return false;
		}
	}
    
    public Segment findPrefixArc(int word) {
		return current.findBranch(word);
	}
    
    public void setSmoothing(Smoothing<T> s) {
    	this.smoother = s;
	}
    
    public void computeStats(Scanner scan) {
    	  double max = 0.0;
    	  double depths = 0.0;
    	  double numSents = 0.0;
    	  double sentlens = 0.0;
    	  while (scan.moreSentences())
    	  {
    	    Sequence sent = new Sequence();
    	    numSents++;
    	    sent = scan.nextSentence();
    	    if (sent.size() == 0) continue;
    	    sent.pad();
    	    sentlens += sent.size();
    	    this.logProb((Queue<T>) sent);
    	    if (smoother.getDepth() > max)
    	      max = smoother.getDepth();
    	    depths += smoother.getDepth();
    	  }
    	  
    	  System.out.println("Total number of nodes: " +" "+ getTrie().numNodes );
    	  System.out.println("Number of leaf nodes: " +" "+ getTrie().numLeaves );
    	  System.out.println("Number of internal nodes: " +" "+  (getTrie().numNodes-getTrie().numLeaves));
    	  System.out.println("Percentage of leaf nodes: " +" "+ ((double)getTrie().numLeaves/(double)getTrie().numNodes));
    	  System.out.println("Percentage of internal nodes: " +" "+  ((((double)getTrie().numNodes-(double)getTrie().numLeaves)/(double)getTrie().numNodes)) );
    	  System.out.println("Size of vocabulary: " +" "+ getTrie().getRoot().children.size() );
    	  System.out.println("Number of words: " +" "+ getTrie().getText().items.size() );
    	  System.out.println("Number of evaluation sentences: " +" "+ numSents );
    	  System.out.println("Number of evaluation words: " +" "+ sentlens );
    	  System.out.println("Average sentence length: " +" "+ (sentlens / numSents) );
    	  System.out.println("Maximum depth reached: " +" "+ max );
    	  System.out.println("Average depth reached: " +" "+ (depths / numSents) );
    	  System.out.println("Percentage of probs with multiple branches: " +" "+ (numMult / sentlens) );
    	  System.out.println("Percentage of probs with one branch: " +" "+ (numOne / sentlens) );
    	  System.out.println("Percentage of probs using UNK: " +" "+ (numUnk / sentlens) );
    	  System.out.println("Number of individual back off instances: " +" "+ numBO );    	  
    	  
	}
	public SuffixTree<T> getTrie() {
		return trie;
	}
	public void setTrie(SuffixTree<T> trie) {
		this.trie = trie;
	}
	public void printLongBranches() {
		System.out.println("Printing long branches...");
		Segment root = this.getTrie().getRoot();
		//for (int i=0; i<this.getTrie().getText().size(); i++) {
		//	System.out.println(this.getTrie().getText().getWordFromIndex(i));
		//}
		findLongBranches(root);
		for (LinkedList<T> c : this.longSequences.keySet()) {
			System.out.println(this.longSequences.get(c).toString() + " " + c + "\\\\");
		}
	}
	
	HashMap<LinkedList<T>,Double> longSequences = new HashMap<LinkedList<T>,Double>();
	private void findLongBranches(Segment current) {

		if (current.getRight() > 0 && current.getRight() - current.getLeft() > 1 && current.getCount() > 1) {
			LinkedList<T> sequence = new LinkedList<T>();
			for (int i=current.getLeft(); i<current.getRight(); i++) {
				T word = this.getTrie().getText().getWordFromIndex(i);
				sequence.add(word);

			}
			if (!this.longSequences.containsKey(sequence))
				this.longSequences.put(sequence, 0.0);
			this.longSequences.put(sequence, this.longSequences.get(sequence)+current.getCount());
			
		}
		if (current instanceof InternalSegment) {
			InternalSegment internal = (InternalSegment) current;
			for (Integer child : internal.children.keySet()) {
				findLongBranches(internal.children.get(child));
			}
		}
	}
}
