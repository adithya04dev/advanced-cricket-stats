



import pandas as pd
def calculate_player_stats(df, params):
    df['Date'] = pd.to_datetime(df['Date'])

    player_name = params.get('player_name')
    stats_type = params.get('stats_type')
    match_type = params.get('match_type')
    group_by = params.get('group_by')
    adv = params.get('adv', False)
    date_from = params.get('date_from')
    date_to = params.get('date_to')
#adding series_name,tournament_name by extracting from param
    series_name = params.get('series_name')
    tournament_name = params.get('tournament_name') 
    player_team = params.get('player_team')
    opp_player_team = params.get('opp_player_team')
    opp_player_type = params.get('opp_player_type')
    venue = params.get('venue')
    overs_from = params.get('overs_from')
    overs_to = params.get('overs_to')
    from_date = pd.to_datetime(date_from)
    to_date = pd.to_datetime(date_to)
    # Rest of your function implementation
    if stats_type == 'batting':
            condition = (df['Batsman'] == player_name) & (df['MatchType'] == match_type) 
            if adv:
                condition &= (df['Date'] >= from_date)    & (df['SeriesName'].isin(series_name)) & (df['TournamentName'].isin(tournament_name)) & (df['Date'] <= to_date) & (df['BattingTeam'].isin(player_team)) & (df['BowlingTeam'].isin(opp_player_team)) & (df['Venue'].isin(venue)) & (df['Over_Number'] >= overs_from) & (df['Over_Number'] <= overs_to)  & (df['BowlingType'].isin(opp_player_type))
            df_player = df[condition]
    elif stats_type == 'bowling':
            condition = (df['Bowler'] == player_name) & (df['MatchType'] == match_type)
            if adv:
                condition &= (df['Date'] >= from_date)   & (df['SeriesName'].isin(series_name))  & (df['TournamentName'].isin(tournament_name)) & (df['Date'] <= to_date) & (df['BattingTeam'].isin(opp_player_team)) & (df['BowlingTeam'].isin(player_team)) & (df['Venue'].isin(venue)) & (df['Over_Number'] >= overs_from) & (df['Over_Number'] <= overs_to) & (df['BattingType'].isin(opp_player_type))
            df_player = df[condition]
   


    # Calculate the statistics
    if stats_type == 'batting':
        stats = df_player.groupby(group_by).agg(
            Innings=('Matchno', 'nunique'),
            Runs=('Batsman_Run', 'sum'),
            BallsFaced=('is_ball', 'sum'),
            Outs=('is_batter_out', 'sum'),
            DotBallsFaced=('is_dot', 'sum'),
            BoundaryBalls=('is_boundary', 'sum')
        )
        stats['Average'] = stats['Runs'] / stats['Outs']
        stats['StrikeRate'] = (stats['Runs'] / stats['BallsFaced']) * 100
        stats['DotBallPercentage'] = (stats['DotBallsFaced'] / stats['BallsFaced']) * 100
        stats['BoundaryPercentage'] = (stats['BoundaryBalls'] / stats['BallsFaced']) * 100
        stats.drop(columns=['BoundaryBalls','DotBallsFaced'], inplace=True)

    elif stats_type == 'bowling':
        stats = df_player.groupby(group_by).agg(
            Innings=('Matchno', 'nunique'),
            Wickets=('is_bowler_wicket', 'sum'),
            BallsBowled=('is_ball', 'sum'),
            RunsConceded=('TotalRuns', 'sum'),
            DotBallsBowled=('is_dot', 'sum'),
            BoundaryBalls=('is_boundary', 'sum')
        )
        stats['EconomyRate'] = (stats['RunsConceded'] / stats['BallsBowled']) * 6
        stats['BowlingAverage'] = stats['RunsConceded'] / stats['Wickets']
        stats['DotBallPercentage'] = (stats['DotBallsBowled'] / stats['BallsBowled']) * 100
        stats['BoundaryPercentage'] = (stats['BoundaryBalls'] / stats['BallsBowled']) * 100
        stats.drop(columns=['BoundaryBalls','DotBallsBowled'], inplace=True)

    return stats

def calculate_leaderboard_stats(df, params):  


    df['Date'] = pd.to_datetime(df['Date'])

    analysis_type = params.get('analysis_type')
    stats_type = params.get('stats_type')
    match_type = params.get('match_type')
    adv = params.get('adv', False)
    date_from = params.get('date_from')
    date_to = params.get('date_to')
    player_team = params.get('player_team')
    opp_player_team = params.get('opp_player_team')
    opp_player_type = params.get('opp_player_type')
