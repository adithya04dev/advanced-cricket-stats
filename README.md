StatsViz: Interactive Cricket Analytics Dashboard


StatsViz is an interactive dashboard designed to deliver in-depth cricket analytics, allowing users to explore a wide range of statistics related to players, teams, venues, and matches. With StatsViz, you can gain insights into leaderboards for batters and bowlers, track performance by series, venue, and date, and filter data by player types (batter/bowler).

Features

Player Stats: Get detailed stats for individual players based on various filters such as venue, series, and time period.
Leaderboards: Access leaderboards for players and teams, categorized by performance in batting and bowling.
Venue Insights: Explore venue-specific statistics to understand how players and teams perform at different grounds.
Filters and Customization: Analyze data with customizable filters based on player type, match type, series, venue, date range, and more.
Real-time Data: Utilize real-time querying to calculate and display the latest stats.



Tech Stack

Streamlit: Simple yet powerful framework for building the interactive web UI.
SQL: Backend logic for calculating and retrieving cricket statistics.
Google Cloud BigQuery: Efficient execution of SQL queries over large datasets, enabling scalable and fast analytics.




Setup and Installation

Clone the repository:

git clone https://github.com/your-repo/statsviz.git
cd statsviz

Install required dependencies:
pip install -r requirements.txt

Set up Google Cloud BigQuery:
Ensure you have a Google Cloud project with BigQuery enabled.
Create a service account and download the credentials file.
Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to point to your credentials file:
export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_credentials_file.json"

Run the Streamlit App:

streamlit run main.py
