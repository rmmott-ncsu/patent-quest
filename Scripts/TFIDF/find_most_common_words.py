import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import csv

from StopWords import stop_words_patent
from Dtype import dtype
from operator import itemgetter

# Have to download stopwords and punkt for nltk library to work correctly.
# Uncomment 4 lines below and run on it's own after pip install.

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

# stop_words = set(stopwords.words('english'))
# punctuation = "!@#$%^&*()_+-={[}]:;<,>.?/"
def get_word_count_for_df(df: pd.DataFrame):
    stop_words = set(stopwords.words('english'))
    stop_words.update(stop_words_patent)

    punctuation = "!@#$%^&*()_+-={[}]:;<,>.?/"

    # Variables for checking stuff on execution
    n_count = 0
    a_count = 0
    r_count = 0
    s_count = 0

    plural_count = 0

    lemmatizer = WordNetLemmatizer()  # Initialize lemmatizer to avoid ~duplicate~ words

    # Load designated csv to pd.DataFrame
    print("loading df")
    # df = pd.read_csv(path, dtype=dtype)
    df = df
    patent_tokenized_dict = {}
    doc_count_dict = {}


    # Tokenize words, ie split words in abstract into a list of space separated elements
    try:
        df['tokenized_abstract'] = df['patent_abstract'].apply(word_tokenize)
    except KeyError:
        print("did not work")

    # Iterate the dataframe -> iterate words in df.tokenized_abstract -> check for uniqueness -> add to dict ||
    # increment existing key value pair for unique word.
    print("iterating rows")
    for index, row in df.iterrows():
        word_set = set()
        for token in row["tokenized_abstract"]:
            token = token.lower()
            # lemmatize nouns -> adjective -> adverb -> satellite(?). Might be a more efficient way to do this/get
            # better results
            lem_token = lemmatizer.lemmatize(token, pos='n')
            n_count += 1
            if lem_token == token:
                lem_token = lemmatizer.lemmatize(token, pos='a')
                a_count += 1
            if lem_token == token:
                lem_token = lemmatizer.lemmatize(token, pos='r')
                r_count += 1
            if lem_token == token:
                lem_token = lemmatizer.lemmatize(token, pos='s')
                s_count += 1

            # Add word to dict if it's
            # 1) not a stop word
            # 2) not punctuation
            # 3) longer than 2 chars
            if lem_token not in stop_words and lem_token not in punctuation and len(lem_token) >= 3:
                plural_flag = False
                # Check if singular version of word is already in dictionary
                if lem_token[-1] == 's' or lem_token[-1] == 'd':
                    try:
                        a = patent_tokenized_dict[lem_token[:-1]]
                        patent_tokenized_dict[lem_token[:-1]] += 1
                        plural_flag = True
                        plural_count += 1
                        # print(lem_token[:-1], '<-', lem_token)

                        if lem_token[:-1] not in word_set and lem_token not in word_set:
                            try:
                                doc_count_dict[lem_token[:-1]] += 1
                                word_set.add(lem_token[:-1])
                            except KeyError:
                                pass

                    except KeyError:
                        pass

                # Check if key without '-ing' or '-ings' is already in dict
                elif lem_token[-3:] == 'ing' or lem_token[-4:] == 'ings':
                    try: # '-ings'
                        a = patent_tokenized_dict[lem_token[:-4]]
                        patent_tokenized_dict[lem_token[:-4]] += 1
                        plural_flag = True
                        plural_count += 1
                        # print(lem_token[:-4], '<-', lem_token)

                        if lem_token[-4:0] not in word_set and lem_token not in word_set:
                            try:
                                doc_count_dict[lem_token[:-4]] += 1
                                word_set.add(lem_token[:-4])
                            except KeyError:
                                pass
                    except KeyError:

                        try: # '-ing'
                            a = patent_tokenized_dict[lem_token[:-3]]
                            patent_tokenized_dict[lem_token[:-3]] += 1
                            plural_flag = True
                            plural_count += 1
                            # print(lem_token[:-3], '<-', lem_token)

                            if lem_token[:-3] not in word_set and lem_token not in word_set:
                                try:
                                    doc_count_dict[lem_token[:-3]] += 1
                                    word_set.add(lem_token[:-3])
                                except KeyError:
                                    pass
                        except KeyError:
                            pass


                # Check if plural version is already in dictionary & replace it with singular version
                elif lem_token[-1] != 's' and lem_token[-1] != 'd':
                    # -S
                    try:
                        removed_token_val = patent_tokenized_dict.pop(lem_token + 's')
                        patent_tokenized_dict[lem_token] = removed_token_val + 1
                        plural_flag = True
                        # print(lem_token + 's', '->', lem_token, 'removed token:', removed_token_val, ", new token:", patent_tokenized_dict[lem_token])
                        plural_count += 1

                        if lem_token + 's' not in word_set and lem_token not in word_set:
                            try:
                                removed_token_val = doc_count_dict.pop(lem_token + 's')
                                doc_count_dict[lem_token] = removed_token_val + 1
                                word_set.add(lem_token)
                            except KeyError:
                                pass

                    except KeyError:
                        pass

                    # -D
                    try:
                        removed_token_val = patent_tokenized_dict.pop(lem_token + 'd')
                        patent_tokenized_dict[lem_token] = removed_token_val + 1
                        plural_flag = True
                        # print(lem_token + 'd', '->', lem_token, 'removed token:', removed_token_val, ", new token:", patent_tokenized_dict[lem_token])
                        plural_count += 1

                        if lem_token + 'd' not in word_set and lem_token not in word_set:
                            try:
                                removed_token_val = doc_count_dict.pop(lem_token + 'd')
                                doc_count_dict[lem_token] = removed_token_val + 1
                                word_set.add(lem_token)
                            except KeyError:
                                pass
                    except KeyError:
                        pass

                # If singular version doesnt exist, increment it.
                if not plural_flag:
                    try:
                        patent_tokenized_dict[lem_token] += 1
                    except KeyError:
                        patent_tokenized_dict[lem_token] = 1

                    if lem_token not in word_set:
                        try:
                            doc_count_dict[lem_token] += 1
                            word_set.add(lem_token)
                        except KeyError:
                            doc_count_dict[lem_token] = 1
                            word_set.add(lem_token)

                # print(patent_tokenized_dict, doc_count_dict)


    print(f"N lemmas: {n_count} A lemmas: {a_count}, R lemma: {r_count}, S lemmas: {s_count}")
    print(f"Number of unique words: {len(patent_tokenized_dict)}")
    print(f"Number of plural -> singular")

    return patent_tokenized_dict, doc_count_dict


