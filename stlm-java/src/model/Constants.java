package model;

public class Constants {

	/*
	 * Constants for the program. Kind of crude, but if you need to change anything do it here. For the most part, 
	 * you shouldn't need to change anything.
	 */
	public static final String ROOT = "<root>";
	public static final String UNK = "UNK";
	public static final int NUM_PAD = 1;
	public static final String STOP = "</s>";
	public static final String START = "<s>";
	public static final String NEWLINE = "\n";
	
	public static final String DASH = "-";
	public static final String DOT = ".";
	public static final String LM = "lm";
	public static final String TEXT = "text";
	public static final String PERP = "perp";
	public static final String ORDER = "order";
	public static final String LONG_BRANCHES = "long";
	public static final String PORT = "port";
	public static final String TEST = "test";
	public static final String UNIT = "unit";
	public static final String STATS = "stats";
	public static final String SERVER = "server";
	
	public static final String CL_LM = DASH + LM;
	public static final String CL_TEXT = DASH + TEXT;
	public static final String CL_TEST = DASH + TEST;
	public static final String CL_PERP = DASH + PERP;
	public static final String CL_ORDER = DASH + ORDER;
	public static final String CL_SERVER = DASH + SERVER;
	public static final String CL_LONG = DASH + LONG_BRANCHES;
	public static final String CL_PORT = DASH + PORT;
	public static final String CL_UNIT = DASH + UNIT;
	public static final String CL_STATS = DASH + STATS;
	
	public static final int DEF_ORDER = -1;

}
