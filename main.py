import streamlit as st
from leader_board import leader_board
from matchup import matchup
from player_comp import player_comp
from player_search import player_search
from venue_stats import venue_search
import pandas as pd

# file_path = r"C:\Users\adith\Documents\Projects\python-projects\cric_metric_clone\json_csv\csv_files\t20_matches_new_format.csv"  # replace with your file path
# if st.button('Rerun'): st.experimental_rerun()
# file_path='https://csvfiles-cricmetric-clone.s3.ap-south-1.amazonaws.com/t20_matches_with_types.csv?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBAaCmFwLXNvdXRoLTEiRzBFAiEA8hikMljYwKHQ0blrgTnhifb3itQ4zm1qHY70LfPbOf0CIAKBdM9zNCFKrawVWli8BXEJb9lhYum8RCntrpXvYPzxKuQCCBkQABoMODk3NzI2MDkxOTY1IgwH%2Fn8sFyOTfzrrbqoqwQJj2X%2BzZFdmico6upX%2BP5Nx5eYkKEwyMlN%2FcSFPF%2BObwadN4T%2Fc%2FH3G8J2OgT6sR%2B470%2FsJEHhRcITIJoL1p8Fk%2FGBL0e5rVEcG994OWPm%2FuLBpZJnOu2fcTH%2Bce81UKM%2Fuqjd2OEe4u%2BDBHutVV0eG9%2B3jPX955hj%2BRio71QS4MqlKDTLrMq%2B%2FKbwBHcMbxVpoHfxWxTQDhOP614coxaCxPRZLB9asAJW5yoqNTK5wyXeJm78pWimn7MzRstGpKPjPxwL7tZsNJ7xBrcghVPB9DQ3jLPMEc4rF5miyzVMxEP5cS4Gy0nrFJx17bWnafSrMQBWRJ4tWAVMLByW0SsFrcm3iLpj6NHs2TyvVwftBe21kclETOB%2F2ph1QdyqPpfPzUjLFUypMb1NhNSAk82Ms9BIVZhmBSqLoMKKcV6Or6IUwsbO3rwY6swKV3SIZeBAtOji2g3OiebVBxnLHAByWnBz2I%2Fa2vQpEFmNM2KnjIQ5cDs%2FKJr7Xuc3tjaI9UbNHNB06Awbc%2BCrXwo5cUx3EXVzVxDhNtQ1v1IKjWjnH4iOMaaG0AViQF4YL3cKWpO%2B1%2B%2FkMP1Y5di32QZa0DaKeQjrhiuEIosMpadq42pvKUEVCnsDhBZKO%2FJbk4Kz5a%2BI3UbDXCzYffeUjA%2FLlhivgoqZ6%2FE%2B8C4cXzwLdB9diugKEoPMsu6ELrY%2ByKUYQARgtM%2BFEqFFI12aQreJv4p6wMgUl2qLOIFgCWLDMpHWNzX8NyW%2BUhfIJlKx634D%2FstybLAgLNma%2F8JvLQ9LOXSl0sMq4Mkv33rhjDdCZo%2B7KmVCDQpitahB69u8I175MvBlfG6hwl6i0J9P9jG4P&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240310T160440Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA5CBFFCK63EXHE5O7%2F20240310%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Signature=2015599ff0ae5b623a1ceb27d6c46eb616cd91694f0dfd9969a741938a3f9387'
# Load the dataframe
# df = pd.read_csv(file_path) 
from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('s3', type=FilesConnection)
df = conn.read("csvfiles-cricmetric-clone/t20_matches_with_types.csv.csv", input_format="csv", ttl=600)

# Create a sidebar for navigation
option = st.selectbox(
    'Select an option',
    ['Leader Board', 'Matchup', 'Player Comparison', 'Player Search','Venue Search']
)

# Call the appropriate function based on the user's selection
if option == 'Leader Board':
    leader_board(df)
elif option == 'Matchup':
    matchup(df)
elif option == 'Player Comparison':
    player_comp(df)
elif option == 'Player Search':
    player_search(df)
elif option == 'Venue Search':
    venue_search(df)
