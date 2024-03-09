import streamlit as st
from leader_board import leader_board
from matchup import matchup
from player_comp import player_comp
from player_search import player_search
from venue_stats import venue_search
import pandas as pd

file_path = r"C:\Users\adith\Documents\Projects\python-projects\cric_metric_clone\json_csv\csv_files\t20_matches_new_format.csv"  # replace with your file path
# if st.button('Rerun'): st.experimental_rerun()

# Load the dataframe
df = pd.read_csv(file_path) 


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