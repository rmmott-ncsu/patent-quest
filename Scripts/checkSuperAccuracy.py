#prediction_test
import numpy as np
import pandas as pd
import random


from queryPatents import searchPatentCSV
from makeStopWords import makePatentStopwords
from makeSortedTokens import create_asymmetric_word_df
from makeWordCloud import visualizeWordCloud
from findSimilarPatents import rankSimilarPatents
from findSubclass import rankSubclass
from checkPredictionAccuracy import isAccurate



accurate_mat = 0
total_mat = 0
num_tokens = 100

filename = 'patents_2022.csv'
top = 10

test_csv = pd.read_csv(filename)

first_patent_ID = 11212952
second_patent_ID = 11540433
#find 100 random patents between 11212952 and 11540433
patent_sample = random.sample(range(11212952, 11540433), 20)


for patent_id in patent_sample:

    response_query = []
    cpc_response_query = []
    id_response_query = []
    x = 0
    while x < len(test_csv):
        if test_csv.iloc[x]['patent_id'] == patent_id:
            response_query.append(test_csv.iloc[x]['patent_abstract'])
            cpc_response_query.append(test_csv.iloc[x]['cpc_subclass_id'])
            id_response_query.append(test_csv.iloc[x]['patent_id'])     
        x = x + 1
    responsive_abstracts_df = pd.DataFrame(response_query, columns=['patent_abstract'])
    responsive_cpc_df = pd.DataFrame(cpc_response_query, columns=['cpc_subclass_id'])
    responsive_id_df = pd.DataFrame(id_response_query, columns=['patent_id'])
    
    result = responsive_id_df
    result['cpc_subclass_id'] = cpc_response_query
    result['patent_abstract'] = response_query
    
    response_df = result
    
    print('making stop words')
    stop_words, punctuation = makePatentStopwords()
    
    print('making sorted tokenized dictionary')
    sorted_tokens = create_asymmetric_word_df(response_df, stop_words, punctuation, num_tokens)
    
    word_cloud_mat = []
    
    for k in sorted_tokens.keys():
        k_space = k + ' '
        word_cloud_mat = word_cloud_mat + ([k_space])*sorted_tokens[k]
    
    word_cloud_str = np.array(word_cloud_mat)
    np.random.shuffle(word_cloud_str)
    word_cloud_str = ''.join(word_cloud_str)
    
    
    print('predicting subclass')
    top_predicted_subclasses = rankSubclass(sorted_tokens,response_df,word_cloud_str,top)
    
    print('top ' + str(top) + ' most likely subclasses:')
    print(top_predicted_subclasses)
    
    print('checking accuracy of prediction')
    accurate, actual_subclass = isAccurate(top_predicted_subclasses,response_df)
    
    
    if accurate == True:
        print('Confirmed -- the prediction was correct.')
        print('The actual class was: ' + str(actual_subclass))
        accurate_mat = accurate_mat + 1
        total_mat = total_mat + 1
    else:
        print('Incorrect -- the prediction was incorrect.')    
        print('The actual class was: ' + str(actual_subclass))
        total_mat = total_mat + 1
    
total_accuracy = (accurate_mat / total_mat)*100
print('The overall accuracy of the model is ' + str(total_accuracy) + "%.")


