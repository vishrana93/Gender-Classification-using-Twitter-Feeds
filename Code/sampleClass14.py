
# coding: utf-8

# In[10]:

# Import all packages

import requests
import ConfigParser
from TwitterAPI import TwitterAPI
import sys
from collections import Counter
import pickle
import re
from itertools import product
import nltk
from nltk.corpus import stopwords
from collections import defaultdict
from scipy.sparse import lil_matrix

class sampleClass14:

    def __init__(self):
            print 

    def get_census_names(self):
        males = requests.get('http://www2.census.gov/topics/genealogy/1990surnames/dist.male.first').text.split('\n')
        females = requests.get('http://www2.census.gov/topics/genealogy/1990surnames/dist.female.first').text.split('\n')
        males_pct = dict([(m.split()[0].lower(), float(m.split()[1])) for m in males if m])
        females_pct = dict([(f.split()[0].lower(), float(f.split()[1])) for f in females if f])
        male_names = set([m for m in males_pct if m not in females_pct or males_pct[m] > females_pct[m]])
        female_names = set([f for f in females_pct if f not in males_pct or females_pct[f] > males_pct[f]]) 
        return male_names, female_names
    
    def get_first_name(self,tweet):
        if 'user' in tweet and 'name' in tweet['user']:
            parts = tweet['user']['name'].split()
            if len(parts) > 0:
                return parts[0].lower()
            
    
    def make_feature_matrix(self,tokens_list, vocabulary,len_tweets):
        X = lil_matrix((len_tweets, len(vocabulary)))
        for i, tokens in enumerate(tokens_list):
            for token in tokens:
                j = vocabulary[token]
                X[i,j] += 1
        return X.tocsr()
    
    def tokenize(self,string, lowercase, keep_punctuation, prefix,collapse_urls, collapse_mentions,collapse_stop_words):
        if not string:
            return []
        if lowercase:
            string = string.lower()
        tokens = []
        if collapse_urls:
            string = re.sub('http\S+', 'THIS_IS_A_URL', string)
        if collapse_mentions:
            string = re.sub('@\S+', 'THIS_IS_A_MENTION', string)
        if keep_punctuation:
            tokens = string.split()
        else:
            tokens = re.sub('\W+', ' ', string).split()
        if collapse_stop_words:
            tokens = list(set(tokens) - set(stopwords.words('english')))
        if prefix:
            tokens = ['%s%s' % (prefix, t) for t in tokens]
        return tokens
    
    def tweet2tokens(self,tweet, use_descr=True, lowercase=True,keep_punctuation=True, descr_prefix='d=',
                 collapse_urls=True, collapse_mentions=True, use_text=True,collapse_stop_words = True):
        tokens = []
        if use_text:
            tokens.extend(self.tokenize(tweet['text'], lowercase, keep_punctuation, None,collapse_urls, collapse_mentions,collapse_stop_words))
        if use_descr:
            tokens.extend(self.tokenize(tweet['user']['description'], lowercase,keep_punctuation, descr_prefix,collapse_urls, collapse_mentions,collapse_stop_words))
        return tokens
    
    def make_vocabulary(self,tokens_list):
        vocabulary = defaultdict(lambda: len(vocabulary)) # Similar to vocabulary = defaultdict(int)
        for tokens in tokens_list:
            for token in tokens:
                vocabulary[token]
        print '%d unique terms in vocabulary' % len(vocabulary)
        return vocabulary
    
    def get_gender(self,tweet, male_names, female_names):
        name = self.get_first_name(tweet)
        if name in female_names:
            return 1
        elif name in male_names:
            return 0
        else:
            return -1

