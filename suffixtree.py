'''
Created on Oct 23, 2018

@author: ckennington
'''
from segment import RootSegment, BaseSegment, InternalSegment, LeafSegment
from sequence import Text

class SuffixTree:
    
    def __init__(self):
        text = Text()
        root = RootSegment(text)
        base = BaseSegment(root)
        root.set_link(base);
        
        #text.offer(Constants.ROOT);
        self.index = 0;
        self.loc = 0;
        self.offset = 0;
        self.current = root;
        self.num_sentences = 0;
        self.num_nodes = 1;
        self.num_leaves = 0;
        
    def get_root(self):
        return self.root;
        
    def add(self, element):
        word = self.text.offer(element)
        self.text.push_back(word)
        self.process(word)
        self.index += 1
        
    
    def start_from_root(self):
        self.offset = 0
        self.current = self.get_root()
        
    def canonize(self):
        if self.offset > 0:
            branch = self.current.find_branch(self.text.at(self.loc))
            span = branch.span()
            while self.offset >= span:
                self.loc += span
                self.offset -= span
                current = branch
                branch = current.find_branch(self.text.at(self.loc))
                span = branch.span()
                    
    
    def process(self, word):
        
        p = False
        b  = None
        branch = None
        old_branch = None
        
        while True:
            self.canonize()
            if self.offset == 0:
                b = self.current.find_branch(self.text.at(self.index))
                p = b != None
            else:
                b = self.current.find_branch(self.text.at(self.loc))
                p = self.text.at(b.get_left() + self.offset) == self.text.at(self.index)
            
            if p:
                self.loc = b._get_left()
                self.offset += 1
                if old_branch != None: old_branch.set_link(self.current)
                
            if self.offset > 0:
                branch = InternalSegment(b.get_left())
                self.num_nodes += 1
                old = self.current.put(branch, self.text.at(b.get_left()))
                old.left += self.offset
                branch.put(old, self.text.at(old.get_left()))
                leaf = LeafSegment(self.text, self.index)
                self.num_nodes += 1
                self.num_leaves += 1
                leaf.set_link(self.root)
                branch.put(leaf, self.text.at(self.index))
                branch.increment(old.get_count() + leaf.get_count())
                self.current.increment(old.get_count())
                
            else:
                branch = self.current
                leaf = LeafSegment(self.text, self.index)
                self.num_nodes += 1
                self.num_leaves += 1
                leaf.set_link(self.root)
                branch.put(leaf, self.text.at(self.index))
                branch.increment() # this might cause problems; overloading
                
            
            if old_branch != None:
                old_branch.set_link(branch)
                
            old_branch = branch
            self.current = self.current.get_link()
        
        
        
        
    def update_counts(self, c):
        if c is None: return
        if c.get_left() > -1:
            if c.num_children() == 0: return
            count = c.get_count()
            s = c
            s.set_count()
            if count == s.get_count(): return
            
        s = c
        for child in s.get_children():
            self.update_counts(s.get_children()[child])
            
    
    def update_all_counts(self):
        self.update_counts(self.get_root())
        
        
    def vocab_size(self):
        return self.text.vocab_size()
    
    
    def at(self, i):
        return self.text.at(i)
    
        
        
        
    
        