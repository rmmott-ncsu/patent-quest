import csv
import math
import operator

from Query import query
from find_most_common_words import get_word_count_for_df
from CPC_codes import CPC_CODES


# Open CSV for common word counts & document occurence
# Generate this CSV with get_word_count.py
def get_super_word_count(path: str) -> dict:
    super_dict = dict()
    with open(path, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            super_dict[row['token']] = [row['count'], row['doc_count']]
    return super_dict

# Term frequency
def tf(num_times_in_doc: int, num_terms_in_doc: int)->float:
    #print(num_times_in_doc, num_terms_in_doc)
    return num_times_in_doc/num_terms_in_doc

# inverse document frequency
def idf(num_docs_in_corpus: int, num_docs_w_term: int)->float:
    #print(num_docs_in_corpus, num_docs_w_term)
    return math.log2(num_docs_in_corpus/num_docs_w_term)

# term frequency * inverse document frequency
def tf_idf_calc(num_times_in_doc: int, num_terms_in_doc: int, num_docs_in_corpus: int, num_docs_w_term: int)-> float:
    return tf(num_times_in_doc, num_terms_in_doc) * idf(num_docs_in_corpus, num_docs_w_term)

# Calculate tf-idf of cpc where all abstracts with given cpc are a 'document' and the corpus is the whole training data set
def calculate_tf_idf_by_cpc(word_count_doc: str, num_docs_in_corpus: int=164523):

    term = 0
    code_dict = {}
    # Load csv to dict
    with open(word_count_doc,'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        super_dict = {rows[0]: [rows[1], rows[2]] for rows in reader}

    # iterate through cpc codes
    for code in CPC_CODES:
        word_dict = dict()
        term += 1
        query_df = query(code, '')
        tokenized_dict, doc_count_dict = get_word_count_for_df(query_df)

        for word in tokenized_dict:
            try:
                num_docs_with_term = int(super_dict[word][1])
            except KeyError:
                num_docs_with_term = 1
            num_terms_in_doc = int(len(tokenized_dict))
            num_times_in_doc = int(tokenized_dict[word])

            calc = tf_idf_calc(num_times_in_doc, num_terms_in_doc, num_docs_in_corpus, num_docs_with_term)
            # print(word, num_times_in_doc, num_terms_in_doc, num_docs_in_corpus, num_docs_with_term)
            word_dict[word] = calc
        sorted_tokens = dict(sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)[:100])
        code_dict[code] = sorted_tokens

    return code_dict

# Get set of unique words by pulling keys from dict and adding to set
def get_word_set(dict:dict) -> set:
    word_set = set()
    for code in dict:
        for key in dict[code].keys():
            word_set.add(key)

    return word_set

def build_tfidf_dict(code_dict, word_list: set):
    tf_idf_dict_list = list()
    for code in code_dict:
        tf_idf_dict = dict()
        tf_idf_dict['cpc'] = code

        for word in word_list:
            try:
                tf_idf_dict[word] = code_dict[code][word]
            except KeyError:
                tf_idf_dict[word] = 0

        tf_idf_dict_list.append(tf_idf_dict)

    return tf_idf_dict_list

# Create CSV file ->
def build_tfidf_csv(tfidf_dict_list: list, tf_idf_doc: str):
    column = ['cpc']
    with open(tf_idf_doc, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, tfidf_dict_list[0].keys())
        writer.writeheader()
        writer.writerows(tfidf_dict_list)

# Need to have created word count csv prior with get_word_count.py
# Outputs csv of each CPC and their tf-idf for each word.
def main():
    # Get top 100 words for each CPC by tf-idf
    code_dict = calculate_tf_idf_by_cpc('word_count_2020.csv', 353661)

    # Create set of unique words for ALL cpc's
    # This essentailly amounts to feature reduction by taking the top 100 words from each CPC rather than ALL words in corpus
    high_tfidf_word_set = get_word_set(code_dict)

    # Create list of dict objects for each cpc with each word in word set.
    tfidf_dict_list = build_tfidf_dict(code_dict, high_tfidf_word_set)

    # Dump list of dicts to CSV for use in predict.py
    build_tfidf_csv(tfidf_dict_list, 'tfidf_calc_2020.csv')


main()
