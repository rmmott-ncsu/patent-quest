#metaCode

#metaCode.py provides an example on how to use each function (except for checkSuperAccuracy.py).  
#it is best to start there.  choose the search criteria, whether you want a wordcloud, 
#and what filename the wordcloud should have.

#queryPatents.py will search a given set of patents based on a query.  
#you must provide a date range.  note that for longer date ranges, the query can be slow.

#makeStopWords.py makes a corpus of stop words using provided ones as well as patent-specific 
#ones found during the course of this project

#makeSortedTokens.py makes a tokenized list of the most common words of the 
#abstract or abstracts found in the search query

#makeWordCloud.py makes a Word Cloud visualization based on the output from makeSortedTokens.py

#findSimilarPatents.py ranks the ten most similar patents in the 
#same date range that did not come from the same assignee.

#findSubclass.py makes a prediction of technological class based on a 
#weighted word frequency similarity comparison

#findNBSubclass makes a prediction of technological class based on a Naive Bayes model

#checkPredictionAccuracy.py evaluates whether a given subclass (word frequency or NB) 

#checkSuperAccuracy.py is the only code independent of metaCode.  
#It performs an iterative accuracy test of the classifier algorithm 
#and produces a chart showing accuracy convergence as well as a .txt log of every prediction made


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
    
