#search script

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from operator import itemgetter

from wordcloud import WordCloud

# Have to download stopwords and punkt for nltk library to work correctly.
# Uncomment 4 lines below and run on it's own after pip install.

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

##############################################################################
#user inputs
#this will ultimately structured as a function with 12 inputs
##############################################################################

begin_day = 11
begin_month = 1
begin_year = 2020
end_day = 5
end_month = 3
end_year = 2022


assignee_search = 'tesla'
inventor_search = ''
country_search = ''
state_search = ''
city_search = ''
cpc_search = ''

##############################################################################
#assign logic parameters for search for use in if/then statements later
##############################################################################

if assignee_search == '':
   assignee_search_log = 'False'
else:
   assignee_search_log = 'True'
    
if inventor_search == '':
   inventor_search_log = 'False'
else:
   inventor_search_log = 'True'

if country_search == '':
   country_search_log = 'False'
else:
   country_search_log = 'True'

if state_search == '':
   state_search_log = 'False'
else:
   state_search_log = 'True'

if city_search == '':
   city_search_log = 'False'
else:
   city_search_log = 'True'

if cpc_search == '':
   cpc_search_log = 'False'
else:
   cpc_search_log = 'True'

###############################################################################
#create array of dates based on the specified date range by finding ALL dates
#that were between 2013 and 2023, and then taking only the ones specified
###############################################################################

begin_date = str(begin_year) + '-' + str(begin_month) + '-' + str(begin_day) 
end_date = str(end_year) + '-' + str(end_month) + '-' + str(end_day) 

days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
days_with_zero = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
months_with_zero = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

num_days = len(days)
num_months = len(months)
num_years = len(years)

dates = []
dates_with_zero = []
z = 0

while z < 2:
    
    if z == 1:
        months = months_with_zero
        days = days_with_zero
    else:
        pass
    
    for y in years:
        current_year = y
        for m in months:
            current_month = m
            for d in days:
                current_day = d
                
                current_date = str(current_year) + '-' + str(current_month) + '-' + str(current_day)
                if z == 1:
                    dates_with_zero.append(current_date)    
                else:
                    dates.append(current_date)
    
    begin_index = 0
    end_index = 0
    
    for x in dates:    
        if begin_date != x:
            begin_index = begin_index+1
        else:
            break
    
    for w in dates:    
        if end_date != w:
            end_index = end_index+2
        else:
            break
    z = z+1

date_search = dates[begin_index:end_index]
date_search_with_zero = dates_with_zero[begin_index:end_index]
date_search.extend(date_search_with_zero)

###############################################################################
#separate the numbers of years searched for the purpose of reading .csv files
###############################################################################

year_range = end_year - begin_year
years_mat = np.linspace(begin_year, end_year, year_range+1, dtype=int)
response_query = []

for y in years_mat:
    
###############################################################################
#for each .csv, read in chunks of 10,000 rows at a time, for memory management
###############################################################################
    
    # Returns a TextFileReader, which is iterable with chunks of 10000 rows.
    filename = 'patents_' + str(y) + '.csv'
    csv_iterator = pd.read_csv(filename, iterator=True, chunksize=1000)
    
    # Iterate through the dataframe chunks
    for chunk in csv_iterator:
        for index, row in chunk.iterrows():

