import pandas as pd
from stats import calculate_matchup_stats
import streamlit as st

file_path = r"C:\Users\adith\Documents\Projects\python-projects\cric_metric_clone\json_csv\csv_files\t20_matches_new_format.csv"  # replace with your file path
# if st.button('Rerun', key='RerunButton1'): 
#     st.experimental_rerun()
# Load the dataframe
# df = pd.read_csv(file_path) 

def matchup(df):

    def get_user_inputs():
        col1, col2, col3 = st.columns(3)
        with col1:
            batter_name = st.multiselect('Batter Name', df['Batsman'].unique())
        with col2:
            bowler_name = st.multiselect('Bowler Name', df['Bowler'].unique())
        with col3:
            group_by = st.selectbox('Group By', ['LeagueName', 'Venue',  'Batsman', 'Bowler'])
        adv = st.checkbox('Advanced Options')
        date_from = None
        date_to = None
        series_name = None
        tournament_name = None
        venue = None
        overs_from = None
        overs_to = None

        if adv:
            col1, col2, col4 = st.columns(4)
            with col1:
                date_from = st.date_input('Date From', pd.to_datetime('2000-01-01'))
            with col2:
                date_to = st.date_input('Date To', pd.to_datetime('2100-12-31'))
            with col3:
                series_name_options = df['SeriesName'].unique().tolist()
                series_name_options.insert(0, 'Select All')
                series_name = st.multiselect('Series Name', options=series_name_options, default='Select All')
                if 'Select All' in series_name:
                    series_name = df['SeriesName'].unique()
        #addtournament_name_options
            with col4:
                tournament_name_options = df['TournamentName'].unique().tolist()
                tournament_name_options.insert(0, 'Select All')
                tournament_name = st.multiselect('Tournament Name', options=tournament_name_options, default='Select All')
                if 'Select All' in tournament_name:
                    tournament_name = df['TournamentName'].unique()
            col1, col2, col3 = st.columns(3)
            with col1:
                tournament_name = st.multiselect('Tournament Name', df['TournamentName'].unique())
            with col2:
                venue = st.multiselect('Venue', df['Venue'].unique())
            with col3:
                overs_from = st.number_input('Overs From', value=0)
            with col3:
                overs_to = st.number_input('Overs To', value=20)

        params = {
            'batter_name': batter_name,
            'bowler_name': bowler_name,
            'group_by': group_by,
            'adv': adv,
            'date_from': date_from,
            'date_to': date_to,
            'series_name': series_name,
            'tournament_name': tournament_name,
            'venue': venue,
            'overs_from': overs_from,
            'overs_to': overs_to
        }

        return params

    # Get user inputs
    params = get_user_inputs()

    # Add a submit button
    if st.button('Submit',key='m'):
        # Calculate stats
        stats = calculate_matchup_stats(df, params)
        # Display stats
        st.write(stats)
