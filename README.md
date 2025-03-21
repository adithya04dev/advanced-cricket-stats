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
### Screenshots:  
![Architecture Diagram](./vector_databases/Screenshot%202024-10-08%20203637.png)     
 
![Player Type Selection](./vector_databases/Screenshot%202024-10-08%20203648.png)    

## Extension of this Project  

-A conversational chatbot that can generate and execute sql query based on given natural language query on the cricket database.It can be built using two approaches.  

First  
-A chatbot that can generate sql query ,improve its response and execute. All of these intermediate functions controlled by user.  
-Thus giving more control to analyst, thus can handle complex workflow.  
Link : https://github.com/adithya04dev/CrickAI-SQL.    

Second (End to End)  
-A langraph agent that generates stats directly from natural language query.  
-Sometimes intermediate steps may not be accurate,but are faster to respond.  
-Implemented in statsguru.py file.   

## Text-> Stats Architecture   
Common part in both of the approaches.   
![Architecture](./vector_databases/Screenshot%202024-09-20%20085938.png)
![Architecture](./vector_databases/Screenshot%202024-09-20%20085949.png)


## Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/adithya04dev/advanced-cricket-stats.git
    cd advanced-cricket-stats
    ```
2.  **Set up a Virtual Environment (Recommended):**

    It's recommended to create a virtual environment to manage project dependencies separately. 

    ```bash
    python3 -m venv .venv
    .venv\Scripts\activate 
    ```

3.  **Install Dependencies:**

    Install the required Python packages using `pip`:

    ```bash
    pip install -r requirements.txt
    ```
4.  **Database Setup:**

    *   Ensure your BigQuery dataset and tables are created according to the schema used in your SQL queries. You'll need to load your cricket data into BigQuery. The specific table names and schema will depend on your project.
    *   Make sure that the service account key has appropriate permissions (read access) to the BigQuery dataset.
5.  **Run the Application:**

    ```bash
    streamlit run app.py  # Or the name of your main Streamlit file
    ```

    This command starts the Streamlit server, and you should be able to access the dashboard in your web browser (usually at `http://localhost:8501`).




