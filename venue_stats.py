import streamlit as st
import pandas as pd
from stats import calculate_venue_stats
import plotly.express as px

file_path = r"C:\Users\adith\Documents\Projects\python-projects\cric_metric_clone\json_csv\csv_files\t20_matches_new_format.csv"  # replace with your file path
# if st.button('Rerun'): st.experimental_rerun()

# Load the dataframe
# df = pd.read_csv(file_path)  # replace 'data.csv' with the path to your data file
def venue_search(df):
        
    # Define a function to get user inputs 
    def get_user_inputs():
        col1, col2 = st.columns(2)
        with col1:
            venue_name = st.selectbox('VenueName', df['Venue'].unique())

        with col2:
            match_type = st.selectbox('Match Type', df['MatchType'].unique())

        adv = st.checkbox('Advanced Options')
        # Set default values for advanced options
        date_from = None
        date_to = None
        series_name = None
        tournament_name = None

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


            with col1:
                overs_from = st.number_input('Overs From', value=0)
            with col2:
                overs_to = st.number_input('Overs To', value=20)
            
            col1, col2 = st.columns(2)



        return {
            'player_name': venue_name,
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
        bt_stats,in_stats = calculate_venue_stats(df, params)
        
        fig = px.bar(in_stats, x=in_stats.index, y='Average_Score', title='Average Score')
        st.plotly_chart(fig)
        fig = px.scatter(bt_stats, x='EconomyRate', y='BowlingAverage', color=bt_stats.index, title='Economy Rate vs Bowling Average')
        st.plotly_chart(fig)    

        #bar graph to plot in_stats y_axis to be Average_Score

        st.write()
        st.write(in_stats)    
        st.write(bt_stats)
