#check prediction accuracy

def isAccurate(top_predicted_subclasses,response_df):
    
    cpc_response_query = response_df['cpc_subclass_id']   
    
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
    
    accurate = False
    top5_accurate = False
    top10_accurate = False
    
    for subclass in cpc_checker:
        if subclass == top_predicted_subclasses.iloc[0]['CPC Class']:
            accurate = True
        else:
            pass
        
    for subclass in cpc_checker:
        for predicted_sub in top_predicted_subclasses.iloc[0:5]['CPC Class']:
            if subclass == predicted_sub:
                    top5_accurate = True
            else:
                pass
    
    for subclass in cpc_checker:
        for predicted_sub in top_predicted_subclasses['CPC Class']:
            if subclass == predicted_sub:
                    top10_accurate = True
            else:
                pass    
    
    return top10_accurate, top5_accurate, accurate, cpc_checker
