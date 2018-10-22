package segment;

public class BaseSegment extends InternalSegment {

	protected Segment root;
	
	public BaseSegment() {
		
	}
	
	public BaseSegment(RootSegment root) {
		super(-2);
		this.root = root;
	}
	
	public Segment findBranch(int word) {
		return root;
	}
	
}
