#queryPatents.py

#This script sesarches .csvs, organized by year, which 
#tabulates all patents published in that time 
#and returns the patent IDs, CPC subclass, and abstracts
#that respond to a certain query

#The query is input into the code at the beginning and can be
#based on patent number, assignee, inventor, country, state, city, or cpc
#subclass


import numpy as np
import pandas as pd

def searchPatentCSV(begin_day, begin_month, begin_year, end_day, end_month, 
                    end_year, patent_number_search, assignee_search, 
                    inventor_search, country_search, state_search, 
                    city_search, cpc_search):
         
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
    if patent_number_search == '':
       patent_number_search_log = 'False'
    else:
       patent_number_search_log = 'True'         
       
    begin_date = str(begin_year) + '-' + str(begin_month) + '-' + str(begin_day) 
    end_date = str(end_year) + '-' + str(end_month) + '-' + str(end_day) 
    
    days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    days_with_zero = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    months_with_zero = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
    
    num_days = len(days)
    num_months = len(months)
    num_years = len(years)
    
    dates = []
    dates_with_zero = []
    z = 0

    while z < 2:
        
        if z == 1:
            months = months_with_zero
            days = days_with_zero
        else:
            pass
        
        for y in years:
            current_year = y
            for m in months:
                current_month = m
                for d in days:
                    current_day = d
                    
                    current_date = str(current_year) + '-' + str(current_month) + '-' + str(current_day)
                    if z == 1:
                        dates_with_zero.append(current_date)    
                    else:
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
                end_index = end_index+2
            else:
                break
        z = z+1
    
    date_search = dates[begin_index:end_index]
    date_search_with_zero = dates_with_zero[begin_index:end_index]
    date_search.extend(date_search_with_zero)
    
    ###########################################################################
    #separate the numbers of years searched for the purpose of reading .csv files
    ###########################################################################
    
    year_range = end_year - begin_year
    years_mat = np.linspace(begin_year, end_year, year_range+1, dtype=int)
    response_query = []
    cpc_response_query = []
    id_response_query = []
    
    for y in years_mat:
        
    ###########################################################################
    #for each .csv, read in chunks of 1,000 rows at a time, for memory management
    ###########################################################################
        
    
        filename = 'patents_' + str(y) + '.csv'
        csv_iterator = pd.read_csv(filename, iterator=True, chunksize=1000)
    
        for chunk in csv_iterator:
            for index, row in chunk.iterrows():
    
    ###########################################################################
    #if a given row is responsive to the date range, check fields for hits
    ###########################################################################
        
                
                if row['patent_date'] in date_search:
                    
                    assignee = row['assignee_org_name']
                    inventor = row['inventor_name']
                    country = row['inventor_country']
                    state = row['inventor_state']
                    city = row['inventor_city']
                    cpc = row['cpc_subclass_id']
                    patent_id = row['patent_id']
                    
                    if assignee_search_log == 'False' or (assignee_search_log == 'True' and isinstance(assignee, str) and assignee_search.lower() in assignee.lower()):                    
                       
                        if inventor_search_log == 'False' or (inventor_search_log == 'True' and isinstance(inventor, str) and inventor_search.lower() in inventor.lower()):
                           
                            if country_search_log == 'False' or (country_search_log == 'True' and isinstance(country, str) and country_search.lower() in country.lower()):
                              
                                if state_search_log == 'False' or (state_search_log == 'True' and isinstance(state, str) and state_search.lower() in state.lower()):
                                  
                                    if city_search_log == 'False' or (city_search_log == 'True' and isinstance(city, str) and city_search.lower() in city.lower()):
                                       
                                        if cpc_search_log == 'False' or (cpc_search_log == 'True' and isinstance(cpc, str) and cpc_search.lower() in cpc.lower()):
    
                                            if patent_number_search_log == 'False' or (patent_number_search_log == 'True' and isinstance(patent_id, int) and patent_number_search == str(patent_id)):
    
    ###########################################################################
    #if a given row is responsive, append the abstract in new array
    ############################################################################                                  
                                                
                                                response_query.append(row['patent_abstract'])
                                                cpc_response_query.append(row['cpc_subclass_id'])
                                                id_response_query.append(row['patent_id'])     
    
    ###########################################################################
    #depending on the size of the search, the response_query may vary in size
    #from in the single digits to the thousands or tends of thousands
    ###########################################################################
  
    responsive_abstracts_df = pd.DataFrame(response_query, columns=['patent_abstract'])
    responsive_cpc_df = pd.DataFrame(cpc_response_query, columns=['cpc_subclass_id'])
    responsive_id_df = pd.DataFrame(id_response_query, columns=['patent_id'])
    
    result = responsive_id_df
    result['cpc_subclasss_id'] = cpc_response_query
    result['patent_abstract'] = response_query
    
    return result
        
