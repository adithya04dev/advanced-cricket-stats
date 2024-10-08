import streamlit as st
from leader_board import leader_board
from matchup import matchup
from player_comp import player_comp
from player_search import player_search
from venue_stats import venue_search
import pandas as pd
from statsguru import ask

# from dotenv import load_dotenv
# load_dotenv()
import os
# Create a sidebar for navigation
option = st.selectbox(
    'Select an option',
    ['Leader Board', 'Matchup', 'Player Comparison', 'Player Search','Venue Search']
)
# Call the appropriate function based on the user's selection
if option == 'Leader Board':
    leader_board()
elif option == 'Matchup':
    matchup()
elif option == 'Player Comparison':
    player_comp()
elif option == 'Player Search':
    player_search()
elif option == 'Venue Search':
    venue_search()
col1, col2 = st.columns([3, 1])  # Adjust the ratio as needed



st.write("Natural Language Querying ")
st.write("Approach 1: For text-sql visit below link ")
st.write("https://cricsql-f233a552789f.herokuapp.com/")
st.write("Approach 2: For text-stats")
with col1:
    question = st.text_input("Enter Your Query")

with col2:
    submit = st.button("Submit")

if submit and question:
    ask(question)
