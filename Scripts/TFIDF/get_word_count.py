import pandas as pd
import csv

from find_most_common_words import get_word_count_for_df_chunk
from Dtype import dtype

# Generate CSV -> token, count, doc_count
# where token is a lemmatized word, count is the number of times it appears in a file (corpus), and doc count is
# the number of documents (individual patent abstracts) it appears in.
# Used for TF-IDF calculations in tf-idf.py
def get_word_count_for_file(path: str):
    # Create dictionary where key = token and value = number of times it occurs
    df = pd.read_csv(path, dtype=dtype, chunksize=10000)
    tokenized_dict, doc_count_dict = get_word_count_for_df_chunk(df)
    csv_list = []

    for token in tokenized_dict:
        try:
            dict = {'token': token, 'count': tokenized_dict[token], 'doc_count': doc_count_dict[token]}
        except KeyError:
            print('Error', token)
            print(token, )
        csv_list.append(dict)
    with open('word_count_2020.csv', 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, csv_list[0].keys())
        writer.writeheader()
        for word in csv_list:
            try:
                writer.writerow(word)
            except KeyError:
                print('Error', word)