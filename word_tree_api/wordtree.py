
# import nltk
# nltk.download('punkt') # for sent_tokenize
# nltk.download('stopwords') 
# nltk.download('wordnet') # for WordNetLemmatizer

import pandas as pd
import numpy as np

# Text preprocessing/analysis
import re
from nltk import word_tokenize, sent_tokenize, FreqDist
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from itertools import groupby 


from datetime import datetime, timedelta

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

def generate_token(reviews):
    """Takes a list of documents and joins them together, before creating a giant lemmatized list of tokens"""
    combined_strings = " ".join(list(reviews))

    tokeniser = RegexpTokenizer("[A-Za-z\']+|\.")
    tokens = tokeniser.tokenize(combined_strings)
    
    # Remove repeat
    deduped_tokens = [i[0] for i in groupby(tokens)]
    
    lemmatiser = WordNetLemmatizer()
    tokens_norm = [lemmatiser.lemmatize(t.lower(), "v") for t in deduped_tokens]
    
    return tokens_norm

def get_word_tree(tokens):
    """
    Takes a list of tokens and returns a function that takes an optional 
    string which will be searched for for particular n-grams
    """

    #remove all grams starting with period
    def _clean_grams(ngram_counter):
        begins_with_period = []
        for gram in ngram_counter:
            if gram[0] == '.':
                begins_with_period.append(gram)
        for gram in begins_with_period:
            del ngram_counter[gram]

    def _word_tree(head=None, show_count=20, trailing=2, direction='forward', levels=0, indent=0):
        if type(head)==str:
            head = head.lower().split()
        trailing_grams = trailing 
        if head != None:
            trailing_grams += len(head)
        if head==None:
            ngram_counter = Counter(ngrams(tokens, trailing_grams))
        else:
            if direction == 'forward':
                ngram_counter = Counter([gram for gram in ngrams(tokens, trailing_grams) if gram[:len(head)] == tuple(head)])
            elif direction == 'backward':
                ngram_counter = Counter([gram for gram in ngrams(tokens, trailing_grams) if gram[-len(head):] == tuple(head)])
            else:
                ngram_counter = Counter([gram for gram in ngrams(tokens, trailing_grams) if gram[:len(head)] == tuple(head)])

        _clean_grams(ngram_counter)
        
        for (text, idx) in ngram_counter.most_common(show_count):
            print(f"{'  '*indent}{idx} - {' '.join(text)}")
            if levels > 0 and idx > 3:
                _word_tree(text, show_count=3, trailing=2, direction=direction, levels=levels-1, indent=indent+1)

    return _word_tree
  
