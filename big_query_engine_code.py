import os


import pandas as pd
from google.cloud import bigquery
import os
import base64
import json
import google.auth
from google.oauth2 import service_account
from google.cloud import bigquery

# Load the credentials from the environment variable
credentials_b64 = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
credentials_bytes = base64.b64decode(credentials_b64)
credentials_dict = json.loads(credentials_bytes)

# Create a Credentials object from the loaded dictionary
credentials = service_account.Credentials.from_service_account_info(credentials_dict)


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
    for key in ['batter_name','bowler_name','inninggs_number','venue','batter_team', 'bowler_team', 'series_name', 'tournament_name',  'batter_type','bowler_type']:
        if key in params and isinstance(params[key], list):
            params[key] = tuple(params[key])
            # print("hello")

    # Build the SQL query
    database ='bbbdata'
    table = 'ballsnew'

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
        condition+= f"MatchType = '{match_type}'"

    if date_from is not None :
        condition += f" AND Date >= '{date_from}'"
    if date_to is not None:
        condition += f" AND Date <= '{date_to}'"
    if series_name is not None:
        condition += f" AND SeriesName IN {series_name}"
    if tournament_name is not None:
        condition += f" AND TournamentName IN {tournament_name}"
    if venue is not None:
        condition += f" AND Venue IN {venue}"
    if overs_from is not None and overs_to is not None:
        condition += f" AND Over_Number BETWEEN {overs_from} AND {overs_to}"
    if batter_name is not None:
        condition += f" AND Batsman IN {batter_name}"
    if bowler_name is not None:
        condition += f" AND Bowler IN {bowler_name}"
    if batter_team is not None:
        condition += f" AND BattingTeam IN {batter_team}"
    if bowler_team  is not None:
        condition += f" AND BowlingTeam IN {bowler_team}"
    if batter_type is not None:
        condition += f" AND BowlingType IN {batter_type}"
    if bowler_type is not None:
        condition += f" AND BowlingType IN {bowler_type}"
    if venue is not None:
        condition += f" AND Venue IN {venue}"
    if inninggs_number is not None:
        condition += f" AND InningsNumber IN {inninggs_number}"
    condition=condition.replace(',)',')')
    if match_type ==None:
        condition =condition.replace('AND',' ',1)


    if function_type=='leaderboard':
        if analysis_type == 'player':
            if stats_type == 'batting':
                sql_query = f"""
                WITH stats AS (
                SELECT
                    Batsman,
                    COUNT(DISTINCT Matchno) AS Innings,
                    SUM(Batsman_Run) AS Runs,
                    SUM(is_ball_int) AS BallsFaced,
                    SUM(is_batter_out) AS Outs,
                    SUM(is_dot) AS DotBallsFaced,
                    SUM(is_boundary) AS BoundaryBalls
                FROM {database}.{table}
                WHERE {condition}
                GROUP BY Batsman
                ),
                calculations AS (
                SELECT
                    Batsman,
                    Innings,
                    Runs,
                    BallsFaced,
                    Outs,
                    Runs / NULLIF(Outs, 0) AS Average,
                    (Runs / BallsFaced) * 100 AS StrikeRate,
                    (DotBallsFaced / BallsFaced) * 100 AS DotBallPercentage,
                    (BoundaryBalls / BallsFaced) * 100 AS BoundaryPercentage
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
                    Bowler,
                    COUNT(DISTINCT Matchno) AS Innings,
                    SUM(is_bowler_wicket) AS Wickets,
                    SUM(TotalRuns) AS RunsConceded,
                    SUM(is_ball_int) AS BallsBowled,
                    SUM(is_dot) AS DotBallsBowled,
                    SUM(is_boundary) AS BoundaryBalls
                FROM {database}.{table}
                WHERE {condition}
                GROUP BY Bowler
                ),
                calculations AS (
                SELECT
                    Bowler,
                    Innings,
                    Wickets,
                    RunsConceded,
                    BallsBowled,
                    Wickets / NULLIF(Innings, 0) AS Average,
                    (RunsConceded / BallsBowled) * 6 AS EconomyRate,
                    (DotBallsBowled / BallsBowled) * 100 AS DotBallPercentage,
                    (BoundaryBalls / BallsBowled) * 100 AS BoundaryPercentage
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
                    BattingTeam,
                    COUNT(DISTINCT Matchno) AS Innings,
                    SUM(Batsman_Run) AS Runs,
                    SUM(is_ball_int) AS BallsFaced,
                    SUM(is_batter_out) AS Outs,
                    SUM(is_dot) AS DotBallsFaced,
                    SUM(is_boundary) AS BoundaryBalls
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
                    Runs / NULLIF(Outs, 0) AS Average,
                    (Runs / BallsFaced) * 100 AS StrikeRate,
                    (DotBallsFaced / BallsFaced) * 100 AS DotBallPercentage,
                    (BoundaryBalls / BallsFaced) * 100 AS BoundaryPercentage
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
                    BowlingTeam,
                    COUNT(DISTINCT Matchno) AS Innings,
                    SUM(is_bowler_wicket) AS Wickets,
                    SUM(TotalRuns) AS RunsConceded,
                    SUM(is_ball_int) AS BallsBowled,
                    SUM(is_dot) AS DotBallsBowled,
                    SUM(is_boundary) AS BoundaryBalls
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
                    Wickets / NULLIF(Innings, 0) AS Average,
                    (RunsConceded / BallsBowled) * 6 AS EconomyRate,
                    (DotBallsBowled / BallsBowled) * 100 AS DotBallPercentage,
                    (BoundaryBalls / BallsBowled) * 100 AS BoundaryPercentage
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

    elif function_type=='player_search':
        if stats_type == 'batting':
            sql_query = f"""
            WITH stats AS (
                SELECT  COUNT(DISTINCT Matchno) as Innings, SUM(Batsman_Run) as Runs, SUM(is_ball_int) as BallsFaced, SUM(is_batter_out) as Outs, SUM(is_dot) as DotBallsFaced, SUM(is_boundary) as BoundaryBalls
                FROM {database}.{table}
                WHERE {condition}
                GROUP BY {group_by}
            ),
            calculations AS (
                SELECT Innings, Runs, BallsFaced, Outs, Runs / NULLIF(Outs, 0) AS Average, (Runs / BallsFaced) * 100 AS StrikeRate, (DotBallsFaced / BallsFaced) * 100 AS DotBallPercentage, (BoundaryBalls / BallsFaced) * 100 AS BoundaryPercentage
                FROM stats
            )
            SELECT  Innings, Runs, BallsFaced, Outs, Average, StrikeRate, DotBallPercentage, BoundaryPercentage
            FROM calculations
            ORDER BY Runs DESC;
            """
        elif stats_type == 'bowling':
            sql_query = f"""
            WITH stats AS (
                SELECT Bowler, COUNT(DISTINCT Matchno) as Innings, SUM(is_bowler_wicket) as Wickets, SUM(TotalRuns) as RunsConceded, SUM(is_ball_int) as BallsBowled, SUM(is_dot) as DotBallsBowled, SUM(is_boundary) as BoundaryBalls
                FROM {database}.{table}
                WHERE {condition}
                GROUP BY {group_by}
            ),
            calculations AS (
                SELECT Bowler, Innings, Wickets, RunsConceded, BallsBowled, Wickets / NULLIF(Innings, 0) AS Average, (RunsConceded / BallsBowled) * 6 AS EconomyRate, (DotBallsBowled / BallsBowled) * 100 AS DotBallPercentage, (BoundaryBalls / BallsBowled) * 100 AS BoundaryPercentage
                FROM stats
            )
            SELECT Bowler, Innings, Wickets, RunsConceded, BallsBowled, Average, EconomyRate, DotBallPercentage, BoundaryPercentage
            FROM calculations
            ORDER BY Wickets DESC;
            """

    elif function_type=='matchup':
        sql_query = f"""
        WITH stats AS (
        SELECT {group_by},
            
            COUNT(DISTINCT Matchno) as Innings,
            SUM(Batsman_Run) as Runs,
            SUM(is_ball_int) as BallsFaced,
            SUM(is_batter_out) as Outs,
            SUM(is_dot) as DotBallsFaced,
            SUM(is_boundary) as BoundaryBalls
        FROM {database}.{table}
        WHERE {condition}
        GROUP BY {group_by}
        ),
        calculations AS (
        SELECT  {group_by},
            Innings,
            Runs,
            BallsFaced,
            Outs,
            Runs / NULLIF(Outs, 0) AS Average,
            (Runs / BallsFaced) * 100 AS StrikeRate,
            (DotBallsFaced / BallsFaced) * 100 AS DotBallPercentage,
            (BoundaryBalls / BallsFaced) * 100 AS BoundaryPercentage
        FROM stats
        )
        SELECT  {group_by},
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

    elif function_type=='venue_search':
        sql_query = f"""
        WITH stats AS (
          SELECT
            BowlingType,
            SUM(Batsman_Run) as Runs,
            SUM(is_ball_int) as Balls,
            SUM(is_batter_out) as Outs,
            SUM(is_dot) as DotBalls,
            SUM(is_boundary) as BoundaryBalls
          FROM {database}.{table}
          WHERE {condition}
          GROUP BY BowlingType
        ),
        calculations AS (
          SELECT
            BowlingType,
            Runs,
            Balls,
            Outs,
            Runs / NULLIF(Outs, 0) AS Average,
            (Runs / Balls) * 100 AS StrikeRate,
            (DotBalls / Balls) * 100 AS DotBallPercentage,
            (BoundaryBalls / Balls) * 100 AS BoundaryPercentage
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

    elif function_type=='player_comp':
        if stats_type == 'batting':
            sql_query = f"""
            WITH stats AS (
              SELECT
                Batsman,
                COUNT(DISTINCT Matchno) as Innings,
                SUM(Batsman_Run) as Runs,
                SUM(is_ball_int) as BallsFaced,
                SUM(is_batter_out) as Outs,
                SUM(is_dot) as DotBallsFaced,
                SUM(is_boundary) as BoundaryBalls
              FROM {database}.{table}
              WHERE {condition}
              GROUP BY Batsman
            ),
            calculations AS (
              SELECT
                Batsman,
                Innings,
                Runs,
                BallsFaced,
                Outs,
                Runs / NULLIF(Outs, 0) AS Average,
                (Runs / BallsFaced) * 100 AS StrikeRate,
                (DotBallsFaced / BallsFaced) * 100 AS DotBallPercentage,
                (BoundaryBalls / BallsFaced) * 100 AS BoundaryPercentage
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
                Bowler,
                COUNT(DISTINCT Matchno) as Innings,
                SUM(is_bowler_wicket) as Wickets,
                SUM(TotalRuns) as RunsConceded,
                SUM(is_ball_int) as BallsBowled,
                SUM(is_dot) as DotBallsBowled,
                SUM(is_boundary) as BoundaryBalls
              FROM {database}.{table}
              WHERE {condition}
              GROUP BY Bowler
            ),
            calculations AS (
              SELECT
                Bowler,
                Innings,
                Wickets,
                RunsConceded,
                BallsBowled,
                Wickets / NULLIF(Innings, 0) AS Average,
                (RunsConceded / BallsBowled) * 6 AS EconomyRate,
                (DotBallsBowled / BallsBowled) * 100 AS DotBallPercentage,
                (BoundaryBalls / BallsBowled) * 100 AS BoundaryPercentage
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

query=convert_to_sql_query(params)
df = query_to_dataframe( query)
# print(query)

def dropdown_values(column):
    query = f"""
    SELECT DISTINCT {column}
    FROM bbbdata.ballsnew
    """
    df = query_to_dataframe(query)
    values = df[column].tolist()

    # Save the list values to a .txt file
    with open(f"{column}.txt", "w") as f:
        for value in values:
            f.write(f"{value}\n")
    if None in values:
        values.remove(None)

    return values


def load_dropdown_values(column):
    values = []

    # Load the list values from a .txt file
    with open(f"{column}.txt", "r") as f:
        for line in f:
            values.append(line.strip())

    return values

def calculate_stats(params):
    query = convert_to_sql_query(params)
    df = query_to_dataframe(query)
    return df
