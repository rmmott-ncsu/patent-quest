#metaCode

from queryPatents import searchPatentCSV
from makeStopWords import makePatentStopwords
from makeSortedTokens import create_asymmetric_word_df
from makeWordCloud import visualizeWordCloud
from findSimilarPatents import rankSimilarPatents
from findSubclass import rankSubclass
from findNBSubclass import rankNBSubclass
from checkPredictionAccuracy import isAccurate

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
begin_year = 2018
end_day = 31
end_month = 12
end_year = 2018

patent_number_search = '10032154'
assignee_search = ''
inventor_search = ''
country_search = ''
state_search = ''
city_search = ''
cpc_search = ''

top = 10

num_tokens=100

make_wordcloud_jpg = 'False'
wordcloud_filename = 'nofile'

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
word_cloud_str = visualizeWordCloud(sorted_tokens, stop_words, make_wordcloud_jpg, wordcloud_filename)

print('finding similar patents')
top_similar_patents = rankSimilarPatents(sorted_tokens,response_df,date_search,assignee_search,years_mat,top)

print('top ' + str(top) + ' most similar patents found:')
print(top_similar_patents)

print('predicting subclass')
top_predicted_subclasses = rankSubclass(sorted_tokens,response_df,word_cloud_str,top)

print('top ' + str(top) + ' most likely subclasses:')
print(top_predicted_subclasses)

print('checking accuracy of prediction')
top10_accurate, top5_accurate, accurate, actual_subclass = isAccurate(top_predicted_subclasses,response_df)

if accurate == True:
    print('Confirmed -- the prediction was correct.')
    print('The class was: ' + str(actual_subclass))

else:
    print('Incorrect -- the prediction was incorrect.')    
    print('The actual class was: ' + str(actual_subclass))
    
print('predicting subclass with Naive Bayes')
print('top ' + str(top) + ' most likely subclasses:')
top_predicted_NBsubclasses = rankNBSubclass(sorted_tokens,response_df,word_cloud_str,top)    

print('checking accuracy of prediction')
top10_accurate, top5_accurate, accurate, actual_subclass = isAccurate(top_predicted_NBsubclasses,response_df)

if accurate == True:
    print('Confirmed -- the prediction was correct.')
    print('The class was: ' + str(actual_subclass))

else:
    print('Incorrect -- the prediction was incorrect.')    
    print('The actual class was: ' + str(actual_subclass))
    
