import csv
from nltk.corpus import stopwords
import operator
import pandas as pd

# Create dict of top 10 CPC predictions. Key=CPC, value = score
def predict(abstract: str) -> dict:
    score_dict = dict()
    stop_words = set(stopwords.words('english'))
    stop_words_patent = {'first', 'second', 'include', 'device', 'one', 'system',
                         'method', 'data', 'least', 'base', 'may', 'provide',
                         'configure', 'plurality', 'portion', 'method',
                         'surface', 'unit', 'information', 'user', 'image',
                         'control', 'including', 'element', 'includes', 'configured',
                         'based', 'provided', 'receive', 'end', 'apparatus', 'member',
                         'body', 'wherein', 'use', 'comprise', 'present', 'set',
                         'communication', 'determine', 'using', 'position', 'also',
                         'structure', 'region', 'side', 'part', 'comprising',
                         'assembly', 'direction', 'value', 'connected', 'embodiment',
                         'associate', 'disclose', 'output', 'input', 'component',
                         'invention', 'comprises', 'consisting', 'associate',
                         'couple', 'within', 'disclosed', 'relate', 'far', 'formed',
                         'two', 'operation', 'receiving', 'module', 'coupled',
                         'associated', 'dispose', 'object', 'area', 'section',
                         'process', 'disposed', 'provides', 'resulting', 'capable',
                         'example', 'response', 'via', 'response', 'along',
                         'determining', 'operating', 'relative', 'define',
                         'operating', 'location', 'acceptable', 'thereof',
                         'composition', 'relates', 'attached', 'specifically',
                         'described', 'and/or', 'herein', 'containing', 'housing',
                         'container', 'positioned', 'particular', 'received',
                         'whether', 'receives', 'corresponding', 'identifying',
                         'identified', 'determined', 'according', 'selected',
                         'determines', 'according', 'whether', 'respective',
                         'different', 'forming', 'arrange', 'amount', 'generate'
                                                                      'determination', 'third', 'different', 'inside',
                         'outside', 'opening', 'arranged', 'near', 'exemplary',
                         'type', 'interior', 'exterior', 'edge', 'size', 'various',
                         'significant', 'generate', 'generating', 'among', 'cause',
                         'presented', 'layer', 'model', 'disclosure', 'e.g.',
                         'producing', 'nearly', 'allows', 'produced', 'increase'
                                                                      'following', 'generally', 'preparing', 'another',
                         'thus', 'new'}
    stop_words.update(stop_words_patent)

    punctuation = "!@#$%^&*()_+-={[}]:;<,>.?/"
    # open tf-idf file
    with open('tfidf_2020.csv', 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        data = [row for row in reader]

    tokenized_abstract = abstract.split(' ')

    # Initialize score for all potential cpc's classes to zero
    for cpc_dict in data:
        score_dict[cpc_dict['cpc']] = 0

    # Iterate words in tokenized abstract
    for word in tokenized_abstract:
        if word not in punctuation and word not in stop_words and len(word) > 2:
            for cpc_dict in data:
                # Check against lematized versions in tf-idf scores file
                for lem_word in check_lem(word):
                    try:
                        score_dict[cpc_dict['cpc']] += float(cpc_dict[lem_word])
                        # print(cpc_dict['cpc'], lem_word, float(cpc_dict[lem_word]))
                        break
                    except KeyError:
                        pass
    sorted_scores = dict(sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)[:10])

    return sorted_scores

# Get top score from dictionary object of scores
def max_prediction(score_dict: dict) -> str:
    return max(score_dict, key=score_dict.get)


# Return tuple of possible lematized versions of word
def check_lem(word: str):
    return word, word[:-1], word[:-4], word[:-3]

# Iterate through patent file and make predictions, compare to real data, return score
def predict_batch():
    df = pd.read_csv('patents_csv/patents_2020.csv').head(3000)
    rel_df = df[["patent_id", 'cpc_subclass_id', 'patent_abstract']]
    count = 0
    pred_score = 0
    for index, row in rel_df.iterrows():
        count += 1
        prediction = predict(row['patent_abstract'])
        max_score = max_prediction(prediction)
        try:
            if max_score in row['cpc_subclass_id']:
                pred_score += 1
        except TypeError:
            print(row['patent_id'])



    print(pred_score, count)


predict_batch()

