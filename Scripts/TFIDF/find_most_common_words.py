import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import csv

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
    stop_words_patent = {'first', 'second', 'include', 'device', 'one', 'system',
     'method', 'data', 'least', 'base', 'may', 'provide',
     'configure', 'plurality', 'portion', 'method',
     'surface', 'unit', 'information', 'user', 'image',
     'control', 'including', 'element', 'includes', 'configured',
     'based', 'provided', 'receive', 'end', 'apparatus', 'member',
     'body', 'wherein', 'use', 'comprise', 'present', 'set',
     'communication', 'determine', 'using', 'position', 'also',
     'structure', 'region', 'side', 'part', 'comprising',
     'assembly', 'direction', 'value', 'connected', 'embodiment',
     'associate', 'disclose', 'output', 'input', 'component',
     'invention', 'comprises', 'consisting', 'associate',
     'couple', 'within', 'disclosed', 'relate', 'far', 'formed',
     'two', 'operation', 'receiving', 'module', 'coupled',
     'associated', 'dispose', 'object', 'area', 'section',
     'process', 'disposed', 'provides', 'resulting', 'capable',
     'example', 'response', 'via', 'response', 'along',
     'determining', 'operating', 'relative', 'define',
     'operating', 'location', 'acceptable', 'thereof',
     'composition', 'relates', 'attached', 'specifically',
     'described', 'and/or', 'herein', 'containing', 'housing',
     'container', 'positioned', 'particular', 'received',
     'whether', 'receives', 'corresponding', 'identifying',
     'identified', 'determined', 'according', 'selected',
     'determines', 'according', 'whether', 'respective',
     'different', 'forming', 'arrange', 'amount', 'generate'
                                                  'determination', 'third', 'different', 'inside',
     'outside', 'opening', 'arranged', 'near', 'exemplary',
     'type', 'interior', 'exterior', 'edge', 'size', 'various',
     'significant', 'generate', 'generating', 'among', 'cause',
     'presented', 'layer', 'model', 'disclosure', 'e.g.',
     'producing', 'nearly', 'allows', 'produced', 'increase'
                                                  'following', 'generally', 'preparing', 'another',
     'thus', 'new'}
    stop_words.update(stop_words_patent)


    punctuation = "!@#$%^&*()_+-={[}]:;<,>.?/"

    # Variables for checking stuff on execution
    n_count = 0
    a_count = 0
    r_count = 0
    s_count = 0

    plural_count = 0

    lemmatizer = WordNetLemmatizer()  # Initialize lemmatizer to avoid ~duplicate~ words

    # Doesn't like non-explicit data types. Might be able to get some performance improvements by changing some of these
    dtype = {
        "patent_id": int,
        "patent_title": "string",
        "patent_date": "string",
        "patent_abstract": "string",
        "application_id": "string",
        "application_filing_date": "string",
        "applicant_name": "string",
        "applicant_organization": "string",
        "assignee_name": "string",
        "assignee_org_name": "string",
        "cpc_class_id": "string",
        "cpc_subclass_id": "string",
        "cpc_group_id": "string",
        "filing_date": "string",
        "inventor_name": "string",
        "inventor_city": "string",
        "inventor_state": "string",
        "inventor_count": "string"
    }

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

    # Doesn't like non-explicit data types. Might be able to get some performance improvements by changing some of these
    dtype = {
        "patent_id": int,
        "patent_title": "string",
        "patent_date": "string",
        "patent_abstract": "string",
        "application_id": "string",
        "application_filing_date": "string",
        "applicant_name": "string",
        "applicant_organization": "string",
        "assignee_name": "string",
        "assignee_org_name": "string",
        "cpc_class_id": "string",
        "cpc_subclass_id": "string",
        "cpc_group_id": "string",
        "filing_date": "string",
        "inventor_name": "string",
        "inventor_city": "string",
        "inventor_state": "string",
        "inventor_count": "string"
    }

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

