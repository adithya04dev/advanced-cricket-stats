import os

import pandas as pd
from google.cloud import bigquery
import base64
import json
import google.auth
from google.oauth2 import service_account

# Load the credentials from the environment variable
credentials_b64 = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
credentials_bytes = base64.b64decode(credentials_b64)
credentials_dict = json.loads(credentials_bytes)

# Create a Credentials object from the loaded dictionary
credentials = service_account.Credentials.from_service_account_info(credentials_dict)


import pandas as pd
from google.cloud import bigquery

import mysql.connector
from mysql.connector import errorcode
import json

# Database connection details (replace with your actual credentials)
db_config = {
    'host': 'your_mysql_host',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'database': 'your_mysql_database'
}
#if credentials not in env variables, then use the db_config dictionary
try:
    db_config['host'] = os.environ.get("MYSQL_HOST")
    db_config['user'] = os.environ.get("MYSQL_USER")
    db_config['password'] = os.environ.get("MYSQL_PASSWORD")
    db_config['database'] = os.environ.get("MYSQL_DATABASE")

except Exception as e:
    print("Error while loading credentials from environment variables")
    print(e)
    print("Using default credentials")



def query_to_dataframe_mysql(query):
    """Executes a MySQL query and returns the result as a Pandas DataFrame."""
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        cursor.execute(query)
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Get column names from the cursor description
        columns = [col[0] for col in cursor.description]

        df = pd.DataFrame(rows, columns=columns)
        return df

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return pd.DataFrame() # Return an empty DataFrame on error
    finally:
        if 'cnx' in locals() and cnx.is_connected():
            cursor.close()
            cnx.close()

def query_to_dataframe( query):
    project_id = 'adept-cosine-420005'

    client = bigquery.Client(project=project_id,credentials=credentials)

    # Execute the query
    query_job = client.query(query)
    query_job.result()

    df = query_job.to_dataframe()

    return df
