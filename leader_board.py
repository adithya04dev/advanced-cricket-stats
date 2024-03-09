import streamlit as st
import pandas as pd
from stats import calculate_leaderboard_stats
import streamlit as st
import pandas as pd

file_path = r"C:\Users\adith\Documents\Projects\python-projects\cric_metric_clone\json_csv\csv_files\t20_matches_new_format.csv"  # replace with your file path
# if st.button('Rerun'): st.experimental_rerun()

# Load the dataframe
# df = pd.read_csv(file_path)  # replace 'data.csv' with the path to your data file
def leader_board(df):
    # Define a function to get user inputs  
    def get_user_inputs():
        col1, col2, col3 = st.columns(3)
        with col1:
            analysis_type = st.selectbox('Analysis Type', ['player', 'team'])
        
        with col2:
            stats_type = st.selectbox('Stats Type', ['batting', 'bowling'])
        with col3:
            match_type = st.selectbox('Match Type', df['MatchType'].unique())
        
        adv = st.checkbox('Advanced Options')
        # Set default values for advanced options
        date_from = None
        date_to = None
        player_team = None
        opp_player_team = None
        opp_player_type = None
        series_name = None
        tournament_name = None
        venue = None
        overs_from = None
        overs_to = None

        if adv:
            col1, col2, col3,col4 = st.columns(4)
            with col1:
                date_from = st.date_input('Date From', pd.to_datetime('2022-01-01'))
            with col2:
                date_to = st.date_input('Date To', pd.to_datetime('2025-12-31'))
            with col3:
                series_name_options = df['SeriesName'].unique().tolist()
                series_name_options.insert(0, 'Select All')
                series_name = st.multiselect('Series Name', options=series_name_options, default='Select All')
                if 'Select All' in series_name:
                    series_name = df['SeriesName'].unique()
            with col4:
                tournament_name_options = df['TournamentName'].unique().tolist()
                tournament_name_options.insert(0, 'Select All')
                tournament_name = st.multiselect('Tournament Name', options=tournament_name_options, default='Select All')
                if 'Select All' in tournament_name:
                    tournament_name = df['TournamentName'].unique()

            

            col1, col2,col3 = st.columns(3)
            with col1:
                player_team_options = df['BattingTeam'].unique().tolist()
                player_team_options.insert(0, 'Select All')
                player_team = st.multiselect('Player Team', options=player_team_options, default='Select All')
                if 'Select All' in player_team:
                    player_team = df['BattingTeam'].unique()
            
            with col2:
                opp_player_team_options = df['BowlingTeam'].unique().tolist()
                opp_player_team_options.insert(0, 'Select All')
                opp_player_team = st.multiselect('Opponent Player Team', options=opp_player_team_options, default='Select All')
                if 'Select All' in opp_player_team:
                    opp_player_team = df['BowlingTeam'].unique()
            
            with col3:
                venue_options = df['Venue'].unique().tolist()
                venue_options.insert(0, 'Select All')
                venue = st.multiselect('Venue', options=venue_options, default='Select All')
                if 'Select All' in venue:
                    venue = df['Venue'].unique()
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
            'analysis_type': analysis_type,
            'stats_type': stats_type,
            'match_type': match_type,
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
    if st.button('Submit',key='l'):
        # Calculate stats
        stats = calculate_leaderboard_stats(df, params)
        # Display stats
        st.write(stats)
