# Script to convert JSON files to CSV files.
# Input path = ./patents_json/
# Output path = ./patents_csv/
# Paths should be changed depending on file structure.
# Modified version of data_clean_test.ipynb. wrapped algorithm in a couple separate methods for ~readability~
import pandas as pd
import json


# load json file as dict in memory.
def load_json(path: str) -> dict:
    with open(path) as f:
        data = json.load(f)
    return data


# Flatten json-like dict and return dict with flattened json-like objects.
def build_clean_dict(data: dict) -> dict:
    patent_df = pd.DataFrame()
    new_json = []
    new_json_item = {}
    cell_list_delimiter = '_'
    for patent in data['patents']:
        new_json_item.update({"patent_id": patent['patent_id']})
        new_json_item.update({"patent_title": patent['patent_title']})
        new_json_item.update({"patent_date": patent['patent_date']})
        new_json_item.update({"patent_abstract": patent['patent_abstract']})

        # for every application id, append as a list separated by cell_list_delimiter
        try:
            application_id = ""
            application_filing_date = ""
            for index, item in enumerate(patent['application']):
                if index == 0:
                    try:
                        application_id += item['application_id']
                    except TypeError:
                        application_id == (None)
                    try:
                        application_filing_date += item['filing_date']
                    except TypeError:
                        application_filing_date == (None)
                else:
                    try:
                        application_id += (cell_list_delimiter + item['application_id'])
                    except TypeError:
                        application_id == (None)
                    try:
                        application_filing_date += (cell_list_delimiter + item['filing_date'])
                    except TypeError:
                        application_filing_date == (None)

            new_json_item.update({"application_id": application_id})
            new_json_item.update({"application_filing_date": application_filing_date})
        except KeyError:
            new_json_item.update({"application_id": None})
            new_json_item.update({"application_filing_date": None})

        # for every applicant, append as a list separated by cell_list_delimiter
        try:
            applicant_name = ""
            applicant_organization = ""
            for index, item in enumerate(patent['applicants']):
                if index == 0:
                    try:
                        applicant_name += (item['applicant_name_first'] + ' ' + item['applicant_name_last'])
                    except TypeError:
                        applicant_name == (None)
                    try:
                        applicant_organization += item['applicant_organization']
                    except TypeError:
                        applicant_organization == (None)
                else:
                    try:
                        applicant_name += (cell_list_delimiter + (
                                    item['applicant_name_first'] + ' ' + item['applicant_name_last']))
                    except TypeError:
                        applicant_name == (None)
                    try:
                        applicant_organization += (cell_list_delimiter + item['applicant_organization'])
                    except TypeError:
                        applicant_organization == (None)

            new_json_item.update({"applicant_name": applicant_name})
            new_json_item.update({"applicant_organization": applicant_organization})
        except KeyError:
            new_json_item.update({"applicant_name": None})
            new_json_item.update({"applicant_organization": None})

        # for every assignee (if it exists), append as a list separated by cell_list_delimiter
        try:
            name_list = ""
            org_list = ""
            for index, item in enumerate(patent['assignees']):
                if index == 0:
                    try:
                        name_list += (item['assignee_individual_name_first'] + ' ' + item['assignee_individual_name_last'])
                    except TypeError:
                        name_list == (None)

                    try:
                        org_list += (item['assignee_organization'])
                    except TypeError:
                        org_list == (None)
                else:
                    try:
                        name_list += (cell_list_delimiter + (
                                    item['assignee_individual_name_first'] + ' ' + item['assignee_individual_name_last']))
                    except TypeError:
                        name_list == (None)

                    try:
                        org_list += (cell_list_delimiter + item['assignee_organization'])
                    except TypeError:
                        org_list == (None)

            new_json_item.update({"assignee_name": name_list})
            new_json_item.update({"assignee_org_name": org_list})

        except KeyError:
            new_json_item.update({"assignee_name": None})
            new_json_item.update({"assignee_org_name": None})

        # for every cpc_current (if it exists), append as a list separated by cell_list_delimiter
        try:
            cpc_class = ""
            cpc_class_id = ""
            cpc_subclass = ""
            cpc_subclass_id = ""
            cpc_group = ""
            cpc_group_id = ""
            for index, item in enumerate(patent['cpc_current']):
                if index == 0:
                    try:
                        cpc_class_id += (item['cpc_class_id'])
                    except TypeError:
                        cpc_class_id == (None)

                    try:
                        cpc_subclass_id += (item['cpc_subclass_id'])
                    except TypeError:
                        cpc_subclass_id == (None)

                    try:
                        cpc_group_id += (item['cpc_group_id'])
                    except TypeError:
                        cpc_group_id == (None)

                else:
                    try:
                        cpc_class_id += (cell_list_delimiter + item['cpc_class_id'])
                    except TypeError:
                        cpc_class_id == (None)

                    try:
                        cpc_subclass_id += (cell_list_delimiter + item['cpc_subclass_id'])
                    except TypeError:
                        cpc_subclass_id == (None)

                    try:
                        cpc_group_id += (cell_list_delimiter + item['cpc_group_id'])
                    except TypeError:
                        cpc_group_id == (None)

            new_json_item.update({"cpc_class_id": cpc_class_id})
            new_json_item.update({"cpc_subclass_id": cpc_subclass_id})
            new_json_item.update({"cpc_group_id": cpc_group_id})

        except KeyError:
            new_json_item.update({"cpc_class_id": None})
            new_json_item.update({"cpc_subclass_id": None})
            new_json_item.update({"cpc_group_id": None})

        # for every foreign_priority (if it exists), append as list separated by cell_list_delimiter
        try:
            filing_date = ""
            for index, item in enumerate(patent['foreign_priority']):
                if index == 0:
                    try:
                        filing_date += (item['filing_date'])
                    except TypeError:
                        filing_date == (None)

                else:
                    try:
                        filing_date += (cell_list_delimiter + item['filing_date'])
                    except TypeError:
                        filing_date == (None)

            new_json_item.update({"filing_date": filing_date})

        except KeyError:
            new_json_item.update({"filing_date": None})

        # for every 'inventors' (if it exists), append as a list separated by cell_list_delimiter
        try:
            inventor_name = ""
            inventor_city = ""
            inventor_state = ""
            inventor_country = ""
            for index, item in enumerate(patent['inventors']):
                if index == 0:
                    try:
                        inventor_name += (item['inventor_name_first'] + ' ' + item['inventor_name_last'])
                    except TypeError:
                        inventor_name == (None)

                    try:
                        inventor_city += (item['inventor_city'])
                    except TypeError:
                        inventor_city == (None)

                    try:
                        inventor_state += (item['inventor_state'])
                    except TypeError:
                        inventor_state == (None)

                    try:
                        inventor_country += (item['inventor_country'])
                    except TypeError:
                        inventor_country == (None)

                else:
                    try:
                        inventor_name += (
                                    cell_list_delimiter + (item['inventor_name_first'] + ' ' + item['inventor_name_last']))
                    except TypeError:
                        inventor_name == (None)

                    try:
                        inventor_city += (cell_list_delimiter + item['inventor_city'])
                    except TypeError:
                        inventor_city == (None)

                    try:
                        inventor_state += (cell_list_delimiter + item['inventor_state'])
                    except TypeError:
                        inventor_state == (None)

                    try:
                        inventor_country += (cell_list_delimiter + item['inventor_country'])
                    except TypeError:
                        inventor_country == (None)

            new_json_item.update({"inventor_name": inventor_name})
            new_json_item.update({"inventor_city": inventor_city})
            new_json_item.update({"inventor_state": inventor_state})
            new_json_item.update({"inventor_country": inventor_country})

        except KeyError:
            new_json_item.update({"inventor_name": None})
            new_json_item.update({"inventor_city": None})
            new_json_item.update({"inventor_state": None})
            new_json_item.update({"inventor_country": None})

        new_json.append(new_json_item)
        new_json_item = {}
    pre_df = {'patents': new_json}
    return pre_df


# Iterate patents_json directory and convert each file to csv & save to ./patents_csv director
def convert_all_to_csv():

    # iterate years 2013 - 2024 end index exclusive.
    for year in range(2013, 2024, 1):
        # Load json to memory
        data = load_json(f'./patents_json/patents_{year}.json')

        # build pd.df from flattened json data
        pre_df = build_clean_dict(data)

        # normalize df and send to patents_csv/patents_{2013 + i}
        df = pd.json_normalize(pre_df['patents'])
        out_path = f'./patents_csv/patents_{year}.csv'
        df.to_csv(out_path)

convert_all_to_csv()