params = {
    'function_type': 'player_search',
    # 'analysis_type': 'player',
    'stats_type': 'batting',
    'match_type': 'T20',
    'date_from': '2022-02-01',
    'date_to': '2023-09-30',
    # 'batter_team': ('Lahore Qalandars', 'Sri Lanka'),
    # 'bowler_team': ('Afghanistan',),
    "batter_name":['V Kohli'],
    'series_name': ['Asia Cup'],
    'tournament_name': ['Asia Cup2022'],
    'group_by':'Inning_Number',
    # 'venue': ("Gaddafi Stadium Lahore", "Dubai International Cricket Stadium", "Sharjah Cricket Stadium"),
    # 'overs_from': 1,
    # 'overs_to': 20
}
def convert_to_sql_query(params):
    # Standardize input parameters
    for key in ['batter_name','bowler_name','inninggs_number','venue','batter_team', 'bowler_team', 'series_name', 'tournament_name', 'venue', 'batter_type','bowler_type']:
        if key in params and isinstance(params[key], list):
            params[key] = tuple(params[key])
            # print("hello")

    # Build the SQL query
    database ='bbbdata'
    # table = 'ballsnew'
    table='ballsnew_2406'

    function_type = params.get('function_type')
    analysis_type = params.get('analysis_type')

    stats_type = params.get('stats_type')
    match_type = params.get('match_type')
    date_from = params.get('date_from')
    date_to = params.get('date_to')
    group_by = params.get('group_by')
    venue = params.get('venue')
    inninggs_number = params.get('inninggs_number')
    batter_name = params.get('batter_name')
    bowler_name = params.get('bowler_name')
    batter_team = params.get('batter_team')
    bowler_team = params.get('bowler_team')
    batter_type = params.get('batter_type')
    bowler_type = params.get('bowler_type')

    series_name = params.get('series_name')
    tournament_name = params.get('tournament_name')
    venue = params.get('venue')

    overs_from = params.get('overs_from')
    overs_to = params.get('overs_to')
    condition=''

    if match_type !=None:
        condition+= f"match_type = '{match_type}'"

    if date_from is not None :
        condition += f" AND date >= '{date_from}'"
    if date_to is not None:
        condition += f" AND date <= '{date_to}'"
    if series_name is not None:
        condition += f" AND series_name IN {series_name}"
    if tournament_name is not None:
        condition += f" AND tournament_name IN {tournament_name}"
    if venue is not None:
        condition += f" AND venue IN {venue}"
    if overs_from is not None and overs_to is not None:
        condition += f" AND overs BETWEEN {overs_from} AND {overs_to}"
    if batter_name is not None:
        condition += f" AND batter IN {batter_name}"
    if bowler_name is not None:
        condition += f" AND bowler IN {bowler_name}"
    if batter_team is not None:
        condition += f" AND team_bat IN {batter_team}"
    if bowler_team  is not None:
        condition += f" AND team_bowl IN {bowler_team}"
    if batter_type is not None:
        condition += f" AND batter_hand IN {batter_type}"
    if bowler_type is not None:
        condition += f" AND bowler_type IN {bowler_type}"
    if venue is not None:
        condition += f" AND venue IN {venue}"
    if inninggs_number is not None:
        condition += f" AND current_match_inning_number IN {inninggs_number}"
    condition=condition.replace(',)',')')
    if match_type ==None:
        condition =condition.replace('AND',' ',1)
    
    if function_type == 'leaderboard':
        if analysis_type == 'player':
            if stats_type == 'batting':
                sql_query = f"""
                WITH stats AS (
                SELECT
                    batter as Batsman,
                    COUNT(DISTINCT match_no) AS Innings,
                    SUM(batter_runs) AS Runs,
                    SUM(balls_faced) AS BallsFaced,
                    SUM(out) AS Outs,
                    SUM(CASE WHEN score=0 THEN 1 ELSE 0 END) AS DotBallsFaced,
                    SUM(CASE WHEN batter_runs IN (4, 6) THEN 1 ELSE 0 END) AS BoundaryBalls
                FROM {database}.{table}
                WHERE {condition}
                GROUP BY batter
                ),
                calculations AS (
                SELECT
                    Batsman,
                    Innings,
                    Runs,
                    BallsFaced,
                    Outs,
                    COALESCE(Runs / NULLIF(Outs, 0), 0) AS Average,
                    COALESCE((Runs / NULLIF(BallsFaced, 0)) * 100, 0) AS StrikeRate,
                    COALESCE((DotBallsFaced / NULLIF(BallsFaced, 0)) * 100, 0) AS DotBallPercentage,
                    COALESCE((BoundaryBalls / NULLIF(BallsFaced, 0)) * 100, 0) AS BoundaryPercentage
                FROM stats
                )
                SELECT
                Batsman,
                Innings,
                Runs,
                BallsFaced,
                Outs,
                Average,
                StrikeRate,
                DotBallPercentage,
                BoundaryPercentage
                FROM calculations
                ORDER BY Runs DESC;
                """
            elif stats_type == 'bowling':
                sql_query = f"""
                WITH stats AS (
                SELECT
                    bowler as Bowler,
                    COUNT(DISTINCT match_no) AS Innings,
                    SUM(out) AS Wickets,
                    SUM(bowler_runs) AS RunsConceded,
                    SUM(balls_faced) AS BallsBowled,
                    SUM(CASE WHEN score=0 THEN 1 ELSE 0 END) AS DotBallsBowled,
                    SUM(CASE WHEN batter_runs IN (4, 6) THEN 1 ELSE 0 END) AS BoundaryBalls
                FROM {database}.{table}
                WHERE {condition}
                GROUP BY bowler
                ),
                calculations AS (
                SELECT
                    Bowler,
                    Innings,
                    Wickets,
                    RunsConceded,
                    BallsBowled,
                    COALESCE(RunsConceded / NULLIF(Wickets, 0), 0) AS Average,
                    COALESCE((RunsConceded / NULLIF(BallsBowled, 0)) * 6, 0) AS EconomyRate,
                    COALESCE((DotBallsBowled / NULLIF(BallsBowled, 0)) * 100, 0) AS DotBallPercentage,
                    COALESCE((BoundaryBalls / NULLIF(BallsBowled, 0)) * 100, 0) AS BoundaryPercentage
                FROM stats
                )
                SELECT
                Bowler,
                Innings,
                Wickets,
                RunsConceded,
                BallsBowled,
                Average,
                EconomyRate,
                DotBallPercentage,
                BoundaryPercentage
                FROM calculations
                ORDER BY Wickets DESC;
                """
        elif analysis_type == 'team':
            if stats_type == 'batting':
                sql_query = f"""
                WITH stats AS (
                SELECT
                    team_bat as BattingTeam,
                    COUNT(DISTINCT match_no) AS Innings,
                    SUM(score) AS Runs,
                    SUM(balls_faced) AS BallsFaced,
                    SUM(out) AS Outs,
                    SUM(CASE WHEN score=0 THEN 1 ELSE 0 END) AS DotBallsFaced,
                    SUM(CASE WHEN batter_runs IN (4, 6) THEN 1 ELSE 0 END) AS BoundaryBalls
                FROM {database}.{table}
                WHERE {condition}
                GROUP BY BattingTeam
                ),
                calculations AS (
                SELECT
                    BattingTeam,
                    Innings,
                    Runs,
                    BallsFaced,
                    Outs,
                    COALESCE(Runs / NULLIF(Outs, 0), 0) AS Average,
                    COALESCE((Runs / NULLIF(BallsFaced, 0)) * 100, 0) AS StrikeRate,
                    COALESCE((DotBallsFaced / NULLIF(BallsFaced, 0)) * 100, 0) AS DotBallPercentage,
                    COALESCE((BoundaryBalls / NULLIF(BallsFaced, 0)) * 100, 0) AS BoundaryPercentage
                FROM stats
                )
                SELECT
                BattingTeam,
                Innings,
                Runs,
                BallsFaced,
                Outs,
                Average,
                StrikeRate,
                DotBallPercentage,
                BoundaryPercentage
                FROM calculations
                ORDER BY Runs DESC;
                """
            elif stats_type == 'bowling':
                sql_query = f"""
                WITH stats AS (
                SELECT
                    team_bowl as BowlingTeam,
                    COUNT(DISTINCT match_no) AS Innings,
                    SUM(out) AS Wickets,
                    SUM(bowler_runs) AS RunsConceded,
                    SUM(balls_faced) AS BallsBowled,
                    SUM(CASE WHEN score=0 THEN 1 ELSE 0 END) AS DotBallsBowled,
                    SUM(CASE WHEN batter_runs IN (4, 6) THEN 1 ELSE 0 END) AS BoundaryBalls
                FROM {database}.{table}
                WHERE {condition}
                GROUP BY BowlingTeam
                ),
                calculations AS (
                SELECT
                    BowlingTeam,
                    Innings,
                    Wickets,
                    RunsConceded,
                    BallsBowled,
                    COALESCE(RunsConceded / NULLIF(Wickets, 0), 0) AS Average,
                    COALESCE((RunsConceded / NULLIF(BallsBowled, 0)) * 6, 0) AS EconomyRate,
                    COALESCE((DotBallsBowled / NULLIF(BallsBowled, 0)) * 100, 0) AS DotBallPercentage,
                    COALESCE((BoundaryBalls / NULLIF(BallsBowled, 0)) * 100, 0) AS BoundaryPercentage
                FROM stats
                )
                SELECT
                BowlingTeam,
                Innings,
                Wickets,
                RunsConceded,
                BallsBowled,
                Average,
                EconomyRate,
                DotBallPercentage,
                BoundaryPercentage
                FROM calculations
                ORDER BY Wickets DESC;
                """
    
    elif function_type == 'player_search':
        if stats_type == 'batting':
            sql_query = f"""
            WITH stats AS (
                SELECT {group_by}, COUNT(DISTINCT match_no) as Innings, SUM(batter_runs) as Runs, SUM(balls_faced) as BallsFaced, SUM(out) as Outs,
                        SUM(CASE WHEN score=0 THEN 1 ELSE 0 END) AS DotBallsFaced,
                        SUM(CASE WHEN batter_runs IN (4, 6) THEN 1 ELSE 0 END) AS BoundaryBalls
                FROM {database}.{table}
                WHERE {condition}
                GROUP BY {group_by}
            ),
            calculations AS (
                SELECT {group_by}, Innings, Runs, BallsFaced, Outs, 
                    COALESCE(Runs / NULLIF(Outs, 0), 0) AS Average, 
                    COALESCE((Runs / NULLIF(BallsFaced, 0)) * 100, 0) AS StrikeRate,
                    COALESCE((DotBallsFaced / NULLIF(BallsFaced, 0)) * 100, 0) AS DotBallPercentage,
                    COALESCE((BoundaryBalls / NULLIF(BallsFaced, 0)) * 100, 0) AS BoundaryPercentage
                FROM stats
            )
            SELECT {group_by}, Innings, Runs, BallsFaced, Outs, Average, StrikeRate, DotBallPercentage, BoundaryPercentage
            FROM calculations
            ORDER BY Runs DESC;
            """
        elif stats_type == 'bowling':
            sql_query = f"""
            WITH stats AS (
                SELECT {group_by}, COUNT(DISTINCT match_no) as Innings, 
                    SUM(balls_faced) as BallsBowled,
                    SUM(out) as Wickets, 
                    SUM(bowler_runs) as RunsConceded, 
                    SUM(CASE WHEN score=0 THEN 1 ELSE 0 END) AS DotBallsBowled,
                    SUM(CASE WHEN batter_runs IN (4, 6) THEN 1 ELSE 0 END) AS BoundaryBalls
                FROM {database}.{table}
                WHERE {condition}
                GROUP BY {group_by}
            ),
            calculations AS (
                SELECT {group_by}, Innings, Wickets, RunsConceded, BallsBowled,  
                    COALESCE(RunsConceded / NULLIF(Wickets, 0), 0) AS Average,
                    COALESCE((RunsConceded / NULLIF(BallsBowled, 0)) * 6, 0) AS EconomyRate,
                    COALESCE((DotBallsBowled / NULLIF(BallsBowled, 0)) * 100, 0) AS DotBallPercentage,
                    COALESCE((BoundaryBalls / NULLIF(BallsBowled, 0)) * 100, 0) AS BoundaryPercentage
                FROM stats
            )
            SELECT {group_by}, Innings, Wickets, RunsConceded, BallsBowled, Average, EconomyRate, DotBallPercentage, BoundaryPercentage
            FROM calculations
            ORDER BY Wickets DESC;
            """
    
    elif function_type == 'matchup':
        sql_query = f"""
        WITH stats AS (
        SELECT {group_by},
            COUNT(DISTINCT match_no) as Innings,
            SUM(batter_runs) as Runs,
            SUM(balls_faced) as BallsFaced,
            SUM(out) as Outs,
            SUM(CASE WHEN score=0 THEN 1 ELSE 0 END) AS DotBallsFaced,
            SUM(CASE WHEN batter_runs IN (4, 6) THEN 1 ELSE 0 END) AS BoundaryBalls
        FROM {database}.{table}
        WHERE {condition}
        GROUP BY {group_by}
        ),
        calculations AS (
        SELECT {group_by},
            Innings,
            Runs,
            BallsFaced,
            Outs,
            COALESCE(Runs / NULLIF(Outs, 0), 0) AS Average,
            COALESCE((Runs / NULLIF(BallsFaced, 0)) * 100, 0) AS StrikeRate,
            COALESCE((DotBallsFaced / NULLIF(BallsFaced, 0)) * 100, 0) AS DotBallPercentage,
            COALESCE((BoundaryBalls / NULLIF(BallsFaced, 0)) * 100, 0) AS BoundaryPercentage
        FROM stats
        )
        SELECT {group_by},
        Innings,
        Runs,
        BallsFaced,
        Outs,
        Average,
        StrikeRate,
        DotBallPercentage,
        BoundaryPercentage
        FROM calculations
        ORDER BY Runs DESC;
        """
    
    elif function_type == 'venue_search':
        sql_query = f"""
        WITH stats AS (
          SELECT
            bowler_type as BowlingType,
            SUM(batter_runs) as Runs,
            SUM(balls_faced) as Balls,
            SUM(out) as Outs,
            SUM(CASE WHEN score=0 THEN 1 ELSE 0 END) AS DotBalls,
            SUM(CASE WHEN batter_runs IN (4, 6) THEN 1 ELSE 0 END) AS BoundaryBalls
          FROM {database}.{table}
          WHERE {condition}
          GROUP BY bowler_type
        ),
        calculations AS (
          SELECT
            BowlingType,
            Runs,
            Balls,
            Outs,
            COALESCE(Runs / NULLIF(Outs, 0), 0) AS Average,
            COALESCE((Runs / NULLIF(Balls, 0)) * 100, 0) AS StrikeRate,
            COALESCE((DotBalls / NULLIF(Balls, 0)) * 100, 0) AS DotBallPercentage,
            COALESCE((BoundaryBalls / NULLIF(Balls, 0)) * 100, 0) AS BoundaryPercentage
          FROM stats
        )
        SELECT
          BowlingType,
          Runs,
          Balls,
          Outs,
          Average,
          StrikeRate,
          DotBallPercentage,
          BoundaryPercentage
        FROM calculations
        ORDER BY Runs DESC;
        """
    
    elif function_type == 'player_comp':
        if stats_type == 'batting':
            sql_query = f"""
            WITH stats AS (
              SELECT
                batter as Batsman,
                COUNT(DISTINCT match_no) as Innings,
                SUM(batter_runs) as Runs,
                SUM(balls_faced) as BallsFaced,
                SUM(out) as Outs,
                SUM(CASE WHEN score=0 THEN 1 ELSE 0 END) AS DotBallsFaced,
                SUM(CASE WHEN batter_runs IN (4, 6) THEN 1 ELSE 0 END) AS BoundaryBalls
              FROM {database}.{table}
              WHERE {condition}
              GROUP BY batter
            ),
            calculations AS (
              SELECT
                Batsman,
                Innings,
                Runs,
                BallsFaced,
                Outs,
                COALESCE(Runs / NULLIF(Outs, 0), 0) AS Average,
                COALESCE((Runs / NULLIF(BallsFaced, 0)) * 100, 0) AS StrikeRate,
                COALESCE((DotBallsFaced / NULLIF(BallsFaced, 0)) * 100, 0) AS DotBallPercentage,
                COALESCE((BoundaryBalls / NULLIF(BallsFaced, 0)) * 100, 0) AS BoundaryPercentage
              FROM stats
            )
            SELECT
              Batsman,
              Innings,
              Runs,
              BallsFaced,
              Outs,
              Average,  
              StrikeRate,
        DotBallPercentage,
        BoundaryPercentage
      FROM calculations
      ORDER BY Runs DESC;
      """
        elif stats_type == 'bowling':
            sql_query = f"""
            WITH stats AS (
              SELECT
                bowler as Bowler,
                COUNT(DISTINCT match_no) as Innings,
                SUM(out) as Wickets,
                SUM(bowler_runs) as RunsConceded,
                SUM(balls_faced) as BallsBowled,
                SUM(CASE WHEN score=0 THEN 1 ELSE 0 END) AS DotBallsBowled,
                SUM(CASE WHEN batter_runs IN (4, 6) THEN 1 ELSE 0 END) AS BoundaryBalls
              FROM {database}.{table}
              WHERE {condition}
              GROUP BY bowler
            ),
            calculations AS (
              SELECT
                Bowler,
                Innings,
                Wickets,
                RunsConceded,
                BallsBowled,
                COALESCE(RunsConceded / NULLIF(Wickets, 0), 0) AS Average,
                COALESCE((RunsConceded / NULLIF(BallsBowled, 0)) * 6, 0) AS EconomyRate,
                COALESCE((DotBallsBowled / NULLIF(BallsBowled, 0)) * 100, 0) AS DotBallPercentage,
                COALESCE((BoundaryBalls / NULLIF(BallsBowled, 0)) * 100, 0) AS BoundaryPercentage
              FROM stats
            )
            SELECT
              Bowler,
              Innings,
              Wickets,
              RunsConceded,
              BallsBowled,
              Average,
              EconomyRate,
              DotBallPercentage,
              BoundaryPercentage
            FROM calculations
            ORDER BY Wickets DESC;
            """


    return sql_query

