#test

from queryPatents import searchPatentCSV
from makeStopWords import makePatentStopwords
from makeSortedTokens import create_asymmetric_word_df
from makeWordCloud import visualizeWordCloud
from findSimilarPatents import rankSimilarPatents
import pandas as pd
import numpy as np


# Have to download stopwords and punkt for nltk library to work correctly.
# Uncomment 4 lines below and run on it's own after pip install.

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

begin_day = 1
begin_month = 1
begin_year = 2022
end_day = 28
end_month = 2
end_year = 2022

patent_number_search = ''
assignee_search = 'Ford'
inventor_search = ''
country_search = ''
state_search = ''
city_search = ''
cpc_search = ''

num_tokens=50

top = 10

make_wordcloud_jpg = 'True'
wordcloud_filename = 'test_rmott'

print('querying data')
response_df, date_search, years_mat = searchPatentCSV(begin_day, begin_month, begin_year, end_day, end_month, 
                    end_year, patent_number_search, assignee_search, 
                    inventor_search, country_search, state_search, 
                    city_search, cpc_search)

print('making stop words')
stop_words, punctuation = makePatentStopwords()

print('making sorted tokenized dictionary')
sorted_tokens = create_asymmetric_word_df(response_df, stop_words, punctuation,num_tokens)

print('making word cloud')
wordcloud = visualizeWordCloud(sorted_tokens, stop_words, make_wordcloud_jpg, wordcloud_filename)

print('finding similar patents')
top_similar_patents = rankSimilarPatents(sorted_tokens,response_df,date_search,assignee_search,years_mat,top)

print(top_similar_patents)