#adding series_name,tournament_name by extracting from param
    series_name = params.get('series_name')
    tournament_name = params.get('tournament_name')
    venue = params.get('venue')
    overs_from = params.get('overs_from')
    overs_to = params.get('overs_to')
    from_date = pd.to_datetime(date_from)
    to_date = pd.to_datetime(date_to)
    # Rest of your function implementation
    if stats_type == 'batting':
            condition =  (df['MatchType'] == match_type)
            if adv:
                condition&= (df['Date'] >= from_date)  & (df['SeriesName'].isin(series_name)) & (df['TournamentName'].isin(tournament_name)) & (df['Date'] <= to_date) & (df['BattingTeam'].isin(player_team)) & (df['BowlingTeam'].isin(opp_player_team)) & (df['Venue'].isin(venue)) & (df['Over_Number'] >= overs_from) & (df['Over_Number'] <= overs_to)  & (df['BowlingType'].isin(opp_player_type))
            df_player = df[condition]
    elif stats_type == 'bowling':
            condition =  (df['MatchType'] == match_type)
            if adv:
                condition &= (df['Date'] >= from_date)  & (df['SeriesName'].isin(series_name)) & (df['TournamentName'].isin(tournament_name)) & (df['Date'] <= to_date) & (df['BattingTeam'].isin(opp_player_team)) & (df['BowlingTeam'].isin(player_team)) & (df['Venue'].isin(venue)) & (df['Over_Number'] >= overs_from) & (df['Over_Number'] <= overs_to) & (df['BattingType'].isin(opp_player_type))
            df_player = df[condition]



    # Calculate the statistics
    if analysis_type == 'player':
        if stats_type == 'batting':
            stats = df_player.groupby('Batsman').agg(
                Innings=('Matchno', 'nunique'),
                Runs=('Batsman_Run', 'sum'),
                BallsFaced=('is_ball', 'sum'),
                Outs=('is_batter_out', 'sum'),
                DotBallsFaced=('is_dot', 'sum'),
                BoundaryBalls=('is_boundary', 'sum')
            )
            stats['Average'] = stats['Runs'] / stats['Outs']
            stats['StrikeRate'] = (stats['Runs'] / stats['BallsFaced']) * 100
            stats['DotBallPercentage'] = (stats['DotBallsFaced'] / stats['BallsFaced']) * 100
            stats['BoundaryPercentage'] = (stats['BoundaryBalls'] / stats['BallsFaced']) * 100
            stats.drop(columns=['BoundaryBalls','DotBallsFaced'], inplace=True)
            #sort stats df based on runs
            stats = stats.sort_values(by='Runs', ascending=False)

        elif stats_type == 'bowling':
            stats = df_player.groupby('Bowler').agg(
                Innings=('Matchno', 'nunique'),
                Wickets=('is_bowler_wicket', 'sum'),
                BallsBowled=('is_ball', 'sum'),
                RunsConceded=('TotalRuns', 'sum'),
                DotBallsBowled=('is_dot', 'sum'),
                BoundaryBalls=('is_boundary', 'sum')
            )
            stats['EconomyRate'] = (stats['RunsConceded'] / stats['BallsBowled']) * 6
            stats['BowlingAverage'] = stats['RunsConceded'] / stats['Wickets']
            stats['DotBallPercentage'] = (stats['DotBallsBowled'] / stats['BallsBowled']) * 100
            stats['BoundaryPercentage'] = (stats['BoundaryBalls'] / stats['BallsBowled']) * 100
            stats.drop(columns=['BoundaryBalls','DotBallsBowled'], inplace=True)
            #sort stats df based on wickets
            stats = stats.sort_values(by='Wickets', ascending=False)


    elif analysis_type == 'team':
        if stats_type == 'batting':
            stats = df_player.groupby('BattingTeam').agg(
                Innings=('Matchno', 'nunique'),
                Runs=('Batsman_Run', 'sum'),
                BallsFaced=('is_ball', 'sum'),
                Outs=('is_batter_out', 'sum'),
                DotBallsFaced=('is_dot', 'sum'),
                BoundaryBalls=('is_boundary', 'sum')
            )
            stats['Average'] = stats['Runs'] / stats['Outs']
            stats['StrikeRate'] = (stats['Runs'] / stats['BallsFaced']) * 100
            stats['DotBallPercentage'] = (stats['DotBallsFaced'] / stats['BallsFaced']) * 100
            stats['BoundaryPercentage'] = (stats['BoundaryBalls'] / stats['BallsFaced']) * 100
            stats.drop(columns=['BoundaryBalls','DotBallsFaced'], inplace=True)
            #sort stats df based on runs
            stats = stats.sort_values(by='Runs', ascending=False)

        elif stats_type == 'bowling':
            stats = df_player.groupby('BowlingTeam').agg(
                Innings=('Matchno', 'nunique'),
                Wickets=('is_bowler_wicket', 'sum'),
                BallsBowled=('is_ball', 'sum'),
                RunsConceded=('TotalRuns', 'sum'),
                DotBallsBowled=('is_dot', 'sum'),
                BoundaryBalls=('is_boundary', 'sum')
            )
            stats['EconomyRate'] = (stats['RunsConceded'] / stats['BallsBowled']) * 6
            stats['BowlingAverage'] = stats['RunsConceded'] / stats['Wickets']
            stats['DotBallPercentage'] = (stats['DotBallsBowled'] / stats['BallsBowled']) * 100
            stats['BoundaryPercentage'] = (stats['BoundaryBalls'] / stats['BallsBowled']) * 100
            stats.drop(columns=['BoundaryBalls','DotBallsBowled'], inplace=True)
            #sort stats df based on wickets
            stats = stats.sort_values(by='Wickets', ascending=False)

    return stats

