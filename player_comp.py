import streamlit as st
import pandas as pd
from big_query_engine_code import load_dropdown_values
from big_query_engine_code import calculate_stats
import time
import matplotlib.pyplot as plt

def player_comp():
    def get_user_inputs():
        col1, col2, col3 = st.columns(3)
        with col1:
            player_name = st.multiselect('Player Name', load_dropdown_values('batter'))
        with col2:
            stats_type = st.selectbox('Stats Type', ['batting', 'bowling'])
        with col3:
            match_type = st.selectbox('Match Type',load_dropdown_values('match_type'))

        adv = st.checkbox('Advanced Options')

        # Set default values for advanced options
        date_from = None
        date_to = None
        series_name = None
        tournament_name = None
        batter_team = None
        bowler_team = None
        batter_type = None
        bowler_type = None
        venue = None
        overs_from = None
        overs_to = None

        # Call load_dropdown_values function once for each category
        series_name_options = load_dropdown_values('series_name')
        tournament_name_options = load_dropdown_values('tournament_name')
        player_team_options = load_dropdown_values('team_bat')
        opp_player_team_options = load_dropdown_values('team_bowl')
        venue_options = load_dropdown_values('venue')
        batter_type_options = load_dropdown_values('batter_hand') if stats_type == 'batting' else load_dropdown_values('bowler_type')
        bowler_type_options = load_dropdown_values('bowler_type') if stats_type == 'batting' else load_dropdown_values('batter_hand')

        if adv:
            col1, col2 = st.columns(2)
            with col1:
                date_from = st.date_input('Date From', pd.to_datetime('2000-01-01'))
            with col2:
                date_to = st.date_input('Date To', pd.to_datetime('2100-12-31'))
            with col1:
                series_name = st.multiselect('Series Name', options=series_name_options, placeholder='Select All')
                if not series_name:
                    series_name = None
            with col2:
                tournament_name = st.multiselect('Tournament Name', options=tournament_name_options, placeholder='Select All')
                if not tournament_name:
                    tournament_name = None

            col1, col2, col3 = st.columns(3)
            with col1:
                batter_team = st.multiselect('Player Team', options=player_team_options, placeholder='Select All')
                if not batter_team:
                    batter_team = None

            with col2:
                bowler_team = st.multiselect('Opponent Player Team', options=opp_player_team_options, placeholder='Select All')
                if not bowler_team:
                    bowler_team = None

            with col3:
                venue = st.multiselect('Venue', options=venue_options, placeholder='Select All')
                if not venue:
                    venue = None

            col1, col2 = st.columns(2)
            with col1:
                overs_from = st.number_input('Overs From', value=0)
            with col2:
                overs_to = st.number_input('Overs To', value=20)

            col1, col2 = st.columns(2)

            with col1:
                batter_type = st.multiselect('Player Type', options=batter_type_options, placeholder='Select All')
                if not batter_type:
                    batter_type = None

            with col2:
                bowler_type = st.multiselect('Opponent Player Type', options=bowler_type_options, placeholder='Select All')
                if not bowler_type:
                    bowler_type = None

        if stats_type == 'bowling':
            batter_type, bowler_type = bowler_type, batter_type
            batter_team, bowler_team = bowler_team, batter_team

        return {
            'function_type': 'player_comp',
            'batter_name': player_name,
            'stats_type': stats_type,
            'match_type': match_type,
            'adv': adv,
            'date_from': date_from,
            'date_to': date_to,
            'series_name': series_name,
            'tournament_name': tournament_name,
            'batter_team': batter_team,
            'bowler_team': bowler_team,
            'batter_type': batter_type,
            'bowler_type': bowler_type,
            'venue': venue,
            'overs_from': overs_from,
            'overs_to': overs_to
        }

    # Get user inputs
    params = get_user_inputs()

    # Add a submit button
    if st.button('Submit',key='pc'):
        # Calculate stats
        sta=time.time()
        df2 = calculate_stats( params)

        st.write(df2)
        st.write(f" time taken for query {time.time()-sta}")
        df=df2.head(10)
        df[df.columns[5]] = pd.to_numeric(df[df.columns[5]], errors='coerce')
        df[df.columns[6]] = pd.to_numeric(df[df.columns[6]], errors='coerce')
        fig, ax = plt.subplots()
        scatter = ax.scatter(df[df.columns[5]], df[df.columns[6]])
        
        # Annotate each point with the batsman name
        for i, row in df.iterrows():
            ax.annotate(row[df.columns[0]], (row[df.columns[5]], row[df.columns[6]]), textcoords="offset points", xytext=(0,10), ha='center')
        
        ax.set_title(f'{df.columns[5]} vs {df.columns[6]}')
        ax.set_xlabel(df.columns[5])
        ax.set_ylabel(df.columns[6])
        

            
        
        # Display plot in Streamlit
        st.pyplot(fig)

