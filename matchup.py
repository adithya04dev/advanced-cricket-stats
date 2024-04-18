import pandas as pd
import streamlit as st
from big_query_engine_code import load_dropdown_values
from big_query_engine_code import calculate_stats
from big_query_engine_code import dropdown_values
def matchup():
    def get_user_inputs():
        col1, col2, col3 = st.columns(3)
        with col1:
            batter_name = st.multiselect('Batter Name', load_dropdown_values('batter'))
        with col2:
            bowler_name = st.multiselect('Bowler Name', load_dropdown_values('bowler'))
        with col3:
            group_by = st.selectbox('Group By', ['TournamentName', 'Venue', 'Batsman', 'Bowler'])
        adv = st.checkbox('Advanced Options')

        # Set default values for advanced options
        date_from = None
        date_to = None
        series_name = None
        tournament_name = None
        venue = None
        overs_from = None
        overs_to = None

        # Call load_dropdown_values function once for each category
        series_name_options = load_dropdown_values('series_name')
        tournament_name_options = load_dropdown_values('tournament_name')
        venue_options = load_dropdown_values('venue')

        if adv:
            col1, col2= st.columns(2)
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

            col1, col2 = st.columns(2)
            with col1:
                tournament_name = st.multiselect('Tournament Name', tournament_name_options)
                if not tournament_name:
                    tournament_name=None
            with col2:
                venue = st.multiselect('Venue', options=venue_options, placeholder='Select All')
                if not venue:
                    venue = None
            with col1:
                overs_from = st.number_input('Overs From', value=0)
            with col2:
                overs_to = st.number_input('Overs To', value=20)


        params = {
            'function_type': 'matchup',
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
        stats = calculate_stats(params)
        # Display stats
        st.write(stats)