def calculate_matchup_stats(df, params):
    df['Date'] = pd.to_datetime(df['Date'])

    batter_name = params.get('batter_name')
    bowler_name = params.get('bowler_name')
    group_by = params.get('group_by')
    adv = params.get('adv', False)

    date_from = params.get('date_from')
    date_to = params.get('date_to')
#adding series_name,tournament_name by extracting from param
    series_name = params.get('series_name')
    tournament_name = params.get('tournament_name')
    venue = params.get('venue')
    overs_from = params.get('overs_from')
    overs_to = params.get('overs_to')
    from_date = pd.to_datetime(date_from)
    to_date = pd.to_datetime(date_to)
    # Rest of your function implementation
    condition = (df['Batsman'].isin(batter_name)) &  (df['Bowler'].isin(bowler_name)) 
    if adv:
        condition &= (df['Date'] >= from_date)    & (df['SeriesName'].isin(series_name)) & (df['TournamentName'].isin(tournament_name)) & (df['Date'] <= to_date) & (df['Venue'].isin(venue)) & (df['Over_Number'] >= overs_from) & (df['Over_Number'] <= overs_to)
    df_player = df[condition]



    # Calculate the statistics
    stats = df_player.groupby(group_by).agg(
        Innings=('Matchno', 'nunique'),
        Runs=('Batsman_Run', 'sum'),
        BallsFaced=('is_ball', 'sum'),
        Outs=('is_batter_out', 'sum'),
        DotBallsFaced=('is_dot', 'sum'),
        BoundaryBalls=('is_boundary', 'sum')
    )
    stats['Average'] = stats['Runs'] / stats['Outs']
    stats['StrikeRate'] = (stats['Runs'] / stats['BallsFaced']) * 100
    stats['DotBallPercentage'] = (stats['DotBallsFaced'] / stats['BallsFaced']) * 100
    stats['BoundaryPercentage'] = (stats['BoundaryBalls'] / stats['BallsFaced']) * 100
    stats.drop(columns=['BoundaryBalls','DotBallsFaced'], inplace=True)

   
    return stats

def calculate_player_comp_stats(df, params):
    df['Date'] = pd.to_datetime(df['Date'])

    player_name = params.get('player_name')
    stats_type = params.get('stats_type')
    match_type = params.get('match_type')
    adv = params.get('adv', False)
    date_from = params.get('date_from')
    date_to = params.get('date_to')
