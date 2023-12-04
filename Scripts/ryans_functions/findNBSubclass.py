#predict with naive bayesian

# prepare naive bayesian matrix


# to properly create naive bayes classifier:
    
    #probability of being in a given class IF a given word is in the abstract is:
    #P(Given Class | presence of word)
    
    #which is found by computing the probability of being
    #in that particular class:
    #P(class)
    
    #multiplied by the probability of having a word in the body IF it is of a given class:
    #P(presence of word|in a given class)
    
    #when expaded to multiple words, i.e.,
    #P(Given Class | presence of several words)
    
    #the probability is found by multiplying each individual probabilities of 
    #the sevearl words
    #P(presence of word 1|in a given class)*P(presence of word 2| in a given class)
    
    #the ultimate conclusion as to what class it falls in is:
    #argmax P(Given Class|presence of words)=P(class)*P(presence of word|in a given class)*P(presence of word 2|in a given class)...
    
    
def rankNBSubclass(sorted_tokens,response_df,word_cloud_str,top):
        
        import pandas as pd
        import numpy as np
        
        filename = 'CPC_Subclass_onehot.csv'
        onehot_dataframe = pd.read_csv(filename)
        max_frequency = onehot_dataframe['CPC Frequency'].max()
        corpus = onehot_dataframe.columns.values.tolist()
        abstract_one_hot = np.zeros(len(corpus), dtype=int)
        corpus = corpus[3:]
        
        # abstract_one_hot = np.zeros(len(corpus), dtype=int)
        
        naivebayes_array = onehot_dataframe.to_numpy()
        
        indx = 3
        for corp in corpus:
            for word in sorted_tokens.keys():
                 if word == corp:                         
                     abstract_one_hot[indx] = abstract_one_hot[indx]+1
                 else:
                     pass                    
            indx = indx + 1

        corpus_id = []
        abs_iteration = 0
        while abs_iteration < len(abstract_one_hot):
            if abstract_one_hot[abs_iteration] > 0:
                corpus_id.append(abs_iteration)
            else:
                pass
            abs_iteration=abs_iteration+1    
        
        
        
        sums = np.zeros(len(naivebayes_array.T))
        
        col_index = 2
        while col_index < len(naivebayes_array.T):
            sums[col_index] = sum(naivebayes_array[:,col_index])
            col_index=col_index+1
        
        naivebayes_array = np.vstack((naivebayes_array,sums))     
        
        
        z = 0
        scores = np.zeros(len(naivebayes_array))
        
        while z < (len(naivebayes_array)-1):
            P_class = naivebayes_array[z,2]/naivebayes_array[len(naivebayes_array)-1,2]
            P_words = 1
            for abs_word in corpus_id:
                if naivebayes_array[z,abs_word] > 0:
                    P_word = naivebayes_array[z,abs_word]/naivebayes_array[z,2]
                else:
                    P_word = 1/max_frequency
                P_words = P_words*P_word
            scores[z] = P_class*P_words
            z = z + 1
            
            data = {'CPC Class': naivebayes_array[:,1], 'Score': scores} 
            ranking_df = pd.DataFrame(data) 
            ranking_df = ranking_df.sort_values(by='Score', ascending=False)
              
            ranking_df = ranking_df.iloc[:top]
    
    
        return ranking_df