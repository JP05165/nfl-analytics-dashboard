import nfl_data_py as nfl
import pandas as pd

data = nfl.import_schedules([2024])

eagles = data[(data['home_team'] == 'PHI') |(data['away_team'] == 'PHI')]
eagles = eagles.copy()

eagles['eagles_score'] = eagles.apply(lambda row: row['home_score'] if row['home_team'] == 'PHI' else row['away_score'], axis=1)
eagles['opp_score'] = eagles.apply(lambda row: row['away_score'] if row['home_team'] == 'PHI' else row['home_score'], axis=1)
eagles['opponent'] = eagles.apply(lambda row: row['away_team'] if row['home_team'] == 'PHI' else row['home_team'], axis=1)
eagles['result'] = eagles.apply(lambda row: 'W' if row['eagles_score'] > row['opp_score'] else 'L', axis=1)

print(eagles[['week', 'opponent', 'eagles_score', 'opp_score', 'result']].to_string())
