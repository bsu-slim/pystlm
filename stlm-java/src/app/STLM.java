package app;

import io.Scanner;

import java.io.FileNotFoundException;
import java.util.HashMap;

import sequence.Sequence;
import suffixtree.SuffixTree;

import lm.STLanguageModel;
import model.Constants;

public class STLM {
	
	public static void main(String[] argv) {
		
		/*
		 * My own way of handling command line arugments. Mostly, just use -text and -test and -perp
		 */
		HashMap<String,String> arguments = new HashMap<String,String>();
		for (int i=0; i<argv.length; i++) {
		    if (argv[i].equals(Constants.CL_LM))
		        arguments.put(argv[i],argv[i+1]);
		    else if (argv[i].equals(Constants.CL_TEXT))
		        arguments.put(argv[i],argv[i+1]);
		    else if (argv[i].equals(Constants.CL_TEST))
		        arguments.put(argv[i],argv[i+1]);
		    else if (argv[i].equals(Constants.CL_ORDER))
		        arguments.put(argv[i],argv[i+1]);
		    else if (argv[i].equals(Constants.CL_PERP))
		        arguments.put(argv[i],argv[i]);
		    else if (argv[i].equals(Constants.CL_SERVER))
		        arguments.put(argv[i],argv[i]);
		    else if (argv[i].equals(Constants.CL_PORT))
		        arguments.put(argv[i],argv[i+1]);
		    else if (argv[i].equals(Constants.CL_UNIT))
		        arguments.put(argv[i],argv[i]);
		    else if (argv[i].equals(Constants.CL_STATS))
		        arguments.put(argv[i],argv[i]);		
		    else if (argv[i].equals(Constants.CL_LONG))
		        arguments.put(argv[i],argv[i]);			    
		}
		
		/*
		 * First, build the suffix tree from the -text file
		 */
		SuffixTree<String> trie = new SuffixTree<String>();
		if (arguments.get(Constants.CL_TEXT) != null) {
			
			try {
				System.out.print("training...");
				Scanner scan = new Scanner(arguments.get(Constants.CL_TEXT), true);
		    	//trie.add(Constants.ROOT);
		    	while (scan.moreSentences()) {
		    		Sequence sent = scan.nextSentence();
		    		if (sent == null) {
		    			continue;
		    		}
		    		sent.pad();
		    		for (int i=0; i<sent.size(); i++) {
		    			trie.add(sent.at(i));
		    		}
		    	}
				trie.finish();
				System.out.println("done.");
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
		}
		//trie.print();
		STLanguageModel<String> lm = new STLanguageModel<String>(trie);
		if (arguments.get(Constants.CL_LONG) != null) {
			lm.printLongBranches();
		}
		
		
		/*
		 * Now, use the suffix tree, either for individual logProbs, or perplexity
		 */
		if (arguments.get(Constants.CL_TEST) != null) {
			try {
				Scanner scan = new Scanner(arguments.get(Constants.CL_TEST), true);
				
				if (arguments.get(Constants.CL_STATS) != null) {
					lm.computeStats(scan);
				}
				else if (arguments.get(Constants.CL_PERP) != null) {
					
					 /*
				     * Standard perplexity of a corpus
				     */
						Sequence cur;
						double numSent = 0.0;
						double logprob = 0.0;
						double words = 0.0;
						
						while (scan.moreSentences()) {
							cur = scan.nextSentence();
							if (cur == null || cur.size() == 0) continue;
							words += cur.size();
							cur.padBack();
							//lm.startNewUtterance();
							//for (int i=0; i<cur.size()-1; i++) {
							//	lm.logProbPrefix(cur.at(i));
							//}
							//logprob += lm.logProbPrefix(cur.at(cur.size()-1));
							logprob += lm.logProb(cur);
							cur.clear();
							numSent++;
						}
						
						numSent--;

						
						System.out.println("logprob: " + logprob);
						logprob = 0 - logprob;
						System.out.println("numSent " +numSent);
						double perp = Math.pow(10.0, (logprob / (words + numSent)));
						System.out.println(perp);
				}
				else {
					while (scan.moreSentences()) {
						Sequence sent = scan.nextSentence();
						//System.out.println(sent);
						if (sent == null || sent.size() == 0) continue;
						sent.pad();
						//System.out.println(sent);
						System.out.println(lm.logProb(sent));
						//System.out.println(lm.getMaxDepthReached());
					}
				}
				
				
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
		}
		
		
	}



}
