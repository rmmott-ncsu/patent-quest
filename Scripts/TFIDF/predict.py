import csv
from nltk.corpus import stopwords
import operator
import pandas as pd

from StopWords import stop_words_patent

# Create dict of top 10 CPC predictions. Key=CPC, value = score
def predict(abstract: str, tfidf_super_data: list) -> tuple:
    data = tfidf_super_data
    score_dict = dict()
    stop_words = set(stopwords.words('english'))

    stop_words.update(stop_words_patent)

    punctuation = "!@#$%^&*()_+-={[}]:;<,>.?/"
    # open tf-idf file


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
    sorted_scores_10 = dict(sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)[:10])
    sorted_scores_5 = dict(sorted(sorted_scores_10.items(), key=operator.itemgetter(1), reverse=True)[:10])
    return sorted_scores_10, sorted_scores_5

# Get top score from dictionary object of scores
def max_prediction(score_dict: dict) -> str:
    return max(score_dict, key=score_dict.get)


# Return tuple of possible lematized versions of word
def check_lem(word: str):
    return word, word[:-1], word[:-4], word[:-3]

# Iterate through patent file and make predictions, compare to real data, return score
# If top prediction is in list of patent cpc's, score += 1, otherwise score += 0
def predict_batch(tf_idf_file: str = 'tfidf_single_cpc.csv', test_data_file: str='patents_csv/patents_2020.csv'):
    df = pd.read_csv(test_data_file).head(10000)
    rel_df = df[["patent_id", 'cpc_subclass_id', 'patent_abstract']]
    pred_dict = {}
    count_dict = {}

    with open(tf_idf_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        data = [row for row in reader]

    count = 0
    pred_score = 0
    pred_score_5 = 0
    pred_score_10 = 0
    for index, row in rel_df.iterrows():
        count += 1
        prediction_10, prediction_5 = predict(row['patent_abstract'], data)
        max_score = max_prediction(prediction_10)
        try:
            actual = row['cpc_subclass_id']
            if max_score in actual:
                try:
                    pred_dict[max_score][0] += 1
                except KeyError:
                    pred_dict[max_score] = [1, 0]
                pred_score += 1

            else:
                try:
                    pred_dict[max_score][1] += 1
                except KeyError:
                    pred_dict[max_score] = [0, 1]

            if score_prediction(list(prediction_5.keys()), actual):
                pred_score_5 += 1

            if score_prediction(list(prediction_10.keys()), actual):
                pred_score_10 += 1

        except TypeError:
            pass

    print('Top Accuracy', pred_score, count)
    print('Top 5 Accuracy', pred_score_5, count)
    print('Top 10 Accuracy', pred_score_10, count)
    print(pred_dict)
    print(count_dict)
    print()

def score_prediction(prediction_list: list, actual: str):
    for cpc in prediction_list:
        if cpc in actual:
            return True
    return False

if __name__ == '__main__':
    predict_batch('tfidf_calc_2020.csv', 'patents_csv/patents_2014.csv')
    predict_batch('tfidf_calc_2020.csv', 'patents_csv/patents_2015.csv')
    predict_batch('tfidf_calc_2020.csv', 'patents_csv/patents_2016.csv')
    predict_batch('tfidf_calc_2020.csv', 'patents_csv/patents_2017.csv')
    predict_batch('tfidf_calc_2020.csv', 'patents_csv/patents_2018.csv')
    predict_batch('tfidf_calc_2020.csv', 'patents_csv/patents_2019.csv')

