#make stopwords


def makePatentStopwords():
    
    from nltk.corpus import stopwords

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
                         'described','and/or','herein','containing', 'housing',
                         'container', 'positioned', 'particular','received',
                         'whether', 'receives', 'corresponding', 'identifying',
                         'identified','determined','according','selected',
                         'determines','according','whether','respective',
                         'different','forming','arrange','amount','generate'
                         'determination','third','different','inside',
                         'outside','opening','arranged','near','exemplary',
                         'type','interior','exterior','edge','size', 'various',
                         'significant','generate','generating','among','cause',
                         'presented','layer','model','disclosure', 'e.g.',
                         'producing', 'nearly','allows','produced','increase'
                         'following', 'generally', 'preparing', 'another',
                         'thus', 'new'}
    
    stop_words.update(stop_words_patent)
    
    punctuation = "!@#$%^&*()_+-={[}]:;<,>.?/"
    
    return(stop_words, punctuation)