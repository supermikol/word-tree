from word_tree_api.wordtree import get_paths, read_files, generate_token, get_word_tree


# DATA_DIR = './data/bed_pillow_reviews/1-Beckham/'
DATA_DIR = './data/bed_pillow_reviews/2-down alt/'
all_files = get_paths(DATA_DIR)


pillow_reviews = read_files(all_files)

prod_1 = pillow_reviews[pillow_reviews['Variation'] == 'B01LYNW421']
prod_1_good = prod_1[prod_1['Rating'] >= 4]
prod_1_bad = prod_1[prod_1['Rating'] <= 3]

prod_1_good_reviews = prod_1_good.reset_index()['Body']
prod_1_bad_reviews = prod_1_bad.reset_index()['Body']

TEXT_TO_ANALYZE = prod_1_bad_reviews

word_tree = get_word_tree(generate_token(TEXT_TO_ANALYZE))


results = word_tree(None, show_count=15, trailing=4, direction='forward', levels=4)
print(results)