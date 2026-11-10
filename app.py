from flask import Flask, jsonify, send_file, send_from_directory
import nfl_data_py as nfl
import pandas as pd

app = Flask(__name__)

def get_team_data(team):
    data = nfl.import_schedules([2024])
    team_games = data[(data['home_team'] == team) | (data['away_team'] == team)].copy()

    team_games['team_score'] = team_games.apply(lambda row: row['home_score'] if row['home_team'] == team else row['away_score'], axis=1)
    team_games['opp_score'] = team_games.apply(lambda row: row['away_score'] if row['home_team'] == team else row['home_score'], axis=1)
    team_games['opponent'] = team_games.apply(lambda row: row['away_team'] if row['home_team'] == team else row['home_team'], axis=1)
    team_games['result'] = team_games.apply(lambda row: 'W' if row['team_score'] > row['opp_score'] else 'L', axis=1)
    return team_games


@app.route('/api/scores/<team>')
def scores(team):
    games = get_team_data(team)
    return jsonify(games[['week', 'opponent', 'team_score', 'opp_score', 'result']].to_dict('records'))

@app.route('/api/home_away/<team>')
def home_away(team):
    team_games = get_team_data(team)
    team_games['location'] = team_games.apply(lambda row: 'Home' if row['home_team'] == team else 'Away', axis=1)
    home_games = team_games[team_games['location'] == 'Home']
    away_games = team_games[team_games['location'] == 'Away']

    return jsonify({
        'home': {
            'wins': int(home_games[home_games['result'] == 'W'].shape[0]),
            'losses': int(home_games[home_games['result'] == 'L'].shape[0]),
            'avg_scored': round(float(home_games['team_score'].mean()),1),
            'avg_allowed': round(float(home_games['opp_score'].mean()),1)
        }, 
        'away': {
            'wins': int (away_games[away_games['result'] == 'W'].shape[0]),
            'losses': int(away_games[away_games['result'] == 'L'].shape[0]),
            'avg_scored': round(float(away_games['team_score'].mean()),1),
            'avg_allowed': round(float(away_games['opp_score'].mean()),1)
        }
    })
@app.route('/')
def index():
    return send_file('Teams.html')

@app.route('/Team.js')
def serve_js():

    return send_from_directory('.', 'Team.js');

if __name__ == '__main__':
    app.run(debug=True, port=5002)