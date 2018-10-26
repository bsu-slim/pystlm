'''
Created on Oct 23, 2018

@author: ckennington
'''

from segment import RootSegment, BaseSegment, InternalSegment, LeafSegment
from sequence import Text
from constants import Constants

from sklearn import linear_model
import numpy as np
import random

class SuffixTree:
    
    def __init__(self):
        self.text = Text()
        self.root = RootSegment(self.text)
        self.base = BaseSegment(self.root)
        self.root.set_link(self.base);
        
        self.text.offer(Constants.ROOT);
        self.index = 0;
        self.loc = 0;
        self.offset = 0;
        self.current = self.get_root()
        self.num_sentences = 0;
        self.num_nodes = 1;
        self.num_leaves = 0;
        self.disc = 0.1
        self.wac = {}
        self.classifier_spec=(linear_model.LogisticRegression,{'penalty':'l2'})
        
    def get_root(self):
        return self.root
    
    def get_text(self):
        return self.text
        
    def add(self, element):
        word = self.text.offer(element)
        self.text.push_back(word)
        self.process()
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
                self.current = branch
                branch = self.current.find_branch(self.text.at(self.loc))
                if branch is None: break # BAD!!!
                span = branch.span()
                    
    def process(self):
        p = False
        b  = None
        branch = None
        old_branch = None
        
        while True:
            self.canonize()
            if self.offset == 0:
                b = self.current.find_branch(self.text.at(self.index))
                p = b is not None
            else:
                b = self.current.find_branch(self.text.at(self.loc))
                p = self.text.at(b.get_left() + self.offset) == self.text.at(self.index)
            
            if p:
                self.loc = b.get_left()
                self.offset += 1
                if old_branch is not None: old_branch.set_link(self.current)
                break
                
            if self.offset > 0:
                branch = InternalSegment(b.get_left())
                self.num_nodes += 1
                old = self.current.put(branch, self.text.at(b.get_left()))
                old.left += self.offset
                branch.put(old, self.text.at(old.get_left()))
                leaf = LeafSegment(self.text, self.index)
                self.num_nodes += 1
                self.num_leaves += 1
                leaf.set_link(self.get_root())
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
                branch.update_count()
                
            if old_branch is not None:
                old_branch.set_link(branch)
                
            old_branch = branch
            self.current = self.current.get_link()
        
    def update_counts(self, c):
        if c is None: return
        if c.get_left() > -1:
            if c.num_children() == 0: return
            c.update_count()
            
        for child in c.children:
            self.update_counts(c.children[child])
            
    def train_node(self, parent_targets, parent, node):
        if node is None: return
        parent_target = self.ground_node(parent_targets, parent, node, 0) # make sure to the copy the list so it doesn't pass by ref
        if parent_target is not None:
            parent_targets.append(parent_target)
        
        if parent is not None:
            offset=1
            while offset < parent.span():
                parent_target = self.ground_node(parent_targets, parent, node, offset)
                if parent_target is not None: parent_targets.append(parent_target)
                offset+=1
            
        if node.num_children() == 0: return
        for child in node.children:
            self.train_node(list(parent_targets), node, node.children[child])
    
    def train_nodes(self):
        for child in self.get_root().children:
            self.train_node(list(), None, self.get_root().children[child])
            
    def get_train_data_for_word(self, word):
        todrop = ['word', 'inc', 'episode_id', 'id']
        positive_train,negative_train = self.train_data
        pos_word_frame = positive_train[positive_train.word == word]
        pos_word_frame = np.array(pos_word_frame.drop(todrop, 1))
        neg_word_frame = negative_train[negative_train.word == word]
        neg_word_frame = np.array(neg_word_frame.drop(todrop, 1))
        neg_word_frame = random.sample(list(neg_word_frame), len(pos_word_frame))
        return np.array(pos_word_frame),np.array(neg_word_frame)
        
    
    def ground_node(self, parent_targets, parent, child, offset): 
        
        
        if offset > 0:
            c_word = self.text.get_word_from_index(self.at(parent.get_left())+offset)
        else:
            c_word = self.text.get_word_from_index(self.text.at(child.get_left()))
            
        pos_word_frame,neg_word_frame = self.get_train_data_for_word(c_word)
        
        if len(pos_word_frame) == 0: return None
        
        X = np.concatenate([pos_word_frame,  neg_word_frame])
        
        if parent is None:
            target = c_word
        else:
            p_word = self.text.get_word_from_index(self.text.at(parent.get_left()))
            target = u'{}-{}'.format(p_word, c_word)
            # need all parents
            if len(parent_targets) > 0:
                X_pt = np.copy(X)
                for parent_target in parent_targets:
                    prediction = self.wac[parent_target].predict_proba(X_pt)[:,1]
                    X_pt = np.concatenate([prediction.reshape(-1,1), X],axis=1) # adding in the parent data
                X = X_pt
        
        classifier, classf_params = self.classifier_spec
        y = np.array([1] * len(pos_word_frame) + [0] * len(neg_word_frame))
        
        
        this_classf = classifier(**classf_params)
        this_classf.fit(X,y)
        self.wac[target] = this_classf
        
        return target
    
    
    def set_grounded_data(self, train_data):
        self.train_data = train_data
        
    def set_classifier_spec(self, spec):
        self.classifier_spec= spec
        
    
    def update_all_counts(self):
        self.update_counts(self.get_root())
        
        
    def vocab_size(self):
        return self.text.vocab_size()
    
    
    def at(self, i):
        return self.text.at(i)
    
    def print_tree(self):
        for child in self.get_root().children:
            self.print_segment(self.get_root().children[child], 0)
        
        
    def print_segment(self, c, depth):
        if c is None: return
        
        pad = ''
        for i in range(depth): pad += '  '
        print(pad + str(c.get_left()) + ' ({})'.format(self.text.get_word_from_index(self.at(c.get_left()))) + ' count({})'.format(c.get_count()))
        
        offset = 1
        while offset < c.span():
            print(pad + str(c.get_left()) + ' offset({})'.format(self.text.get_word_from_index(self.at(c.get_left())+offset)))
            offset +=1
        
        if c.num_children() == 0: return
        for child in c.children:
            self.print_segment(c.children[child], depth+1) 
        
        
    
        
        