# StatsViz: Interactive Cricket Analytics Dashboard and an AI tool.

**StatsViz** is an interactive dashboard designed to provide in-depth cricket analytics. It allows users to explore a wide range of statistics related to players, teams, venues, and matches. With StatsViz, you can gain insights into leaderboards for batters and bowlers, track performance by series, venue, and date, and filter data by player types (batter/bowler).   
It also includes an AI based tool that can calculate stats directly based on user text prompt by iteratively generating query and executing it in bigquery.

## Features

- **Player Stats**: Get detailed stats for individual players based on various filters such as venue, series, and time period.
- **Leaderboards**: Access leaderboards for players and teams, categorized by performance in batting and bowling.
- **Venue Insights**: Explore venue-specific statistics to understand how players and teams perform at different grounds.
- **Filters and Customization**: Analyze data with customizable filters based on player type, match type, series, venue, date range, and more.
- **Real-time Data**: Utilize real-time querying to calculate and display the latest stats.

## Tech Stack
- **Langgraph**: For making the the system  follow certain steps/stages iteratively.
- **Langchain**: Used to create tool calling agent(specifically ReAct) to search for correct names/events/venues that are actually present in database.
- **Streamlit**: Simple yet powerful framework for building the interactive web UI.
- **SQL**: Backend logic for calculating and retrieving cricket statistics.
- **Google Cloud BigQuery**: Efficient execution of SQL queries over large datasets, enabling scalable and fast analytics.

---
ScreenShots:  
![Alt text](./vector_databases/Screenshot%2024-10-08%203637.png)     
![Alt text](./vector_databases/Screenshot%2024-10-08%203637.png)    

## Text-Stats Architecture  

![Architecture](./vector_databases/Screenshot%202024-09-20%20085938.png)
![Architecture](./vector_databases/Screenshot%202024-09-20%20085949.png)



