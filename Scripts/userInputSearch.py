#search script

import numpy as np
import pandas as pd
import math

##############################################################################
#user inputs
#this will ultimately structured as a function with 12 inputs
##############################################################################

begin_day = 1
begin_month = 1
begin_year = 2013
end_day = 31
end_month = 4
end_year = 2014
assignee_search = ''
inventor_search = ''
country_search = ''
state_search = ''
city_search = ''
cpc_search = 'C12N'

##############################################################################
#assign logic parameters for search for use in if/then statements later
##############################################################################

if assignee_search == '':
   assignee_search_log = 'False'
else:
   assignee_search_log = 'True'
    
if inventor_search == '':
   inventor_search_log = 'False'
else:
   inventor_search_log = 'True'

if country_search == '':
   country_search_log = 'False'
else:
   country_search_log = 'True'

if state_search == '':
   state_search_log = 'False'
else:
   state_search_log = 'True'

if city_search == '':
   city_search_log = 'False'
else:
   city_search_log = 'True'

if cpc_search == '':
   cpc_search_log = 'False'
else:
   cpc_search_log = 'True'

###############################################################################
#create array of dates based on the specified date range by finding ALL dates
#that were between 2013 and 2023, and then taking only the ones specified
###############################################################################

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

###############################################################################
#separate the numbers of years searched for the purpose of reading .csv files
###############################################################################

year_range = end_year - begin_year
years_mat = np.linspace(begin_year, end_year, year_range+1, dtype=int)
response_query = []

for y in years_mat:
    
###############################################################################
#for each .csv, read in chunks of 10,000 rows at a time, for memory management
###############################################################################
    
    # Returns a TextFileReader, which is iterable with chunks of 10000 rows.
    filename = 'patents_' + str(y) + '.csv'
    csv_iterator = pd.read_csv(filename, iterator=True, chunksize=10000)
    
    # Iterate through the dataframe chunks
    for chunk in csv_iterator:
        for index, row in chunk.iterrows():

###############################################################################
#if a given row is responsive to the date range, check fields for hits
#(some of the compliations below stem from the fact that when the data value
#is empty, Python runs into problems, so you have to do all these checks
#before you make an improper comparison (for example, whether a string is in
#a NaN)
###############################################################################
    
            
            if row['patent_date'] in date_search:
                
                assignee = row['assignee_org_name']
                inventor = row['inventor_name']
                country = row['inventor_country']
                state = row['inventor_state']
                city = row['inventor_city']
                cpc = row['cpc_group_id']    
                
                if assignee_search_log == 'False' or (assignee_search_log == 'True' and isinstance(assignee, str) and assignee_search in assignee):                    
                   
                    if inventor_search_log == 'False' or (inventor_search_log == 'True' and isinstance(inventor, str) and inventor_search in inventor):
                       
                        if country_search_log == 'False' or (country_search_log == 'True' and isinstance(country, str) and country_search in country):
                          
                            if state_search_log == 'False' or (state_search_log == 'True' and isinstance(state, str) and state_search in state):
                              
                                if city_search_log == 'False' or (city_search_log == 'True' and isinstance(city, str) and city_search in city):
                                   
                                    if cpc_search_log == 'False' or (cpc_search_log == 'True' and isinstance(cpc, str) and cpc_search in cpc):

###############################################################################
#if a given row is responsive, append the abstract in new array
###############################################################################                                    

                                        response_query.append(row['patent_abstract'])
                                    
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
            
###############################################################################
#depending on the size of the search, the response_query may vary in size
#from in the single digits to the thousands or tends of thousands
###############################################################################


