#create tokenized dictionary

def create_asymmetric_word_df(df, stop_words, punctuation, num_tokens):
    
     from nltk.tokenize import word_tokenize
     from nltk.stem import WordNetLemmatizer

     from numpy import savetxt

     from operator import itemgetter


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
         "cpc_subclass_id": "string",
         "filing_date": "string",
         "inventor_name": "string",
         "inventor_city": "string",
         "inventor_state": "string",
         "inventor_count": "string"
     }
 
     # Load designated csv to pd.DataFrame
     # print("loading df")
 
     # Tokenize words, ie split words in abstract into a list of space separated elements
     df['tokenized_abstract'] = df['patent_abstract'].apply(word_tokenize)
     patent_tokenized_dict = {}
 
     # Iterate the dataframe -> iterate words in df.tokenized_abstract -> check for uniqueness -> add to dict ||
     # increment existing key value pair for unique word.
     # print("iterating rows")
     for index, row in df.iterrows():
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
                         # print(lem_token[:-1], '<-', lem_token)
                     except KeyError:
                         pass
 
                 # Check if plural version is already in dictionary & replace it with singular version
                 elif lem_token[-1] != 's' and lem_token[-1] != 'd':
                     try:
                         removed_token_val = patent_tokenized_dict.pop(lem_token + 's')
                         patent_tokenized_dict[lem_token] = removed_token_val + 1
                         plural_flag = True
                         # print(lem_token + 's', '->', lem_token, 'removed token:', removed_token_val, ", new token:", patent_tokenized_dict[lem_token])
                         plural_count += 1
                     except KeyError:
                         pass
 
                     # Check for ends with d. I dont know what this is called. plurdal? ie. rated -> rate
                     try:
                         removed_token_val = patent_tokenized_dict.pop(lem_token + 'd')
                         patent_tokenized_dict[lem_token] = removed_token_val + 1
                         plural_flag = True
                         # print(lem_token + 'd', '->', lem_token, 'removed token:', removed_token_val, ", new token:", patent_tokenized_dict[lem_token])
                         plural_count += 1
                     except KeyError:
                         pass
 
                 # Probably want to add case for words ending with '-ing'. Pluringal?
 
                 # Probably want to add case for superlatives so ending with '-est'. Plurest?
 
                 # Probably want to add case for words ending with 'er'
 
                 # Fortunately, we're accessing a dictionary so we don't need to iterate through millions of elements like a list.
 
                 # If singular version doesnt exist, increment it.
                 if not plural_flag:
                     try:
                         patent_tokenized_dict[lem_token] += 1
                     except KeyError:
                         patent_tokenized_dict[lem_token] = 1
 
     # print(f"N lemmas: {n_count} A lemmas: {a_count}, R lemma: {r_count}, S lemmas: {s_count}")
     # print(f"Number of unique words: {len(patent_tokenized_dict)}")
     # print(f"Number of plural -> singular")
     
     sorted_tokens = dict(sorted(patent_tokenized_dict.items(), key=itemgetter(1), reverse=True)[:num_tokens])
     
     return sorted_tokens