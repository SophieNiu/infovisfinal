# infovisfinal

## Start the program
Install the dash python package 
""pip install dash""
Then run the map_dash.py code, it would open up a local server developmental page of our demo. We are deploying it to a personal server that one of our teammate has but it may not come soon. 

## Data Cleaning
In the original dataset, there is a column called __GeoName__ which has names of the county/CBSA and states separated by comma. We separated them and put them into several columns.
New file was called _climate_dataset_cleaned_v1.0.csv_ in the file _dataset_.
* added columns

    | New Columns | Description |
    | --- | ---- |
    | GeoName_new | GeoName without States |
    | StateName_raw | State names extracted from GeoName. Some are abbreviations |
    | StateName | State names with no abbreviations |
    | IsMultiState | Some counties include area in several states. int 1 means True |
    | NumStates | Number of states one county belongs to |
    | StateName_1 | The first state |
    | StateName_2 | The second state. "Empty" means NaN |
    | StateName_3 | Same as above |
    | StateName_4 | Same as above | 
* There are 4 geographic types:
  1. National
  2. State
  3. County
  4. CBSA - Core-based statistical area
  5. cd113 - have no idea what it means
* About column  __TotalPop__
  Since some counties include areas in several states, the sum of __TotalPop__ for all the counties in one state may not equal to the __TotalPop__ of one state.You can find more information in the code.
