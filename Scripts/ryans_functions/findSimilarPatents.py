#findSimilarPatents.py

def rankSimilarPatents(sorted_tokens,response_df,date_search,assignee_search, years_mat,top):
###############################################################################
#find ten most similar patents based on common keywords
###############################################################################
    import numpy as np
    import pandas as pd
    
    cpc_response_query = response_df['cpc_subclass_id']
    response_query = response_df['patent_abstract']
    #In this next phase, we will take the results of the word cloud and compare it
    #other patents in the database, to find a list of top ten most similar patents
    #that are not owned by the same company
    
    #First, determine how often each word appears a single time in a patent
    
    # for p in sorted_tokens.keys():
    #     sorted_tokens[p]=0
    #     for q in response_query:
    #         if p in q:
    #             sorted_tokens[p] = sorted_tokens[p]+1
    
    # #use this number to calculate the probability that the word will appear
    # #in a patent known to be responsive to the query
    
    # for p in sorted_tokens.keys():
    #     sorted_tokens[p] = sorted_tokens[p]/len(response_query)
    
    similarity_query = [0, 0]
    prob = 0
    test = 0

    
    #determine all cpc classes identified in the response query
    #in order for a patent to be considered "similar" it must fall within 
    #one of the same cpc subclasses identified in the response query
    
    #to find all the subclasses, check the cpc_response_query matrix, which
    #lists each of the cpc subclasses for each of the responsive patents
    
    cpc_checker = []
    
    for x in cpc_response_query:
        if isinstance(x,str):
            y = x.split("_")
            for z in y:
                if z in cpc_checker:
                    pass
                else:
                    cpc_checker.append(z)
        else:
            continue
        
    #then, split it using the split function and throw all the subclasses into
    #a new database
    
    
    #read all the other patents in the same time period and rank them by 
    #similarity
    for y in years_mat:    
        filename = 'patents_' + str(y) + '.csv'
        csv_iterator = pd.read_csv(filename, iterator=True, chunksize=1000)
        for chunk in csv_iterator:
            for index, row in chunk.iterrows():
    
                if row['patent_date'] in date_search:
                    patent_ID = row['patent_id']
                    patent_abstract = row['patent_abstract']
                    assignee = row['assignee_org_name']
                    patent_subclass = row['cpc_subclass_id']
                    score = 0
    #if the patent was already responsive to the last query (i.e. it was by
    #the same company) then skip it                
                    if isinstance(assignee, str) and assignee_search.lower() in assignee.lower():
                        pass
                    else:
                        cpc_test = 0
                        for z in cpc_checker:
                            if isinstance(patent_subclass, str) and z in patent_subclass:
                                cpc_test = cpc_test+1
                            else:
                                pass
                        if cpc_test > 0:
                            for p in sorted_tokens.keys():
                                if p in patent_abstract:
                                    score = score + sorted_tokens[p]
                                else:
                                    pass
                            arr = np.array([patent_ID, score], dtype=int)
                            similarity_query=np.vstack((similarity_query,arr))   
                        
                        else:
                            
                            pass
                        
                                                      
                    
    #if the patent was not responsive to the first query (i.e. it is by a different
    #or an unknown company), calculate a score by checking for the presence of each
    #of the top 100 words, and then, sum them according to their weight
    #(weight determined by the probaility that the score was found in the patents
    #that were retrieved for the original company)
    
         
    #rank by order
    similarity_query_inv = -1*similarity_query        
    similarity_query_inv_ranked = similarity_query_inv[similarity_query_inv[:, 1].argsort()]   
    similarity_query_ranked = -1*similarity_query_inv_ranked        
    similarity_query_top = similarity_query_ranked[0:top-1,:]
    df = pd.DataFrame(similarity_query_top, columns =['Patent Number', 'Score'])
     
    return df