###############################################################################
#if a given row is responsive to the date range, check fields for hits
###############################################################################
    
            
            if row['patent_date'] in date_search:
                
                assignee = row['assignee_org_name']
                inventor = row['inventor_name']
                country = row['inventor_country']
                state = row['inventor_state']
                city = row['inventor_city']
                cpc = row['cpc_group_id']    
                
                if assignee_search_log == 'False' or (assignee_search_log == 'True' and isinstance(assignee, str) and assignee_search.lower() in assignee.lower()):                    
                   
                    if inventor_search_log == 'False' or (inventor_search_log == 'True' and isinstance(inventor, str) and inventor_search.lower() in inventor.lower()):
                       
                        if country_search_log == 'False' or (country_search_log == 'True' and isinstance(country, str) and country_search.lower() in country.lower()):
                          
                            if state_search_log == 'False' or (state_search_log == 'True' and isinstance(state, str) and state_search.lower() in state.lower()):
                              
                                if city_search_log == 'False' or (city_search_log == 'True' and isinstance(city, str) and city_search.lower() in city.lower()):
                                   
                                    if cpc_search_log == 'False' or (cpc_search_log == 'True' and isinstance(cpc, str) and cpc_search.lower() in cpc.lower()):

###############################################################################
#if a given row is responsive, append the abstract in new array
###############################################################################                                    

                                        response_query.append(row['patent_abstract'])
                                    
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
            
###############################################################################
#depending on the size of the search, the response_query may vary in size
#from in the single digits to the thousands or tends of thousands
###############################################################################


responsive_abstracts_df = pd.DataFrame(response_query, columns=['patent_abstract'])

stop_words = set(stopwords.words('english'))

#add to the stop words dictionary some patent-specific words that are 
#common to the entire dataset and do not add value

stop_words_patent = {'first', 'second', 'include', 'device', 'one', 'system', 
                     'method', 'data', 'least', 'base', 'may', 'provide', 
                     'configure', 'plurality', 'portion', 'method',
                     'surface', 'unit', 'information', 'user', 'image', 
                     'control', 'including', 'element', 'includes', 'configured',
                     'based', 'provided', 'receive', 'end', 'apparatus', 'member',
                     'body','wherein','use','comprise','present','set',
                     'communication','determine','using','position', 'also',
                     'structure', 'region', 'side', 'part', 'comprising',
                     'assembly','direction','value','connected','embodiment',
                     'associate','disclose','output','input','component',
                     'invention', 'comprises', 'consisting', 'associate',
                     'couple', 'within', 'disclosed', 'relate','far','formed',
                     'two','operation','receiving','module', 'coupled',
                     'associated','dispose','object', 'area', 'section',
                     'process', 'disposed', 'provides', 'resulting', 'capable',
                     'example', 'response', 'via', 'response', 'along', 
                     'determining', 'operating', 'relative','define',
                     'operating','location', 'acceptable', 'thereof', 
                     'composition', 'relates','attached', 'specifically',
                     'described','and/or','herein','containing'}

stop_words.update(stop_words_patent)

punctuation = "!@#$%^&*()_+-={[}]:;<,>.?/"

def create_asymmetric_word_df(df):
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

    # Tokenize words, ie split words in abstract into a list of space separated elements
    df['tokenized_abstract'] = df['patent_abstract'].apply(word_tokenize)
    patent_tokenized_dict = {}

    # Iterate the dataframe -> iterate words in df.tokenized_abstract -> check for uniqueness -> add to dict ||
    # increment existing key value pair for unique word.
    print("iterating rows")
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
    return patent_tokenized_dict

# Create dictionary where key = token and value = number of times it occurs
tokenized_dict = create_asymmetric_word_df(responsive_abstracts_df)

# Sort tokens into dict of num_tokens number of tokens that occur the most frequently
print("sorting")
num_tokens = 25
sorted_tokens = dict(sorted(tokenized_dict.items(), key=itemgetter(1), reverse=True)[:num_tokens])
print(sorted_tokens)

###############################################################################
#create word cloud
###############################################################################

word_cloud_mat = []

for k in sorted_tokens.keys():
    k_space = k + ' '
    word_cloud_mat = word_cloud_mat + ([k_space])*sorted_tokens[k]

word_cloud_mat = np.array(word_cloud_mat)
np.random.shuffle(word_cloud_mat)
word_cloud_str=''.join(word_cloud_mat)

wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stop_words_patent,
                min_font_size = 10).generate(word_cloud_str)

plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()