def create_asymmetric_word_df(path: str):
    # Variables for checking stuff on execution
    n_count = 0
    a_count = 0
    r_count = 0
    s_count = 0

    plural_count = 0

    lemmatizer = WordNetLemmatizer()  # Initialize lemmatizer to avoid ~duplicate~ words

    # Doesn't like non-explicit data types. Might be able to get some performance improvements by changing some of these
    dtype = {
        "patent_id": int,
        "patent_title": "string",
        "patent_date": "string",
        "patent_abstract": "string",
        "application_id": "string",
        "application_filing_date": "string",
        "applicant_name": "string",
        "applicant_organization": "string",
        "assignee_name": "string",
        "assignee_org_name": "string",
        "cpc_class_id": "string",
        "cpc_subclass_id": "string",
        "cpc_group_id": "string",
        "filing_date": "string",
        "inventor_name": "string",
        "inventor_city": "string",
        "inventor_state": "string",
        "inventor_count": "string"
    }

    # Load designated csv to pd.DataFrame
    print("loading df")
    # df = pd.read_csv(path, dtype=dtype)
    df = pd.read_csv(path, dtype=dtype, chunksize=10000)
    patent_tokenized_dict = {}
    for chunk in df:
    # Tokenize words, ie split words in abstract into a list of space separated elements
        chunk['tokenized_abstract'] = chunk['patent_abstract'].apply(word_tokenize)


    # Iterate the dataframe -> iterate words in df.tokenized_abstract -> check for uniqueness -> add to dict ||
    # increment existing key value pair for unique word.
        print("iterating rows")
        for index, row in chunk.iterrows():
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
                            patent_tokenized_dict[lem_token[:-1]] += 1
                            plural_flag = True
                            plural_count += 1
                            print(lem_token[:-1], '<-', lem_token)
                        except KeyError:
                            pass

                    # Check if key without '-ing' or '-ings' is already in dict
                    elif lem_token[-3:] == 'ing' or lem_token[-4:] == 'ings':
                        try: # '-ings'
                            patent_tokenized_dict[lem_token[-4:]] += 1
                            plural_flag = True
                            plural_count += 1
                            print(lem_token[:-4], '<-', lem_token)
                        except KeyError:

                            try: # '-ing'
                                patent_tokenized_dict[lem_token[-3:]] += 1
                                plural_flag = True
                                plural_count += 1
                                print(lem_token[:-3], '<-', lem_token)
                            except KeyError:
                                pass


                    # Check if plural version is already in dictionary & replace it with singular version
                    elif lem_token[-1] != 's' and lem_token[-1] != 'd':
                        # -S
                        try:
                            removed_token_val = patent_tokenized_dict.pop(lem_token + 's')
                            patent_tokenized_dict[lem_token] = removed_token_val + 1
                            plural_flag = True
                            print(lem_token + 's', '->', lem_token, 'removed token:', removed_token_val, ", new token:", patent_tokenized_dict[lem_token])
                            plural_count += 1
                        except KeyError:
                            pass

                        # -D
                        try:
                            removed_token_val = patent_tokenized_dict.pop(lem_token + 'd')
                            patent_tokenized_dict[lem_token] = removed_token_val + 1
                            plural_flag = True
                            print(lem_token + 'd', '->', lem_token, 'removed token:', removed_token_val, ", new token:", patent_tokenized_dict[lem_token])
                            plural_count += 1
                        except KeyError:
                            pass

                        # -ING


                    # Probably want to add case for superlatives so ending with '-est'. Plurest?

                    # Probably want to add case for words ending with 'er'

                    # Fortunately, we're accessing a dictionary so we don't need to iterate through millions of elements like a list.



                    # If singular version doesnt exist, increment it.
                    if not plural_flag:
                        try:
                            patent_tokenized_dict[lem_token] += 1
                        except KeyError:
                            patent_tokenized_dict[lem_token] = 1

    print(f"N lemmas: {n_count} A lemmas: {a_count}, R lemma: {r_count}, S lemmas: {s_count}")
    print(f"Number of unique words: {len(patent_tokenized_dict)}")
    print(f"Number of plural -> singular")
    return patent_tokenized_dict

def get_word_count_for_file(path):
    dtype = {
        "patent_id": int,
        "patent_title": "string",
        "patent_date": "string",
        "patent_abstract": "string",
        "application_id": "string",
        "application_filing_date": "string",
        "applicant_name": "string",
        "applicant_organization": "string",
        "assignee_name": "string",
        "assignee_org_name": "string",
        "cpc_class_id": "string",
        "cpc_subclass_id": "string",
        "cpc_group_id": "string",
        "filing_date": "string",
        "inventor_name": "string",
        "inventor_city": "string",
        "inventor_state": "string",
        "inventor_count": "string"
    }
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
    with open('word_count_2020.csv', 'w', encoding='utf-8',newline='') as outfile:
        writer = csv.DictWriter(outfile, csv_list[0].keys())
        writer.writeheader()
        for word in csv_list:
            try:
                writer.writerow(word)
            except KeyError:
                print('Error', word)

# get_word_count_for_file('patents_csv/patents_2020.csv')
# Sort tokens into dict of num_tokens number of tokens that occur the most frequently
# print("sorting")
# num_tokens = 50
# sorted_tokens = dict(sorted(tokenized_dict.items(), key=itemgetter(1), reverse=True)[:num_tokens])
# print(sorted_tokens)