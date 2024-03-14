import pandas as pd
import streamlit as st
import json

PLAYER_POINTS_MAP = {
    1: 25, 2: 22, 3: 20, 4: 18, 5: 17, 6: 16,
    7: 15, 8: 14, 9: 13, 10: 12, 11: 11, 12: 10,
    13: 9, 14: 8, 15: 7, 16: 6, 17: 5, 18: 4,
    19: 3, 20: 2
}

TEAM_POINTS_MAP = {
    1: 13,
    2: 10,
    3: 8,
    4: 6,
    5: 5,
    6: 4,
    7: 3,
    8: 2,
}

def calculate_total_points(group):
    total_points = sum(PLAYER_POINTS_MAP.get(place, 0) for place in group['rank'])
    return pd.Series({'total_points': total_points})

def calculate_total_team_points(group):
    total_points = sum(TEAM_POINTS_MAP.get(place, 0) for place in group['rank'])
    return pd.Series({'total_points': total_points})

def make_dict_from_raw_data(raw_data):
    result = []
    for row in raw_data:
        record = row['fields']
        record['id'] = row['pk']
        result.append(record)
    return result

tournament_info_raw = json.load(open('data/tournament.json'))
team_info_raw = json.load(open('data/team.json'))
player_info_raw = json.load(open('data/player.json'))
tournament_results_raw = json.load(open('data/TournamentTeamResult.json'))
player_results_raw = json.load(open('data/TournamentPlayerResult.json'))

tournament_info = make_dict_from_raw_data(tournament_info_raw)
team_info = make_dict_from_raw_data(team_info_raw)
player_info = make_dict_from_raw_data(player_info_raw)
tournament_results = make_dict_from_raw_data(tournament_results_raw)
player_results = make_dict_from_raw_data(player_results_raw)


tournament_df = pd.DataFrame(tournament_info)
team_df = pd.DataFrame(team_info)
player_df = pd.DataFrame(player_info)
tournament_results_df = pd.DataFrame(tournament_results)
player_results_df = pd.DataFrame(player_results)

full_players_results_df = player_results_df.merge(player_df, left_on='player', right_on='id')
full_teams_results_df = tournament_results_df.merge(team_df, left_on='team', right_on='id')

player_season_points = full_players_results_df.groupby('username').apply(calculate_total_points).sort_values('total_points', ascending=False).reset_index()
team_season_points = full_teams_results_df.groupby('name').apply(calculate_total_team_points).sort_values('total_points', ascending=False).reset_index()

st.title('Командный зачет 4 сезона')
st.dataframe(team_season_points, hide_index=True)
st.title('Индивидуальный зачет 4 сезона')
st.dataframe(player_season_points, hide_index=True)





