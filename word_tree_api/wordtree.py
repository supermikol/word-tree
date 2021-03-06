
from typing import (
  List,
  Dict
)
import pandas as pd
import numpy as np

# Text preprocessing/analysis
import re
from nltk import (
  word_tokenize, 
  sent_tokenize, 
  FreqDist
)
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from itertools import groupby 


from datetime import (
  datetime, 
  timedelta
)

# import io
import json
import os
import glob
# import base64

def get_paths(pathname):
    return sorted([os.path.join(pathname, f) for f in os.listdir(pathname)])

def read_files(files, separator=','):
    """
    Takes a list of pathnames and individually reads then concats them into a single DataFrame which is returned.
    Can handle Excel files, csv, or delimiter separated text.
    """
    processed_files = []
    for file in files:
        if file.lower().endswith('.xlsx') or file.lower().endswith('.xls'):
            processed_files.append(pd.read_excel(file, engine='openpyxl', index_col=None, header=0))
        elif file.lower().endswith('.csv'):
            processed_files.append(pd.read_csv(file, index_col=None, header=0))
        else:
            processed_files.append(pd.read_csv(file, sep=separator, index_col=None, header=0))
    completed_df = pd.concat(processed_files, ignore_index=True)
    return completed_df


class WordTree:
    """
    Takes a list of reviews and returns an object that can be searched for n-grams frequency
    """
    def __init__(self, tokens: List[List[str]]):
        # self.tokens = WordTree.generate_token(reviews)
        self.tokens = tokens
        self.word_tree = None
        self.ngram_database = {}

    def _clean_grams(self, ngram_counter):
        to_ignore_terms = ['eol']
        to_delete = []
        for gram in ngram_counter:
            if gram[0] == '.': # starts with '.'
                to_delete.append(gram)
            # if any(v in gram for v in to_ignore_terms): # cut after to ignore
            #     to_delete.append(gram)
        for gram in to_delete:
            del ngram_counter[gram]

    def get_most_frequent(self, max_grams=6, show_count=18):
        results = []
        for counter_length in range(2,max_grams+1):
            ngram_counter = Counter(ngrams(self.tokens, counter_length))
            self._clean_grams(ngram_counter)
            results.append(ngram_counter.most_common(show_count))
        return results

    def train_and_print(self, head=None, trailing_grams=2, nested_trailing_grams=3, direction='forward', show_count = 20, indent=0, levels=0):
        if levels==-1:
            return []
        if head==None:
            head = []
        if type(head)==str:
            head = head.lower().split()
        if head != None:
            trailing_grams += len(head)
        key_pattern = ((' ').join(head), trailing_grams, direction)
        if key_pattern in self.ngram_database.keys():
            ngram_counter = self.ngram_database[key_pattern]
        else:
            if len(head)==0:
                ngram_counter = Counter(ngrams(self.tokens, trailing_grams))
                ngram_counter_backward = Counter(ngrams(self.tokens, trailing_grams))
            else:
                ngram_counter = Counter([gram for gram in ngrams(self.tokens, trailing_grams) if gram[:len(head)] == tuple(head)])
                ngram_counter_backward = Counter([gram for gram in ngrams(self.tokens, trailing_grams) if gram[-len(head):] == tuple(head)])

        self._clean_grams(ngram_counter)
        self._clean_grams(ngram_counter_backward)

        # self.ngram_database[key_pattern] = ngram_counter # will take up too much memory, so disabling; hit rates will likely be low
        result = [
            [
                [
                    counter[1],
                    counter[0],
                ] for counter in ngram_counter.most_common(show_count)
            ],
            [
                [
                    counter[1],
                    counter[0],
                ] for counter in ngram_counter_backward.most_common(show_count)
            ]
        ]
        return result
    
    def __repr__(self):
        ngrams_list = [i for i in self.ngram_database.keys()]
        return 'Length: %d words \n ngrams: %s' % (len(self.tokens), ngrams_list)

    @staticmethod
    def generate_token(reviews) -> List[str]:
        """Takes a string of text and creates a giant lemmatized list of tokens"""
        # combined_strings = " ".join(list(reviews))
        tokeniser = RegexpTokenizer("[A-Za-z\']+|\.")
        # tokens = tokeniser.tokenize(combined_strings)
        tokens = tokeniser.tokenize(reviews)
        # Remove repeat
        deduped_tokens = [i[0] for i in groupby(tokens)]
        
        lemmatiser = WordNetLemmatizer()
        tokens_norm = [lemmatiser.lemmatize(t.lower(), "v") for t in deduped_tokens]
        
        return tokens_norm
