import streamlit as st
import pandas as pd
from stats import calculate_player_stats

file_path = r"C:\Users\adith\Documents\Projects\python-projects\cric_metric_clone\json_csv\csv_files\t20_matches_new_format.csv"  # replace with your file path
# if st.button('Rerun'): st.experimental_rerun()

# Load the dataframe
# df = pd.read_csv(file_path,low_memory=False)  # replace 'data.csv' with the path to your data file
# Q)what does set low_memory=false do in above command?
# A) 

# Define a function to get user inputs 
def player_search(df):

    def get_user_inputs():
        col1, col2, col3 = st.columns(3)
        with col1:
            player_name = st.selectbox('Player Name', df['Batsman'].unique())
        with col2:
            stats_type = st.selectbox('Stats Type', ['batting', 'bowling'])
        with col3:
            match_type = st.selectbox('Match Type', df['MatchType'].unique())
        with col1:
            group_by = st.selectbox('Group By', ['Season','Venue', 'LeagueName', 'BattingType', 'BowlingType'])
        adv = st.checkbox('Advanced Options')
        # Set default values for advanced options
        date_from = None
        date_to = None
        series_name = None
        tournament_name = None
        player_team = None
        opp_player_team = None
        opp_player_type = None
        venue = None
        overs_from = None
        overs_to = None

        if adv:
            col1, col2, col3 = st.columns(3)
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

            col1, col2, col3 = st.columns(3)
            with col1:
                tournament_name_options = df['TournamentName'].unique().tolist()
                tournament_name_options.insert(0, 'Select All')
                tournament_name = st.multiselect('Tournament Name', options=tournament_name_options, default='Select All')
                if 'Select All' in tournament_name:
                    tournament_name = df['TournamentName'].unique()

            with col2:
                player_team_options = df['BattingTeam'].unique().tolist()
                player_team_options.insert(0, 'Select All')
                player_team = st.multiselect('Player Team', options=player_team_options, default='Select All')
                if 'Select All' in player_team:
                    player_team = df['BattingTeam'].unique()

            with col3:
                opp_player_team_options = df['BattingTeam'].unique().tolist()
                opp_player_team_options.insert(0, 'Select All')
                opp_player_team = st.multiselect('Opponent Player Team', options=opp_player_team_options, default='Select All')
                if 'Select All' in opp_player_team:
                    opp_player_team = df['BowlingTeam'].unique()
            col1, col2 = st.columns(2)
            with col1:
                overs_from = st.number_input('Overs From', value=0)
            with col2:
                overs_to = st.number_input('Overs To', value=20)
            
            col1, col2 = st.columns(2)

            with col1:
                opp_player_type_options = df['BattingType'].unique().tolist()+df['BowlingType'].unique().tolist()
                opp_player_type_options.insert(0, 'Select All')
                opp_player_type = st.multiselect('Opponent Player Type', options=opp_player_type_options, default='Select All')
                if 'Select All' in opp_player_type:
                    opp_player_type = df['BattingType'].unique().tolist()+df['BowlingType'].unique().tolist()

        return {
            'player_name': player_name,
            'stats_type': stats_type,
            'match_type': match_type,
            'group_by': group_by,
            'adv': adv,
            'date_from': date_from,
            'date_to': date_to,
            'series_name': series_name,
            'tournament_name': tournament_name,
            'player_team': player_team,
            'opp_player_team': opp_player_team,
            'opp_player_type': opp_player_type,
            'venue': venue,
            'overs_from': overs_from,
            'overs_to': overs_to
        }

    # Get user inputs
    params = get_user_inputs()

    # Add a submit button
    if st.button('Submit',key='ps'):
        # Calculate stats
        stats = calculate_player_stats(df, params)
        # Display stats
        st.write(stats)
