#prediction_test
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt


from queryPatents import searchPatentCSV
from makeStopWords import makePatentStopwords
from makeSortedTokens import create_asymmetric_word_df
from makeWordCloud import visualizeWordCloud
from findSimilarPatents import rankSimilarPatents
from findSubclass import rankSubclass
from checkPredictionAccuracy import isAccurate

top10_accurate_mat = 0
top5_accurate_mat = 0
accurate_mat = 0
total_mat = 0
num_tokens = 200

filename = 'patents_2023.csv'
top = 10

test_csv = pd.read_csv(filename)

first_patent_ID = 11540434
second_patent_ID = 11665987
number_of_samples = 1000

accurate_trials = np.zeros((number_of_samples))
top5_accurate_trials = np.zeros((number_of_samples))
top10_accurate_trials = np.zeros((number_of_samples))
total_trials = np.zeros((number_of_samples))



#find 1000 random patents between 11212952 and 11540433
patent_sample = random.sample(range(first_patent_ID, second_patent_ID), number_of_samples)




f = open("output.txt", "a")

w = 0

for patent_id in patent_sample:

    print(str(w + 1) + ': ' + str(patent_id) )
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
    with open("output.txt", "a") as f:
        print('|', file=f)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', file=f)
        print('For U.S. Patent No. ' + str(patent_id) + ' . . .', file=f)  
    # print('making stop words')
    stop_words, punctuation = makePatentStopwords()
    
    # print('making sorted tokenized dictionary')
    sorted_tokens = create_asymmetric_word_df(response_df, stop_words, punctuation, num_tokens)
    
    word_cloud_mat = []
    
    for k in sorted_tokens.keys():
        k_space = k + ' '
        word_cloud_mat = word_cloud_mat + ([k_space])*sorted_tokens[k]
    
    word_cloud_str = np.array(word_cloud_mat)
    np.random.shuffle(word_cloud_str)
    word_cloud_str = ''.join(word_cloud_str)
    
    
    # print('predicting subclass')
    top_predicted_subclasses = rankSubclass(sorted_tokens,response_df,word_cloud_str,top)
    with open("output.txt", "a") as f: 
        print('Top ' + str(top) + ' most likely subclasses:', file=f)
        print(top_predicted_subclasses, file=f)
    
    # print('Checking accuracy of prediction . . .')
    top10_accurate, top5_accurate, accurate, actual_subclass = isAccurate(top_predicted_subclasses,response_df)
       
    if accurate == True:
        with open("output.txt", "a") as f: 
            print('Confirmed - the prediction was correct.', file=f)
            print('The actual class was: ' + str(actual_subclass), file=f)
        accurate_mat = accurate_mat + 1
        top5_accurate_mat = top5_accurate_mat + 1
        top10_accurate_mat = top10_accurate_mat + 1
        total_mat = total_mat + 1
    elif accurate == False and top5_accurate == True:
        with open("output.txt", "a") as f: 
            print('Almost - the correct class was in the top 5.', file=f)
            print('The actual class was: ' + str(actual_subclass), file=f)
        top5_accurate_mat = top5_accurate_mat + 1
        top10_accurate_mat = top10_accurate_mat + 1
        total_mat = total_mat + 1
    elif top5_accurate == False and top10_accurate == True:
        with open("output.txt", "a") as f: 
            print('Close - the correct class was in the top 10.', file=f)
            print('The actual class was: ' + str(actual_subclass), file=f)
        top10_accurate_mat = top5_accurate_mat + 1
        total_mat = total_mat + 1
    elif actual_subclass == [] :
        with open("output.txt", "a") as f: 
            print("Not qualified - there was no subclass.", file=f)
    else:
        with open("output.txt", "a") as f: 
            print('Incorrect -- the prediction was incorrect, and the correct class was identified in neither the top 5 nor top 10.', file=f)    
            print('The actual class was: ' + str(actual_subclass), file=f)
        total_mat = total_mat + 1
    
    accurate_trials[w] = (accurate_mat / total_mat)*100
    top5_accurate_trials[w] = (top5_accurate_mat / total_mat)*100
    top10_accurate_trials[w] = (top10_accurate_mat / total_mat)*100
    total_trials[w] = total_mat

    with open("output.txt", "a") as f: 
        print('', file=f)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', file=f)
        print('|', file=f)   
        
        
        print("Overall accuracy so far: " + str((accurate_mat / total_mat)*100))
        print("Overall top-5 accuracy so far: " + str((top5_accurate_mat / total_mat)*100))
        print("Overall top-10 accuracy so far: " + str((top10_accurate_mat / total_mat)*100))
        print('')
        
    w = w + 1
    
total_accuracy = (accurate_mat / total_mat)*100
top5_accuracy = (top5_accurate_mat / total_mat)*100
top10_accuracy = (top10_accurate_mat / total_mat)*100


with open("output.txt", "a") as f: 
    print('The overall accuracy of the model is ' + str(total_accuracy) + "%.", file=f)
    print('', file=f)
    print('The top-5 overall accuracy of the model is ' + str(top5_accuracy) + "%.", file=f)
    print('', file=f)      
    print('The top-10 overall accuracy of the model is ' + str(top10_accuracy) + "%.", file=f)
    print('', file=f) 
    
# initialize data of lists. 
data = {'Accuracy': accurate_trials, 
        'Top 5 Accuracy': top5_accurate_trials,
        'Top 10 Accuracy': top10_accurate_trials,
        'Total Trials' :total_trials}  
  
# Create DataFrame 
df = pd.DataFrame(data) 

df.to_csv('trial_accuracy_data.csv')
  

#plot individual lines with custom colors and labels
plt.plot(df['Accuracy'], '-', label = 'Top 1', color='green')
plt.plot(df['Top 5 Accuracy'], '--', label = 'Top 5', color='steelblue')
plt.plot(df['Top 10 Accuracy'], ':', label = 'Top 10', color='coral')

#add legend
plt.legend(title='Measure of Accuracy')

#add axes labels and a title
plt.ylabel('Accuracy', fontsize=12)
plt.xlabel('Number of Trials', fontsize=12)
plt.title('Accuracy Convergence of CPC Model over 1000 Trials', fontsize=12)

#display plot
plt.show()


