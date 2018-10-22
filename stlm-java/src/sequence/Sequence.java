package sequence;

import model.Constants;

public class Sequence extends Queue<String> {

    int numPads;
    
    public Sequence() {


    }
    
    /*
     * Sequences sometimes need <s> and </s> "padding" the params are set in Constants
     */
    public void pad() {
    	int max = Constants.NUM_PAD;
    	numPads = max;
    	for (int i=0; i<max; i++) {
    		pushFront(Constants.START);
    		pushBack(Constants.STOP);
    		numPads++;
    	}
    	numPads *= 2;
    }
    
    public void padBack() {
    	int max = Constants.NUM_PAD;
    	numPads = max;
    	for (int i=0; i<max; i++) {
    		pushBack(Constants.STOP);
    	}
    }



}
	