## High Level Steps: 
## 1. Read URLs and APIKey
## 2. Populate data using Google API


#---------------------------------------------------------------------------------------------------------------
## Difference between GoogleSheets and WorkSheets
## GoogleSheet: The file within GoogleDrive which may contain one or multiple worksheets/tabs
## Worksheet: Tab/Sheet equivalent of Excel - contains actual data
#---------------------------------------------------------------------------------------------------------------

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from datetime import datetime
import requests
from urllib.parse import urlencode
import json
import pandas as pd

#---------------------------------------------------------------------------------------------------------------
## Constants
#---------------------------------------------------------------------------------------------------------------

# Names of the two GoogleSheets
RESULTS_GOOGLESHEET_NAME = "GoogleCoreWebVitalsDashboard_Results"
CONFIG_GOOGLESHEET_NAME = "GoogleCoreWebVitalsDashboard_Config"

# Names of worksheets/tabs within GoogleSheets
WORKSHEET_RESULTS_NAME = "Results"
WORKSHEET_CONFIG_PAGES_NAME = "Pages"
WORKSHEET_CONFIG_CREDENTIALS_NAME = "Credentials"

# Indexes of Worksheets/Tabs. Index starts from 0 so first sheet as index 0
WORKSHEET_RESULTS_INDEX = 0
WORKSHEET_CONFIG_PAGES_INDEX = 0
WORKSHEET_CONFIG_CREDENTIALS_INDEX = 1

# Last column in ActivitiesData sheet
RESULTS_SHEET_LAST_COLUMN = "U"

# Name of Google Service Account JSON Keypair File Name
SERVICE_ACCOUNT_CREDENTIALS_KEYFILE_NAME = "YOUR-SERVICE-ACCOUNT-JSON-FILE"


# Constant to define whether logs should be  printed. 
# Set the value to False if logs are not needed
DEBUG_LOGS_FLAG = True


# Function-name: next_available_row
# This function returns the row number of the next empty row of a Google Worksheet
# Input: Google Worksheet
# Output: Integer
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return len(str_list)+1

# A custom print function for debugging purposes
# it takes string as param
# checks whether DEBUG_LOGS is true; if yes prints the function
def myprint(str_to_print, end = "\n"):
    if DEBUG_LOGS_FLAG == True:
        print(str_to_print, end)
        
# Function to get all API Keys
def get_apikeys():
    print("x")
          
# Function to get API Key
def get_apikey(key_name):
    print("x")

# Function to get all Page-URLs
def get_page_urls():
    print("x")


## Funtion-name: clear_results_sheet_data
## This function clears data in Results sheet, leaving only header row
## Input: googlesheet - googlesheet object
## Input: worksheet - worksheet to be cleared
## Output: None
def clear_results_sheet_data(googlesheet, worksheet):
    googlesheet.values_clear(WORKSHEET_RESULTS_NAME + \
                                            "!A2:" + RESULTS_SHEET_LAST_COLUMN + str(next_available_row(worksheet)))

    