def get_word_count_for_df_chunk(df: pd.DataFrame):
    stop_words = set(stopwords.words('english'))
    punctuation = "!@#$%^&*()_+-={[}]:;<,>.?/"

    # Variables for checking stuff on execution
    n_count = 0
    a_count = 0
    r_count = 0
    s_count = 0

    plural_count = 0

    lemmatizer = WordNetLemmatizer()  # Initialize lemmatizer to avoid ~duplicate~ words

    # Load designated csv to pd.DataFrame
    print("loading df")
    # df = pd.read_csv(path, dtype=dtype)
    df = df
    patent_tokenized_dict = {}
    doc_count_dict = {}

    for chunk in df:
    # Tokenize words, ie split words in abstract into a list of space separated elements
        chunk['tokenized_abstract'] = chunk['patent_abstract'].apply(word_tokenize)

    # Iterate the dataframe -> iterate words in df.tokenized_abstract -> check for uniqueness -> add to dict ||
    # increment existing key value pair for unique word.
        print("iterating rows")
        for index, row in chunk.iterrows():
            word_set = set()
            for token in row["tokenized_abstract"]:
                token = token.lower()
                # lemmatize nouns -> adjective -> adverb -> satellite(?). Might be a more efficient way to do this/get
                # better results
                lem_token = lemmatizer.lemmatize(token, pos='n')
                n_count += 1
                if lem_token == token:
                    lem_token = lemmatizer.lemmatize(token, pos='a')
                    a_count += 1
                if lem_token == token:
                    lem_token = lemmatizer.lemmatize(token, pos='r')
                    r_count += 1
                if lem_token == token:
                    lem_token = lemmatizer.lemmatize(token, pos='s')
                    s_count += 1

                # Add word to dict if it's
                # 1) not a stop word
                # 2) not punctuation
                # 3) longer than 2 chars
                if lem_token not in stop_words and lem_token not in punctuation and len(lem_token) >= 3:
                    plural_flag = False
                    # Check if singular version of word is already in dictionary
                    if lem_token[-1] == 's' or lem_token[-1] == 'd':
                        try:
                            a = patent_tokenized_dict[lem_token[:-1]]
                            patent_tokenized_dict[lem_token[:-1]] += 1
                            plural_flag = True
                            plural_count += 1
                            # print(lem_token[:-1], '<-', lem_token)

                            if lem_token[:-1] not in word_set and lem_token not in word_set:
                                try:
                                    doc_count_dict[lem_token[:-1]] += 1
                                    word_set.add(lem_token[:-1])
                                except KeyError:
                                    pass

                        except KeyError:
                            pass

                    # Check if key without '-ing' or '-ings' is already in dict
                    elif lem_token[-3:] == 'ing' or lem_token[-4:] == 'ings':
                        try: # '-ings'
                            a = patent_tokenized_dict[lem_token[:-4]]
                            patent_tokenized_dict[lem_token[:-4]] += 1
                            plural_flag = True
                            plural_count += 1
                            # print(lem_token[:-4], '<-', lem_token)

                            if lem_token[-4:0] not in word_set and lem_token not in word_set:
                                try:
                                    doc_count_dict[lem_token[:-4]] += 1
                                    word_set.add(lem_token[:-4])
                                except KeyError:
                                    pass
                        except KeyError:

                            try: # '-ing'
                                a = patent_tokenized_dict[lem_token[:-3]]
                                patent_tokenized_dict[lem_token[:-3]] += 1
                                plural_flag = True
                                plural_count += 1
                                # print(lem_token[:-3], '<-', lem_token)

                                if lem_token[:-3] not in word_set and lem_token not in word_set:
                                    try:
                                        doc_count_dict[lem_token[:-3]] += 1
                                        word_set.add(lem_token[:-3])
                                    except KeyError:
                                        pass
                            except KeyError:
                                pass


                    # Check if plural version is already in dictionary & replace it with singular version
                    elif lem_token[-1] != 's' and lem_token[-1] != 'd':
                        # -S
                        try:
                            removed_token_val = patent_tokenized_dict.pop(lem_token + 's')
                            patent_tokenized_dict[lem_token] = removed_token_val + 1
                            plural_flag = True
                            # print(lem_token + 's', '->', lem_token, 'removed token:', removed_token_val, ", new token:", patent_tokenized_dict[lem_token])
                            plural_count += 1

                            if lem_token + 's' not in word_set and lem_token not in word_set:
                                try:
                                    removed_token_val = doc_count_dict.pop(lem_token + 's')
                                    doc_count_dict[lem_token] = removed_token_val + 1
                                    word_set.add(lem_token)
                                except KeyError:
                                    pass

                        except KeyError:
                            pass

                        # -D
                        try:
                            removed_token_val = patent_tokenized_dict.pop(lem_token + 'd')
                            patent_tokenized_dict[lem_token] = removed_token_val + 1
                            plural_flag = True
                            # print(lem_token + 'd', '->', lem_token, 'removed token:', removed_token_val, ", new token:", patent_tokenized_dict[lem_token])
                            plural_count += 1

                            if lem_token + 'd' not in word_set and lem_token not in word_set:
                                try:
                                    removed_token_val = doc_count_dict.pop(lem_token + 'd')
                                    doc_count_dict[lem_token] = removed_token_val + 1
                                    word_set.add(lem_token)
                                except KeyError:
                                    pass
                        except KeyError:
                            pass

                    # If singular version doesnt exist, increment it.
                    if not plural_flag:
                        try:
                            patent_tokenized_dict[lem_token] += 1
                        except KeyError:
                            patent_tokenized_dict[lem_token] = 1

                        if lem_token not in word_set:
                            try:
                                doc_count_dict[lem_token] += 1
                                word_set.add(lem_token)
                            except KeyError:
                                doc_count_dict[lem_token] = 1
                                word_set.add(lem_token)

                    # print(patent_tokenized_dict, doc_count_dict)


    print(f"N lemmas: {n_count} A lemmas: {a_count}, R lemma: {r_count}, S lemmas: {s_count}")
    print(f"Number of unique words: {len(patent_tokenized_dict)}")
    print(f"Number of plural -> singular")

    return patent_tokenized_dict, doc_count_dict
