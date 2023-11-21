#date and company searcher

import numpy as np
import pandas as pd
import math

#user inputs
begin_day = 1
begin_month = 10
begin_year = 2013
end_day = 31
end_month = 4
end_year = 2017
assignee_search = 'TERYX'

#date calculation

begin_date = str(begin_year) + '-' + str(begin_month) + '-' + str(begin_day) 
end_date = str(end_year) + '-' + str(end_month) + '-' + str(end_day) 

days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

num_days = len(days)
num_months = len(months)
num_years = len(years)

dates = []

for y in years:
    current_year = y
    for m in months:
        current_month = m
        for d in days:
            current_day = d
            current_date = str(current_year) + '-' + str(current_month) + '-' + str(current_day)
            dates.append(current_date)

begin_index = 0
end_index = 0

for x in dates:    
    if begin_date != x:
        begin_index = begin_index+1
    else:
        break

for w in dates:    
    if end_date != w:
        end_index = end_index+1
    else:
        break

date_search = dates[begin_index:end_index]


year_range = end_year - begin_year
years_mat = np.linspace(begin_year, end_year, year_range+1, dtype=int)
response_query = []

for y in years_mat:
    # Returns a TextFileReader, which is iterable with chunks of 1000 rows.
    filename = 'patents_' + str(y) + '.csv'
    csv_iterator = pd.read_csv(filename, iterator=True, chunksize=1000)
    
    # Iterate through the dataframe chunks
    for chunk in csv_iterator:
        for index, row in chunk.iterrows():
            if row['patent_date'] in date_search:
                assignee_org = row['assignee_org_name']
                if isinstance(assignee_org, str):
                    if assignee_search in assignee_org:
                        response_query.append(row['patent_abstract'])
                    else:
                        pass
                else:
                    pass
            else:
                pass