def main(data, context):
    #---------------------------------------------------------------------------------------------------------------
    ## Initialisations
    #---------------------------------------------------------------------------------------------------------------

    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    # SERVICE_ACCOUNT_CREDENTIALS_KEYFILE_NAME 
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_CREDENTIALS_KEYFILE_NAME, scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)

    # get the instances of both GoogleSheets
    googlesheet_config = client.open(CONFIG_GOOGLESHEET_NAME) 
    googlesheet_results = client.open(RESULTS_GOOGLESHEET_NAME) 

    # initialise all worksheets
    worksheet_config_pages = googlesheet_config.get_worksheet(WORKSHEET_CONFIG_PAGES_INDEX)
    worksheet_config_credentials = googlesheet_config.get_worksheet(WORKSHEET_CONFIG_CREDENTIALS_INDEX)
    worksheet_results = googlesheet_results.get_worksheet(WORKSHEET_RESULTS_INDEX)

    #---------------------------------------------------------------------------------------------------------------
    ## 1. Iterate through the Credentials worksheet to gather API
    #----------------------------------------------------------------------------------------------------------------

    # get data from Credentials worksheet
    credentials_data = worksheet_config_credentials.get_all_records()

    # convert credentials data to a Pandas dataframe
    credentials_df = pd.DataFrame.from_dict(credentials_data)
    
    config_keys_series = credentials_df.loc[:,'API-KEY']

    pagespeed_key_index = config_keys_series[config_keys_series == "Page-Speed"].index[0]
    pagespeed_key_value = credentials_df.loc[pagespeed_key_index,'VALUE']
    

    myprint("Key "+ pagespeed_key_value)
    
    #---------------------------------------------------------------------------------------------------------------
    ## 2. Get all the Pages for which report needs to be generated
    #----------------------------------------------------------------------------------------------------------------
    
    # get data from Pages worksheet
    pages_data = worksheet_config_pages.get_all_records()

    # convert credentials data to a Pandas dataframe
    pages_df = pd.DataFrame.from_dict(pages_data)
    
    pages_series = pages_df.loc[:,'PAGE-URL']

    myprint("Pages "+ str(pages_series))
    
    #---------------------------------------------------------------------------------------------------------------
    ## 3. Iterate through pages_series, extract data from Google API and populate the Results sheet
    #----------------------------------------------------------------------------------------------------------------
    
    if len(pages_series) > 0:
        # get data from Results worksheet and create a Dataframe
        existing_sheet_results_data = worksheet_results.get_all_records()
        existing_sheet_results_df = pd.DataFrame.from_dict(existing_sheet_results_data)

        # get the count of existing data in Results sheet
        existing_sheet_results_count = len(existing_sheet_results_df.index)

        # if no existing results then create a list of all google data and update the sheet
        if existing_sheet_results_count == 0:
            # list to hold activity list - A list of lists that will be written to the googlesheet
            toupload_results_list = []
        else:
            # if there are existing activities in AcvitiesSheet then put the data into a list of lists
            # each list represents row for an activity
            # We'll also clear all the content excpet the header row
            # as I could not find a way to replace rows in gspread package - SUGGESTIONS WELCOME
            toupload_results_list = existing_sheet_results_df.values.tolist()
            # clear the content of Results sheet
            clear_results_sheet_data(googlesheet_results, worksheet_results)
            
        
        for page_url in pages_series:
            toupload_result_list = [''] *10
            
            toupload_result_list[0] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            toupload_result_list[1] = datetime.now().strftime('%Y-%m-%d')
            toupload_result_list[2] = datetime.now().strftime('%H:%M:%S')
            toupload_result_list[3] = page_url
            
            # first get data for desktop
            api_url_desktop = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + page_url + '&key=' + pagespeed_key_value + '&strategy=desktop'
            
             # send http request
            res = requests.get(api_url_desktop)
                       
            if res.status_code == 200:
                res_json_data = json.loads(res.text)
                toupload_result_list[4] = res_json_data['lighthouseResult']['categories']['performance']['score'] *100
                toupload_result_list[5] = res_json_data['lighthouseResult']['audits']['metrics']['details']['items'][0]['firstContentfulPaint'] / 1000
                toupload_result_list[6] = res_json_data['lighthouseResult']['audits']['metrics']['details']['items'][0]['speedIndex'] / 1000
            
            # first get data for mobile
            api_url_mobile = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + page_url + '&key=' + pagespeed_key_value + '&strategy=mobile'
            
             # send http request
            res = requests.get(api_url_mobile)
                       
            if res.status_code == 200:
                res_json_data = json.loads(res.text)
                toupload_result_list[7] = res_json_data['lighthouseResult']['categories']['performance']['score'] * 100
                toupload_result_list[8] = res_json_data['lighthouseResult']['audits']['metrics']['details']['items'][0]['firstContentfulPaint'] / 1000
                toupload_result_list[9] = res_json_data['lighthouseResult']['audits']['metrics']['details']['items'][0]['speedIndex'] / 1000
            
            toupload_results_list.append(toupload_result_list)
        
        worksheet_results.append_rows(toupload_results_list, 2)  

if __name__ == "__main__":
    main('data','context')
