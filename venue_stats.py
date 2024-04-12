import streamlit as st
import pandas as pd
from stats import calculate_venue_stats
import plotly.express as px
from big_query_engine_code import load_dropdown_values
from big_query_engine_code import calculate_stats
def venue_search():
    def get_user_inputs():
        col1, col2 = st.columns(2)
        with col1:
            venue_name = st.selectbox('Venue Name', load_dropdown_values('Venue'))

        with col2:
            match_type = st.selectbox('Match Type', load_dropdown_values('MatchType'))

        adv = st.checkbox('Advanced Options')

        # Set default values for advanced options
        date_from = None
        date_to = None
        series_name = None
        tournament_name = None
        overs_from = None
        overs_to = None

        # Call load_dropdown_values function once for each category
        series_name_options = load_dropdown_values('SeriesName')
        tournament_name_options = load_dropdown_values('TournamentName')

        if adv:
            col1, col2, col3 = st.columns(3)
            with col1:
                date_from = st.date_input('Date From', pd.to_datetime('2000-01-01'))
            with col2:
                date_to = st.date_input('Date To', pd.to_datetime('2100-12-31'))
            with col3:
                series_name = st.multiselect('Series Name', options=series_name_options, placeholder='Select All')
                if not series_name:
                    series_name = None

            col1, col2, col3 = st.columns(3)
            with col1:
                tournament_name = st.multiselect('Tournament Name', options=tournament_name_options, placeholder='Select All')
                if not tournament_name:
                    tournament_name = None

            with col2:
                overs_from = st.number_input('Overs From', value=0)
            with col3:
                overs_to = st.number_input('Overs To', value=20)

        return {
            'function_type': 'venue_search',
            'venue_name': venue_name,
            'match_type': match_type,
            'adv': adv,
            'date_from': date_from,
            'date_to': date_to,
            'series_name': series_name,
            'tournament_name': tournament_name,
            'overs_from': overs_from,
            'overs_to': overs_to
        }

    # Get user inputs
    params = get_user_inputs()

    # Add a submit button
    if st.button('Submit',key='vs'):
        # Calculate stats
        # bt_stats, in_stats = calculate_venue_stats(params)
        stats = calculate_stats(params)
        # fig = px.bar(in_stats, x=in_stats.index, y='Average_Score', title='Average Score')
        # st.plotly_chart(fig)
        # fig = px.scatter(bt_stats, x='EconomyRate', y='BowlingAverage', color=bt_stats.index, title='Economy Rate vs Bowling Average')
        # st.plotly_chart(fig)

        # st.write(in_stats)
        st.write(stats)