'''
Created on Oct 24, 2018

@author: casey
'''
import sqlite3
import pandas as pd
from scipy.spatial import distance
from pandasql import sqldf
import sklearn
from sklearn import ensemble
import random
import numpy as np
from tqdm import tqdm_notebook as tqdm
import traceback
import pickle
from tqdm import tqdm
from stlm import STLM
from suffixtree import SuffixTree
from sequence import Sequence

trials = 1
scores = []

trie = SuffixTree()

for trial in range(0,trials+1):
    
    '''
    requires take.db to be in the working folder
    '''
    # connect to the database
    con = sqlite3.connect('take.db')
    # get raw features
    tiles = pd.read_sql_query("SELECT * FROM cv_piece_raw", con)
    # do a one-hot encoding of string features
    tiles['v_top_skewed'] = tiles.v_skew == 'top_skewed'
    tiles.v_top_skewed = tiles.v_top_skewed.astype(int)
    tiles['v_symmetric'] = tiles.v_skew == 'symmetric'
    tiles.v_symmetric = tiles.v_symmetric.astype(int)
    tiles['v_bottom_skewed'] = tiles.v_skew == 'bottom-skewed'
    tiles.v_bottom_skewed = tiles.v_bottom_skewed.astype(int)
    tiles['h_top_skewed'] = tiles.h_skew == 'right_skewed'
    tiles.h_top_skewed = tiles.v_bottom_skewed.astype(int)
    tiles['h_symmetric'] = tiles.h_skew == 'symmetric'
    tiles.h_symmetric = tiles.v_bottom_skewed.astype(int)
    tiles['h_bottom_skewed'] = tiles.h_skew == 'left-skewed'
    tiles.h_bottom_skewed = tiles.v_bottom_skewed.astype(int)
    # now drop non-continious columns
    tiles.drop(['h_skew','v_skew','position'], 1, inplace=True)
    # add feature: eucliden distance from center
    center = (0,0)
    tiles['c_diff'] = tiles.apply(lambda x: distance.euclidean(center, (x['pos_x'], x['pos_y'])), axis=1)
    # obtain the referents
    targs = pd.read_sql_query("SELECT * FROM referent", con)
    targs.columns = ['episode_id', 'target']
    # this should result in a dataframe of the target objects' features
    query = '''
    SELECT tiles.* FROM
    targs 
    INNER JOIN
    tiles
    ON targs.episode_id = tiles.episode_id
    AND targs.target = tiles.id;
    '''
    targets = sqldf(query, locals())
    # this should result in a datafrom of the non-target (i.e., distractor) features
    query = '''
    SELECT tiles.* FROM
    tiles
    LEFT OUTER JOIN
    targs
    ON targs.episode_id = tiles.episode_id
    AND targs.target = tiles.id
    WHERE targs.target is null;
    '''
    non_targets = sqldf(query, locals())
    # obtain the referring expressions as utts
    utts = pd.read_sql_query("SELECT * FROM hand", con)
    
    print('training trie...')
    prev = ''
    for i,row in utts.iterrows():
        cur = row['episode_id']
        if cur != prev:
            trie.start_from_root()
        word = row['word']
        if word == '<sil>': continue
        trie.add(word)
        prev=cur
        
    # the result of this shuold be the words and corresponding object features for positive examples
    query = '''
    SELECT utts.word, utts.inc, targets.* FROM
    targets 
    INNER JOIN
    utts
    ON targets.episode_id = utts.episode_id
    '''
    positive = sqldf(query, locals())
    
    # the result of this shuold be the words and corresponding object features for negative examples
    query = '''
    SELECT utts.word, utts.inc, non_targets.* FROM
    non_targets 
    INNER JOIN
    utts
    ON non_targets.episode_id = utts.episode_id
    '''
    num_eval = 100
    negative = sqldf(query, locals())
    negative.drop_duplicates(subset=['inc', 'episode_id', 'id'], inplace=True)
    eids = set(positive.episode_id)
    
    test_eids = set(random.sample(eids, num_eval))
    train_eids = eids - test_eids
    positive_train = positive[positive.episode_id.isin(train_eids)]
    negative_train = negative[negative.episode_id.isin(train_eids)]
    words = list(set(utts.word))
    #words.sort()
    todrop = ['word', 'inc', 'episode_id', 'id']
    
    print('grounding nodes...')
    # now we finally use our data for training
    trie.set_grounded_data((positive_train,negative_train))
    trie.train_nodes()
    
    print('evaluating...')
    utts = pd.read_sql_query("SELECT * FROM hand", con)
    utts_eval = utts[utts.episode_id.isin(test_eids)]
    tiles_eval = tiles[tiles.episode_id.isin(test_eids)]
    # get obj features
    query = '''
    SELECT utts_eval.word, utts_eval.inc, tiles_eval.* FROM
    utts_eval
    INNER JOIN
    tiles_eval
    ON utts_eval.episode_id = tiles_eval.episode_id
    '''
    eval_data = sqldf(query, locals())
    
    corr = []
    for eid in test_eids:
        episode = eval_data[eval_data.episode_id == eid]
        if len(episode) == 0: continue
        for inc in list(set(episode.inc)):
            increment = episode[episode.inc == inc]
            word = increment.word.iloc[0] # all the words in the increment are the same, so just get the first one
            intents = increment.id
            feats = np.array(increment.drop(todrop, 1))
        #wac.compose_conn(list(zip(intents,feats)))
    s = sum(corr)/len(corr)
    print(s)
    scores.append(s)
    
print(np.mean(scores), len(scores))
print(np.std(scores))
