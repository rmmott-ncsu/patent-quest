import pandas as pd
import csv
import math
from find_most_common_words import get_word_count_for_df
import operator

dtype = {
        "patent_id": "string",
        "patent_title": "string",
        "patent_date": "string",
        "patent_abstract": "string",
        "application_id": "string",
        "application_filing_date": "string",
        "applicant_name": "string",
        "applicant_organization": "string",
        "assignee_name": "string",
        "assignee_org_name": "string",
        "cpc_class_id": "string",
        "cpc_subclass_id": "string",
        "cpc_group_id": "string",
        "filing_date": "string",
        "inventor_name": "string",
        "inventor_city": "string",
        "inventor_state": "string",
        "inventor_count": "string"
    }

# Make string for pandas.dataframe built in query method for subclass_id and/or assignee_org_name
def make_query_string(subclass_id: str='', assignee_org_name: str=''):
    first = True
    query_string = ''
    if subclass_id:
        query_string += f'cpc_subclass_id.str.contains("{subclass_id}") '
        first = False

    if assignee_org_name:
        if not first:
            query_string += f'& assignee_org_name.str.contains("{assignee_org_name}") '
        else:
            query_string += f'assignee_org_name.str.contains("{assignee_org_name}") '
    return query_string

# Query csv by subclass id or assignee org name
def query(subclass_id: str='', assignee_org_name: str=''):
    filename = './patents_csv/patents_' + str(2020) + '.csv'
    query_df = pd.DataFrame()
    i = 0
    query_string = make_query_string(subclass_id=subclass_id, assignee_org_name=assignee_org_name)
    print(query_string)
    df = pd.read_csv(filename, dtype=dtype, chunksize=10000)
    for chunk in df:
        try:
            filtered_patents = chunk.query(query_string)
        except KeyError:
            continue
        if len(query_df) == 0 and len(filtered_patents) > 0:
            query_df = filtered_patents
        elif len(filtered_patents) > 0:
            query_df = pd.concat([query_df, filtered_patents], axis=0)
    # print(query_df.columns)
    try:
        query_df = query_df.drop(['Unnamed: 0'], axis=1)
    except:
        pass
    return query_df