#adding series_name,tournament_name by extracting from param
    series_name = params.get('series_name')
    tournament_name = params.get('tournament_name')

    player_team = params.get('player_team')
    opp_player_team = params.get('opp_player_team')
    opp_player_type = params.get('opp_player_type')
    venue = params.get('venue')
    overs_from = params.get('overs_from')
    overs_to = params.get('overs_to')
    from_date = pd.to_datetime(date_from)
    to_date = pd.to_datetime(date_to)
    # Rest of your function implementation
    if stats_type == 'batting':
            condition = (df['Batsman'].isin(player_name)) & (df['MatchType'] == match_type) 
            if adv:
                condition &= (df['Date'] >= from_date)    & (df['SeriesName'].isin(series_name)) & (df['TournamentName'].isin(tournament_name)) & (df['Date'] <= to_date) & (df['BattingTeam'].isin(player_team)) & (df['BowlingTeam'].isin(opp_player_team)) & (df['Venue'].isin(venue)) & (df['Over_Number'] >= overs_from) & (df['Over_Number'] <= overs_to)  & (df['BowlingType'].isin(opp_player_type))
            df_player = df[condition]
    elif stats_type == 'bowling':
            condition =  (df['MatchType'] == match_type) & (df['Bowler'].isin(player_name))
            if adv:
                condition &= (df['Date'] >= from_date)   & (df['SeriesName'].isin(series_name))  & (df['TournamentName'].isin(tournament_name)) & (df['Date'] <= to_date) & (df['BattingTeam'].isin(opp_player_team)) & (df['BowlingTeam'].isin(player_team)) & (df['Venue'].isin(venue)) & (df['Over_Number'] >= overs_from) & (df['Over_Number'] <= overs_to) & (df['BattingType'].isin(opp_player_type))
            df_player = df[condition]
   


    # Calculate the statistics
    if stats_type == 'batting':
        stats = df_player.groupby('Batsman').agg(
            Innings=('Matchno', 'nunique'),
            Runs=('Batsman_Run', 'sum'),
            BallsFaced=('is_ball', 'sum'),
            Outs=('is_batter_out', 'sum'),
            DotBallsFaced=('is_dot', 'sum'),
            BoundaryBalls=('is_boundary', 'sum')
        )
        stats['Average'] = stats['Runs'] / stats['Outs']
        stats['StrikeRate'] = (stats['Runs'] / stats['BallsFaced']) * 100
        stats['DotBallPercentage'] = (stats['DotBallsFaced'] / stats['BallsFaced']) * 100
        stats['BoundaryPercentage'] = (stats['BoundaryBalls'] / stats['BallsFaced']) * 100
        stats.drop(columns=['BoundaryBalls','DotBallsFaced'], inplace=True)
        #sort stats df based on runs
        stats = stats.sort_values(by='Runs', ascending=False)

    elif stats_type == 'bowling':
        stats = df_player.groupby('Bowler').agg(
            Innings=('Matchno', 'nunique'),
            Wickets=('is_bowler_wicket', 'sum'),
            BallsBowled=('is_ball', 'sum'),
            RunsConceded=('TotalRuns', 'sum'),
            DotBallsBowled=('is_dot', 'sum'),
            BoundaryBalls=('is_boundary', 'sum')
        )
        stats['EconomyRate'] = (stats['RunsConceded'] / stats['BallsBowled']) * 6
        stats['BowlingAverage'] = stats['RunsConceded'] / stats['Wickets']
        stats['DotBallPercentage'] = (stats['DotBallsBowled'] / stats['BallsBowled']) * 100
        stats['BoundaryPercentage'] = (stats['BoundaryBalls'] / stats['BallsBowled']) * 100
        stats.drop(columns=['BoundaryBalls','DotBallsBowled'], inplace=True)
        #sort stats df based on wickets
        stats = stats.sort_values(by='Wickets', ascending=False)

    return stats


def calculate_venue_stats(df, params):
    df['Date'] = pd.to_datetime(df['Date'])

    venue = params.get('venue')
    match_type = params.get('match_type')
    adv = params.get('adv', False)
    date_from = params.get('date_from')
    date_to = params.get('date_to')
    #add series_name,tournament_name,overs_from,over_to
    series_name = params.get('series_name')
    tournament_name = params.get('tournament_name')
    overs_from = params.get('overs_from')
    overs_to = params.get('overs_to')


    from_date = pd.to_datetime(date_from)
    to_date = pd.to_datetime(date_to)
    # Rest of your function implementation
    condition = (df['Venue'].isin(venue)) & (df['MatchType'] == match_type)
    if adv:
        condition &= (df['Date'] >= from_date) & (df['SeriesName'].isin(series_name)) & (df['TournamentName'].isin(tournament_name)) & (df['Date'] <= to_date) & (df['Over_Number'] >= overs_from) & (df['Over_Number'] <= overs_to)
    df_player = df[condition]

    bt_stats = df_player.groupby('BowlingType').agg(
            Innings=('Matchno', 'nunique'),
            Wickets=('is_bowler_wicket', 'sum'),
            BallsBowled=('is_ball', 'sum'),
            RunsConceded=('TotalRuns', 'sum'),
            DotBallsBowled=('is_dot', 'sum'),
            BoundaryBalls=('is_boundary', 'sum')
        )
    bt_stats['EconomyRate'] = (bt_stats['RunsConceded'] / bt_stats['BallsBowled']) * 6
    bt_stats['BowlingAverage'] = bt_stats['RunsConceded'] / bt_stats['Wickets']


    in_stats = df_player.groupby("Inning_Number").agg(
    Innings=('Matchno', 'nunique'),
    Runs=('Batsman_Run', 'sum'),
    BallsFaced=('is_ball', 'sum'),
    Outs=('is_batter_out', 'sum'),
    DotBallsFaced=('is_dot', 'sum'),
    BoundaryBalls=('is_boundary', 'sum'),

)
    in_stats['Average_Score'] = in_stats['Runs'] / in_stats['Innings']
    in_stats['Runrate'] = in_stats['Runs'] / in_stats['BallsFaced']

    #return both dataframes
    return bt_stats,in_stats

    


