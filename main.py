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

SMALL_POINTS_MAP = {
    1: 13,
    2: 10,
    3: 8,
    4: 6,
    5: 5,
    6: 4,
    7: 3,
    8: 2,
    9: 1,
}

def calculate_total_points(group):
    total_points = sum(PLAYER_POINTS_MAP.get(place, 0) for place in group['rank'])
    return pd.Series({'total_points': total_points, 'team': group['name'].values[0]})

def calculate_total_points_sub(group):
    total_points = sum(SMALL_POINTS_MAP.get(place, 0) for place in group['place'])
    return pd.Series({'total_points': total_points, 'team': group['name'].values[0]})

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
full_players_results_df = full_players_results_df.merge(team_df, left_on='team_y', right_on='id')
full_teams_results_df = tournament_results_df.merge(team_df, left_on='team', right_on='id')

young_players_result = full_players_results_df[full_players_results_df['is_youngster']].loc[:, ['username', 'tournament', 'score', 'rank', 'name']]
woman_players_result = full_players_results_df[full_players_results_df['is_woman']].loc[:, ['username', 'tournament', 'score', 'rank', 'name']]

young_players_result['place'] = young_players_result.groupby('tournament')['rank'].rank(method='dense')
woman_players_result['place'] = woman_players_result.groupby('tournament')['rank'].rank(method='dense')


player_season_points = full_players_results_df.groupby('username').apply(calculate_total_points).sort_values('total_points', ascending=False).reset_index()
team_season_points = full_teams_results_df.groupby('name').apply(calculate_total_team_points).sort_values('total_points', ascending=False).reset_index()
young_players_points = young_players_result.groupby('username').apply(calculate_total_points_sub).sort_values('total_points', ascending=False).reset_index()
woman_players_points = woman_players_result.groupby('username').apply(calculate_total_points_sub).sort_values('total_points', ascending=False).reset_index()

player_season_points.index = player_season_points.index + 1
team_season_points.index = team_season_points.index + 1
young_players_points.index = young_players_points.index + 1
woman_players_points.index = woman_players_points.index + 1


st.sidebar.markdown("# Текущие рейтинги 🏆")

st.title('БНЛ Весна 2024')
st.title('Командный зачет 🏆')
st.markdown('''4 команд проходят в финал  
Призы:  
1 место - 1000 рублей  
2 место - 400 рублей  
''')
st.dataframe(team_season_points, width=1000)
st.title('Индивидуальный зачет 🥇')
st.markdown('''20 игроков проходят в финал  
Призы:   
1 место - 700 рублей  
2 место - 300 рублей  
3 место - 130 рублей  
4 место - 70 рублей  
''')
st.dataframe(player_season_points)
st.title('Юношеский зачет 🥇')
st.markdown('''16 игроков проходят в финал  
Призы:   
1 место - 300 рублей  
2 место - 150 рублей  
3 место - 100 рублей  
''')

st.dataframe(young_players_points, width=800)
st.title('Женский зачет 🥇')
st.markdown('''16 игроков проходят в финал  
Призы:   
1 место - 300 рублей  
2 место - 150 рублей  
3 место - 100 рублей  
''')
st.dataframe(woman_players_points, width=800)