# Open CSV for common word counts & document occurence
def get_super_word_count(path: str) -> dict:
    super_dict = dict()
    with open(path, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            super_dict[row['token']] = [row['count'], row['doc_count']]
    return super_dict

# Term frequency
def tf(num_times_in_doc: int, num_terms_in_doc: int)->float:
    #print(num_times_in_doc, num_terms_in_doc)
    return num_times_in_doc/num_terms_in_doc

# inverse document frequency
def idf(num_docs_in_corpus: int, num_docs_w_term: int)->float:
    #print(num_docs_in_corpus, num_docs_w_term)
    return math.log2(num_docs_in_corpus/num_docs_w_term)

# term frequency * inverse document frequency
def tf_idf_calc(num_times_in_doc: int, num_terms_in_doc: int, num_docs_in_corpus: int, num_docs_w_term: int)-> float:
    return tf(num_times_in_doc, num_terms_in_doc) * idf(num_docs_in_corpus, num_docs_w_term)

def calculate_tf_idf_by_cpc(num_docs_in_corpus: int=164523):
    CPC_CODES = {'F22G', 'D01C', 'G06M', 'A61Q', 'H01T', 'C12P', 'F15C', 'B02B', 'Y02C', 'F41H', 'H02J', 'C12N', 'A47D',
                 'B27G', 'B27J', 'A24C', 'A61P', 'B44D', 'A42B', 'A45D', 'B08B', 'B65B', 'E01F', 'F27B', 'H01S', 'F41G',
                 'B66D', 'C07F', 'F41F', 'A23K', 'D01G', 'F23K', 'D01F', 'B25G', 'B62B', 'B05D', 'G07C', 'C07H',
                 'C10M', 'H03B', 'G05D', 'A01H', 'F24V', 'F02P', 'C04B', 'A01N', 'G05F', 'F03C', 'F01B', 'A23J', 'F01N',
                 'C09C', 'C10N', 'C01B', 'F25J', 'A47C', 'F16L', 'B41B', 'B01J', 'B65F', 'A63B', 'H01F', 'H01H', 'G06V',
                 'B32B', 'Y10T', 'A01K', 'B26F', 'B67B', 'E03F', 'D04C', 'A23F', 'B60S', 'F22B', 'C12Q', 'A61J', 'C10J',
                 'F16M', 'B41J', 'B24D', 'G03B', 'B23B', 'G06T', 'B68G', 'H01C', 'H01B', 'C01G', 'H01R', 'H03F', 'B29D',
                 'B64U', 'D05B', 'B21F', 'G09G', 'F23Q', 'F16F', 'F16D', 'F24S', 'A43D', 'G01W', 'A45C', 'B27M', 'A01F',
                 'C21D', 'B27H', 'B26D', 'C10C', 'G01Q', 'A23V', 'B02C', 'E01H', 'D01B', 'B41K', 'C03C', 'F24T', 'B29K',
                 'B64C', 'G11C', 'E04B', 'F03H', 'A43B', 'B67D', 'A01J', 'G10K', 'C07K', 'D06B', 'G07F', 'B62M', 'G10C',
                 'H10N', 'F16P', 'B82Y', 'F21L', 'D10B', 'C25B', 'B60M', 'G03C', 'C07G', 'F27D', 'E21B', 'B68C', 'G16C',
                 'B62L', 'G01N', 'B42P', 'C09G', 'B22F', 'F24F', 'B65H', 'F04B', 'G21H', 'G03F', 'D06C', 'C08G', 'C25F',
                 'F17C', 'B23G', 'B01F', 'B42F', 'A46B', 'H02P', 'F28D', 'B60Y', 'G07D', 'B21L', 'G07G', 'G09B', 'H02B',
                 'A22C', 'Y02T', 'F02M', 'B07C', 'B21G', 'C01P', 'A62C', 'B66F', 'D21H', 'A21C', 'G08G', 'B28B', 'F41A',
                 'B23Q', 'B27K', 'E04G', 'A47G', 'C08B', 'D03J', 'Y10S', 'D06P', 'H04H', 'Y02B', 'E99Z', 'B33Y', 'G04R',
                 'C23G', 'B29L', 'B21J', 'A01G', 'G02B', 'D06N', 'D06L', 'E05G', 'A23G', 'G02F', 'E04C', 'G09D', 'F42C',
                 'B27B', 'B63J', 'F05B', 'D04D', 'G06N', 'B01L', 'Y04S', 'F16H', 'H04M', 'B44B', 'B44F', 'B60F', 'B04B',
                 'F01K', 'B65C', 'C13B', 'B43L', 'C12L', 'C10H', 'C08H', 'B21D', 'G10D', 'C40B', 'F22D', 'E05F', 'A61C',
                 'D03D', 'H01Q', 'H10K', 'G10B', 'A41G', 'B05C', 'F23G', 'B60D', 'G01T', 'B27F', 'B60P', 'E02C', 'B25F',
                 'B41M', 'B68B', 'D06G', 'C01D', 'D21G', 'B64G', 'A62D', 'G05G', 'B25C', 'E04D', 'E02B', 'C05G', 'B60H',
                 'A47H', 'E02D', 'C03B', 'B21B', 'C10B', 'G04F', 'B61F', 'G04B', 'A41D', 'F41B', 'E21C', 'G10G', 'D02J',
                 'B31B', 'F05D', 'B31C', 'F16C', 'G09F', 'B41P', 'B60K', 'C02F', 'H02K', 'A61F', 'G10F', 'H04L', 'G01P',
                 'B27C', 'F16B', 'A47J', 'C06C', 'D21J', 'F21Y', 'C25C', 'A61G', 'G01M', 'A47K', 'C08L', 'B61L', 'C09F',
                 'C14C', 'H04S', 'B64D', 'G03G', 'D04H', 'F23B', 'F04D', 'C23F', 'Y02A', 'G01H', 'F03B', 'G01L', 'A47L',
                 'C14B', 'C09D', 'A43C', 'C08F', 'H02H', 'A46D', 'F17D', 'C12M', 'C07J', 'G16Y', 'F23L', 'C11C', 'D02G',
                 'A61H', 'A63F', 'F05C', 'H02G', 'B27D', 'B60L', 'B61B', 'B81C', 'H01P', 'A61N', 'G01D', 'A61L', 'E03C',
                 'A61K', 'A01P', 'B09C', 'G16Z', 'A61D', 'E03D', 'A24F', 'A47F', 'F24C', 'E02F', 'G09C', 'F23C', 'C06D',
                 'E04H', 'G12B', 'G01R', 'C08K', 'C01F', 'F23N', 'B22C', 'D05D', 'C06F', 'A45B', 'H04W', 'G02C', 'G03H',
                 'C11B', 'B25H', 'E01C', 'G01V', 'H03L', 'G21C', 'H01M', 'G21F', 'F16S', 'A23C', 'D06M', 'E21F', 'H03J',
                 'C12J', 'B61K', 'B41L', 'C05B', 'B23P', 'H04Q', 'C05C', 'B23D', 'B63H', 'A61B', 'B65G', 'D07B', 'A41C',
                 'A01D', 'A45F', 'E05B', 'C12F', 'C12H', 'C10F', 'C22B', 'B82B', 'C09H', 'Y02D', 'A47B', 'C12R', 'H01J',
                 'B41N', 'D01D', 'H10B', 'B66B', 'A61M', 'G06D', 'C10L', 'G16B', 'F41J', 'B22D', 'F27M', 'A21D', 'B62J',
                 'B07B', 'C11D', 'B03D', 'C10K', 'G06C', 'C21C', 'C30B', 'G21G', 'G06G', 'B41G', 'B60W', 'F01D', 'D21F',
                 'B42D', 'B25J', 'F41C', 'D06Q', 'E04F', 'A01M', 'F16N', 'F01M', 'G01B', 'C05D', 'D03C', 'B62H', 'F26B',
                 'A23P', 'D21B', 'F15D', 'B81B', 'H04T', 'B29B', 'F02D', 'A01L', 'H03G', 'E05C', 'B62C', 'B31F', 'F02G',
                 'F01P', 'G01C', 'G06J', 'E05Y', 'C07C', 'G21J', 'F24B', 'A22B', 'Y02E', 'C08J', 'B60N', 'H03D', 'B41C',
                 'B01B', 'B01D', 'E01B', 'H03M', 'F21H', 'H02S', 'F02K', 'B04C', 'G04G', 'C08C', 'G10H', 'F28C', 'A63K',
                 'G01F', 'F25B', 'H05G', 'F25C', 'B03B', 'A44C', 'B23H', 'G01J', 'B61H', 'B43K', 'F17B', 'H04K', 'B26B',
                 'G03D', 'G11B', 'G01K', 'C09K', 'A63G', 'A24D', 'H02M', 'B60B', 'B42B', 'B28C', 'E03B', 'C22F', 'A63J',
                 'A42C', 'B06B', 'A24B', 'B25D', 'D06H', 'G06E', 'F16K', 'F01C', 'G21K', 'C05F', 'A44D', 'G16H', 'F16G',
                 'B24C', 'B61D', 'H03K', 'F02C', 'A41B', 'B60R', 'B41F', 'D06F', 'B05B', 'A01C', 'B61G', 'B41D', 'A23L',
                 'C09B', 'C07B', 'C12G', 'B66C', 'D04B', 'B03C', 'H05C', 'H01L', 'F23D', 'D05C', 'F02B', 'H01K', 'C12C',
                 'B61J', 'F16J', 'H05K', 'C09J', 'B29C', 'H02N', 'A21B', 'C06B', 'G01G', 'E06C', 'A23N', 'G08B', 'B27L',
                 'G04D', 'C23D', 'G08C', 'A63C', 'B60T', 'D21D', 'B24B', 'F23J', 'C22C', 'B67C', 'C13K', 'B09B', 'A23Y',
                 'B60V', 'B63B', 'F21V', 'A63D', 'F23M', 'C21B', 'H04J', 'B30B', 'B60J', 'B21C', 'H03C', 'G05B', 'F28F',
                 'F42B', 'F23H', 'B25B', 'B61C', 'F04C', 'H04R', 'G01S', 'A62B', 'G07B', 'H04B', 'D04G', 'F24H', 'B65D',
                 'C12Y', 'H99Z', 'B63G', 'B28D', 'G10L', 'E05D', 'A44B', 'F16T', 'F24D', 'H05F', 'A01B', 'D21C', 'Y02W',
                 'H05B', 'H05H', 'G21D', 'H01G', 'B64F', 'B63C', 'C25D', 'A41H', 'F21W', 'G21B', 'B23F', 'Y02P', 'F15B',
                 'B60C', 'G04C', 'B68F', 'A63H', 'B60Q', 'F03D', 'F42D', 'G06Q', 'C23C', 'F23R', 'F04F', 'B23C', 'F28G',
                 'D02H', 'E06B', 'B44C', 'F01L', 'F28B', 'B27N', 'G06F', 'B42C', 'B21H', 'F21S', 'A23D', 'E21D', 'C07D',
                 'B23K', 'D01H', 'F02F', 'F25D', 'D06J', 'B62D', 'G06K', 'B62K', 'A41F', 'B31D', 'B60G', 'A23B', 'F02N',
                 'B43M', 'C10G', 'B21K', 'B64B', 'E01D', 'F03G', 'C01C', 'F21K', 'H03H', 'H04N'}
    # CPC_CODES = {'F22G', 'D01C', 'G06M'}
    term = 0
    code_dict = {}
    # Load csv to dict
    with open('word_count_2020.csv','r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        super_dict = {rows[0]: [rows[1], rows[2]] for rows in reader}

    # iterate through cpc codes
    for code in CPC_CODES:
        word_dict = dict()
        term += 1
        query_df = query(code, '')
        tokenized_dict, doc_count_dict = get_word_count_for_df(query_df)

        for word in tokenized_dict:
            try:
                num_docs_with_term = int(super_dict[word][1])
            except KeyError:
                num_docs_with_term = 1
            num_terms_in_doc = int(len(tokenized_dict))
            num_times_in_doc = int(tokenized_dict[word])

            calc = tf_idf_calc(num_times_in_doc, num_terms_in_doc, num_docs_in_corpus, num_docs_with_term)
            # print(word, num_times_in_doc, num_terms_in_doc, num_docs_in_corpus, num_docs_with_term)
            word_dict[word] = calc
        print(code)
        sorted_tokens = dict(sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)[:100])
        print(sorted_tokens)
        code_dict[code] = sorted_tokens
        # print()
        # print(code_dict)

    return code_dict

        # if term > 10:
        #     break

def get_word_set(dict:dict) -> set:
    word_set = set()
    for code in dict:
        for key in dict[code].keys():
            word_set.add(key)

    return word_set

def build_tfidf_dict(code_dict, word_list: set):
    tf_idf_dict_list = list()
    for code in code_dict:
        tf_idf_dict = dict()
        tf_idf_dict['cpc'] = code

        for word in word_list:
            try:
                tf_idf_dict[word] = code_dict[code][word]
            except KeyError:
                tf_idf_dict[word] = 0

        tf_idf_dict_list.append(tf_idf_dict)

    return tf_idf_dict_list

def build_tfidf_csv(tfidf_dict_list: list):
    column = ['cpc']
    with open('tfidf_2020.csv', 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, tfidf_dict_list[0].keys())
        writer.writeheader()
        writer.writerows(tfidf_dict_list)


def main():
    code_dict = calculate_tf_idf_by_cpc()

    high_tfidf_word_set = get_word_set(code_dict)
    print(len(high_tfidf_word_set))
    tfidf_dict_list = build_tfidf_dict(code_dict, high_tfidf_word_set)
    build_tfidf_csv(tfidf_dict_list)


main()
