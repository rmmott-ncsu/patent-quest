import requests
import json
from time import sleep

API_KEY = "G1ltQBOe.xBsGCvH18RmZ7Sm9ALUZCorc9Jyk6WSh"
BASE_URL = "https://search.patentsview.org/api/v1"

# Change for batch size. Max = 1000
STEP_SIZE = 1000

# Start 8341762 01-01-2013, End 11665988 06/01/2023

# Get batch of patents from patent_id_low -> patent_id_high from patentsview API
# batch size 100 for testing
def get_patents(patent_id_low: str, patent_id_high: str) -> list:
    print(patent_id_low, patent_id_high)

    # Request parameters. Got to be a better way to do this...
    request_query = f"{{\"_and\":[{{\"_gte\":{{\"patent_id\":\"{patent_id_low}\"}}}},{{\"_lte\":{{\"patent_id\":\"{patent_id_high}\"}}}}]}}"
    request_format = f"[\"patent_id\",\"application.application_id\",\"application.filing_date\",\"application_type\",\"applicants.applicant_name_first\",\"applicants.applicant_name_last\",\"applicants.applicant_organization\",\"assignees.assignee_individual_name_first\",\"assignees.assignee_individual_name_last\",\"assignees.assignee_organization\",\"inventors.inventor_city\",\"inventors.inventor_country\",\"inventors.inventor_name_first\",\"inventors.inventor_name_last\",\"inventors.inventor_state\",\"cpc_current\",\"patent_title\",\"patent_date\",\"patent_abstract\"]"
    request_o = f"{{\"size\": {STEP_SIZE}}}"

    # Build URL with base and request parameters
    patents_url = BASE_URL + f"/patent/?q={request_query}&f={request_format}&o={request_o}"
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    # print(patents_url)
    # Call API
    response = requests.get(patents_url, headers=headers)
    # Set json response to dict object
    response_json = response.json()
    print(response_json)
    # return patents list from dict
    return response_json["patents"]


# Create json file and iteratively call patents API
def get_all_patents(start_id: int, end_id: int, outfile: str):
    # Create or overwrite existing file and set up patents object for valid json
    with open(outfile, "w") as file:
        file.write("{\n    \"patents\": [\n")
        file.close()

    # Loop API requests from start_id to end_id and write to patent
    while start_id < end_id:
        patent_batch = get_patents(str(start_id), str(start_id + STEP_SIZE))
        print(patent_batch)
        last_id = 0

        # Iteratively append patent objects to file
        with open(outfile, "a") as file:
            for patent in patent_batch:

                current_id = int(patent['patent_id'])

                # API responding with dups. first response w/ given id does NOT have CNC field. Writing second
                # response to output file.
                if current_id == last_id and current_id < end_id - 1:
                    json.dump(patent, file, indent=4, sort_keys=False, ensure_ascii=True)
                    file.write(",\n")

                # Don't append trailing comma for last element in json file for ~valid~ json
                elif current_id == last_id and current_id == end_id - 1:
                    json.dump(patent, file, indent=4, sort_keys=False, ensure_ascii=True)
                    file.write("\n")
                last_id = current_id
            file.close()

        # Avoid request limit?
        sleep(1.5)
        start_id = last_id + 1

    # close out patents list and bracket for valid json file
    with open(outfile, "a") as file:
        file.write("]\n}")
        file.close()


def main():
    # Start 8341762 01-01-2013, End 11665988 06/01/2023

    # Create JSON files by year.

    # 2013: [8341762 - 8621662)
    # get_all_patents(8341762, 8621662, 'patents_2013.json')

    # 2014: [8621662 - 8925112)
    get_all_patents(8621662, 8925112, 'patents_2014.json')

    # # 2015: [8925112, 9226437)
    # get_all_patents(8925112, 9226437, 'patents_2015.json')
    #
    # # 2016: [9226437, 9532496)
    # get_all_patents(9226437, 9532496, 'patents_2016.json')
    #
    # # 2017: [9532496, 9854721)
    # get_all_patents(9532496, 9854721, 'patents_2017.json')
    #
    # # 2018: [9854721, 10165721)
    # get_all_patents(9854721, 10165721, 'patents_2018.json')
    #
    # # 2019: [10165721, 10524402)
    # get_all_patents(10165721, 10524402, 'patents_2019.json')
    #
    # # 2020: [10524402, 10881042)
    # get_all_patents(10524402, 10881042, 'patents_2020.json')
    #
    # # 2021: [10881042, 11212952)
    # get_all_patents(10881042, 11212952, 'patents_2021.json')
    #
    # # 022: [11212952, 11540434)
    # get_all_patents(11212952, 11540434, 'patents_2022.json')
    #
    # # 2023: [11540434, 11665988)
    # get_all_patents(11540434, 11665988, 'patents_2023.json')


if __name__ == '__main__':
    main()