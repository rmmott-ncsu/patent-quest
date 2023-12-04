import pandas as pd
from Dtype import dtype

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
    # filename = './patents_csv/patents_' + str(2020) + '.csv'
    filename = 'single_cpc.csv'
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