import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
## you can comment the following 2 lines if you run the code in Jupyter Notebook/Lab
# pd.set_option("display.max_columns", None)
# pd.set_option("display.max_row", None)
"""
Author: Yixian Zhou, ...
Date: Nov. 9
What is for: Exploaration. Data Cleaning: extrated state names from the GeoName and added some columns
"""

####### SET UP #######
Write_to_file = False ## Don't change if if you just want to run the code and see what it does
STATE_ABBR = """Alabama - AL
Alaska - AK
Arizona - AZ
Arkansas - AR
California - CA
Colorado - CO
Connecticut - CT
District of Columbia - DC
Delaware - DE
Florida - FL
Georgia - GA
Hawaii - HI
Idaho - ID
Illinois - IL
Indiana - IN
Iowa - IA
Kansas - KS
Kentucky - KY
Louisiana - LA
Maine - ME
Maryland - MD
Massachusetts - MA
Michigan - MI
Minnesota - MN
Mississippi - MS
Missouri - MO
Montana - MT
Nebraska - NE
Nevada - NV
New Hampshire - NH
New Jersey - NJ
New Mexico - NM
New York - NY
North Carolina - NC
North Dakota - ND
Ohio - OH
Oklahoma - OK
Oregon - OR
Pennsylvania - PA
Rhode Island - RI
South Carolina - SC
South Dakota - SD
Tennessee - TN
Texas - TX
Utah - UT
Vermont - VT
Virginia - VA
Washington - WA
West Virginia - WV
Wisconsin - WI
Wyoming - WY"""
MAX_NUM_STATE = 4
DATA_PATH = "./dataset"
FILENAME = "./dataset/climate_dataset_cleaned_v1.0.csv"
NUM_STATES = 51 ## well... it should be 50 but they included District of Columbia
def is_multi_state(s):
    """return 1 if the county is a multi-state area"""
    if "-" in s:
        return 1
    else:
        return 0

def get_num_states(s):
    """return the number of states"""
    if ("US" in s):
        return NUM_STATES
    _state_list = s.split('-')
    return len(_state_list)

def convert2full(s, abbr2full):
    """convert abbreviations to full names"""
    if ("US" in s) | (len(s) > 2) & ("-" not in s) : # record for country # record for states
        return s        
    elif "-" in s:
        return "-".join([abbr2full[abbr] for abbr in s.split("-")])
    else:
        return abbr2full[s]

####### LOAD DATA AND DATA CLEANING #######
climate = pd.read_csv(f"{DATA_PATH}/YCOM_2016_Data.01.csv")
metadata = pd.read_csv(f"{DATA_PATH}/YCOM_Metadata_2017Feb20.csv")

raw_cols = list(climate.columns)
pair_list = STATE_ABBR.split('\n')
abbr2full = {s.split('-')[1].strip(): s.split('-')[0].strip() for s in pair_list} # abbr_dict = {}

climate['StateName_raw'] = climate['GeoName'].str.split(", ").str[-1]
climate['StateName'] = climate['StateName_raw'].apply(lambda x: convert2full(x, abbr2full))
climate['GeoName_new'] = climate['GeoName'].str.split(", ").str[0]
# climate = climate[np.insert(climate.columns, 3, "GeoName_new")[:-1]] move columns name
climate['IsMultiState'] = climate['StateName_raw'].apply(lambda x: is_multi_state(x))
climate['NumStates'] = climate['StateName_raw'].apply(lambda x: get_num_states(x))

for i in range(MAX_NUM_STATE):
    climate[f'StateName_{i + 1}'] = climate['StateName'].str.split('-').str[i].str.strip()
    climate[f'StateName_{i + 1}'] = climate[f'StateName_{i + 1}'].fillna("Empty")

climate = climate[raw_cols[:3] + ['GeoName_new', 'StateName_raw', 'StateName', 'IsMultiState', 'NumStates'] + \
                  [f"StateName_{i + 1}" for i in range(MAX_NUM_STATE)] + raw_cols[3:]]

if Write_to_file:
    climate.to_csv(FILENAME, index=False)

###### SOMETHINE ELSE ######
print("Total Pop...")
print("Total population of all the counties in Alabama:", climate[(climate['StateName'].str.contains("\w*Alabama\w*")) & (climate['GeoType'] != 'State')]['TotalPop'].sum())
print("Total population in Alabama:", climate[(climate['StateName'] == "Alabama") & (climate['GeoType'] == 'State')]['TotalPop'].sum())
print("Different GeoType")
print(climate['GeoType'].value_counts())

print(f"Number of States: {len(climate[climate['GeoType'] == 'State'])}")
print("List of States in the dataset:\n", list(climate[climate['GeoType'] == "State"]["GeoName"]))

print("All the columns:\n", list(climate.columns))