# query=convert_to_sql_query(params)
# df = query_to_dataframe( query)
# # print(query)

def dropdown_values(column):
    query = f"""
    SELECT DISTINCT {column}
    FROM bbbdata.ballsnew
    """
    df = query_to_dataframe(query)
    values = df[column].tolist()

    # Save the list values to a .txt file
    file_path = os.path.join("vector_store_files", f"{column}.txt")

    with open(fr"C:\Users\adith\Documents\Projects\python-projects\cric_metric_clone\vector_store_files\{column}.txt", "w") as f:
        for value in values:
            f.write(f"{value}\n")
    if None in values:
        values.remove(None)

    return values
l=['venue', 'series_name',  'tournament_name',   'match_type',  'team_bat',  'team_bowl',  'batter',  'bowler', 'bowler_type', 
   'bowler_kind','batter_hand']

def load_dropdown_values(column):
    values = []
    cwd = os.getcwd()
    
    # Construct the absolute file path using os.path.join
    file_path = os.path.join(cwd, "dropdown_values", f"{column}.txt")
    # Load the list values from a .txt file
    with open(file_path, 'r', encoding='latin-1') as f:
        for line in f:
            values.append(line.strip())

    return values
# for lis in l:

#     df=dropdown_values(lis)

def calculate_stats(params):
    query = convert_to_sql_query(params)
    # df = query_to_dataframe(query)
    df=query_to_dataframe_mysql(query)
    return df
