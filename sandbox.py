from itertools import tee
from word_tree_api.wordtree import get_paths, read_files, WordTree


DATA_DIR = './data/bed_pillow_reviews/1-Beckham/'
# DATA_DIR = './data/bed_pillow_reviews/2-down alt/'
all_files = get_paths(DATA_DIR)


pillow_reviews = read_files(all_files)

prod_1 = pillow_reviews[pillow_reviews['Variation'] == 'B01LYNW421']
prod_1_good = prod_1[prod_1['Rating'] >= 4]
prod_1_bad = prod_1[prod_1['Rating'] <= 3]

prod_1_good_reviews = prod_1_good.reset_index()['Body']
prod_1_bad_reviews = prod_1_bad.reset_index()['Body']

TEXT_TO_ANALYZE = prod_1_bad_reviews

wordtree_tokens = WordTree.generate_token(TEXT_TO_ANALYZE)
word_tree = WordTree(wordtree_tokens) # takes list of documents/reviews
word_tree.train_and_print()
word_tree.train_and_print('this pillow', levels=1)

