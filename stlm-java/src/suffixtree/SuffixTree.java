package suffixtree;

import java.util.Set;

import segment.BaseSegment;
import segment.InternalSegment;
import segment.LeafSegment;
import segment.RootSegment;
import segment.Segment;
import sequence.Queue;
import sequence.Text;

public class SuffixTree<T> {

    Segment oldBranch;
    Segment current;
    int loc;
    int offset;

    BaseSegment base;
    RootSegment<T> root;
    Text<T> text;

    boolean countsChanged;
    int index;
    public int numSentences;
    public int numNodes;
    public int numLeaves;
    
    public Text<T> getText() {
    	return this.text;
    }
    
    public Set<T> getVocabulary() {
    	return getText().getVocabulary();
    }
    
    public SuffixTree() {
    	text = new Text<T>();
    	root = new RootSegment<T>(text);
    	base = new BaseSegment(root);
    	root.setLink(base);
    	//text.offer(Constants.ROOT);
    	index = 0;
    	loc = 0;
    	offset = 0;
    	current = root;
    	numSentences = 0;
    	numNodes = 1;
    	numLeaves = 0;
    }
    
    public void finish() {
    	updateCounts();
    	//current = null;
    	//oldBranch = null;
    }
    
    public void add(T element) {
    	int word = text.offer(element);
		text.pushBack(word);
		process(word);
		index++;
    }
    
    public void startFromRoot() {
    	offset = 0;
    	current = this.getRoot();
    }
    
    public void addSequence(Queue<T> sequence) {
    	int word;
    	for (int i=0; i<sequence.size(); i++) {
			word = text.offer(sequence.at(i));
			text.pushBack(word);
			process(word);
			index++;
		}
    }
    
    /*
     * Read in sequences and add them to the tree one at a time.
     *
    public void build(String path) throws FileNotFoundException {
    	Scanner scan = new Scanner(path, true);
    	int word;
    	
    	while (scan.moreSentences()) {
    		Sequence sent = scan.nextSentence();
    		if (sent == null) {
    			continue;
    		}
    		sent.pad();
    		numSentences++;
    		for (int i=0; i<sent.size(); i++) {
    			word = text.offer(sent.at(i));
    			text.pushBack(word);
    			process(word);
    			index++;
    		}
    	}
    	System.out.println("DONE!");
    	finish();
    }
    */
    
    /*
     * Procressing a "word" builds the tree based on Ukkonen's algorithm.
     */
    public void process(int word) {
    	boolean p = false;
    	Segment b = null;
    	Segment branch = null;
    	oldBranch = null;
    	
    	while(true) {
    		canonize();
    		if (offset == 0) {
    			b = current.findBranch(text.at(index));
    			p = (b != null);
    		}
    		else {
    			b = current.findBranch(text.at(loc));
    			p = text.at(b.getLeft() + offset) == text.at(index);
    		}
    		
    		//Deal with branches
    		if (p) {
    			loc = b.getLeft();
    			offset++;
    			if (oldBranch != null) {
    				oldBranch.setLink(current);
    			}
    			break;
    		}
    		
    		if (offset > 0) {
    			branch = new InternalSegment(b.getLeft());
    			numNodes++;
    			Segment old = current.put(branch, text.at(b.getLeft()));
    			old.left += offset;
    			branch.put(old, text.at(old.getLeft()));
    			LeafSegment leaf = new LeafSegment(text, index);
    			numNodes++;
    			numLeaves++;
    			leaf.setLink(root);
    			branch.put(leaf,  text.at(index));
    			branch.increment(old.getCount() + leaf.getCount());
    			current.increment(old.getCount());
    		}
    		else
    		{
    			branch = current;
    			LeafSegment leaf = new LeafSegment(text, index);
    			numNodes++;
    			numLeaves++;
    			leaf.setLink(root);
    			branch.put(leaf, text.at(index));
    			branch.increment();
    		}
    		
    		if (oldBranch != null) {
    			oldBranch.setLink(branch);
    		}
    		
    		oldBranch = branch;
    		current = current.getLink();
    	}
    }
    
    public void canonize() {
    	if (offset > 0) {
    		Segment branch = current.findBranch(text.at(loc));
    		int span = branch.span();
    		while (offset >= span) {
    			loc += span;
    			offset -= span;
    			current = branch;
    			branch = current.findBranch(text.at(loc));
    			span = branch.span();
    		}
    	}
    }
    
    /*
     * Not part of Ukkonen's algorithm, this is where it becomes a language model. This is where it sets counts. The count of a node is the sum of the 
     * counts of the child nodes, where leaf nodes (no children) have a count of 1. 
     */
    public void updateCounts(Segment c) {
    	if (c == null) return;
    	if (c.getLeft() > -1) {
    		if (c.numChildren() == 0) return;
    		double count = c.getCount();
    		InternalSegment s = (InternalSegment) c;
    		s.setCount();
    		
    		if (count == s.getCount()) return;
    		else countsChanged = true;
    	}
    	
    	InternalSegment s = (InternalSegment) c;
    	for (Integer child : s.children.keySet()) {
    		updateCounts(s.children.get(child));
    	}
    	
    	
    }
    
    /*
     * When the tree is built, this runs a depth-first check to make sure the counts are accurate.
     */
    public void updateCounts() {
    	countsChanged = true;
    	while (countsChanged) {
    		countsChanged = false;
    		updateCounts(root);
    	}
    }
    
    public int vocabSize() {
    	return text.vocabSize();
    }
 
    public void print() {
    	printSegment(getRoot(), 0);
    }
    
    public void printSegment(Segment c, int depth) {
    	  if (c == null) return;

    	  String pad = "";
    	  for (int i=0; i<depth; i++) pad += "  ";

    	  System.out.println(pad  + c.getLeft() + " (" + text.getWordFromIndex(at(c.getLeft())) + ") count(" + c.getCount() + ")");
    	  /*
    	  for (unsigned int i=0; i<c->branches.size(); i++)
    	  {
    	    printSegment(c->branches.at(i),  depth+1);
    	  }
    	  */
    	  if (c.numChildren() == 0)
    	  {
    	    return;
    	  }
    	  InternalSegment s = (InternalSegment ) c;
    	  for (Integer i :s.children.keySet())
    	  {
    	    printSegment(s.children.get(i), depth+1);
    	  }    	
    }
    
    public int at(int i) {
    	return text.at(i);
    }
    
    public RootSegment<T>  getRoot() {
    	return this.root;
    }
   
    /*
     * Haven't needed this yet, but here it is.
     */
    void clearTree(Segment c) {
    	if (c == null) return;
    	if (c.numChildren() == 0)
    		return;
    	InternalSegment s = (InternalSegment) c;
    	for (Integer i : s.children.keySet()) {
    		clearTree(s.children.get(i));
    	}
    	c = null;
    }
   
}
