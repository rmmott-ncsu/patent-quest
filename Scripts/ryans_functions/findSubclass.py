#findSubclass.py

def rankSubclass(sorted_tokens,response_df,word_cloud_str,top):
###############################################################################
#find most likely subclass based on similar keywords
###############################################################################
    import numpy as np
    import pandas as pd
  
    
    filename = 'CPC_Common_Words.csv'
    cpc_dataframe = pd.read_csv(filename)
    new_header = cpc_dataframe.iloc[0] #grab the first row for the header
    cpc_dataframe = cpc_dataframe[1:] #take the data less the header row
    cpc_dataframe.columns = new_header #set the header row as the df header

    
    cpc_checker = []
    
    word_cloud_split = word_cloud_str.split(" ")
    m = 0

    
    score_mat = np.ones(len(cpc_dataframe))

    while m < len(cpc_dataframe):
        n = 0
        score = 0
        subclass = cpc_dataframe.iloc[m]['CPC Class']
        score_words = cpc_dataframe.iloc[m]['CPC Common Words'].split(" ")
        score_freq = cpc_dataframe.iloc[m]['CPC Word Frequency'].split(" ")
        # print(subclass)
        
        for word in word_cloud_split:     
            # print(word)
            while n < 100:
                if n < len(score_words) and word in score_words[n]:
                    score = score + int(score_freq[n])
                    n = n + 1
                else:
                    # print(word + ' ' + str(score_words[n]))
                    n = n + 1
        # print(score)
        score_mat[m] = score
        m = m + 1
    
    cpc_dataframe['Score']=score_mat
    # cpc_dataframe['Confidence'] = 100*(score_mat/sum(score_mat))
    
    all_cpc_predictions = cpc_dataframe.sort_values(by=['Score'], ascending=False)    
    top_cpc_predictions = all_cpc_predictions.drop(columns=['CPC Common Words','CPC Word Frequency'])
    
    top_cpc_predictions = top_cpc_predictions.iloc[:top]
    
    return top_cpc_predictions