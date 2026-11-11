# NFL Analytics Dashboard

A web dashboard that pulls real NFL game data and shows any team's 2024 season at a glance: score for every game, win/loss record, and home vs. away performance.

I decided to build an NFL Analytics Dashboard because I wanted to experience how data is converted from documents into charts using tools in Python. I learned a lot of data visualization from this project and how to tweak certain functions in order to produce the graphs that you like. 

## How it works

- **Data:** game schedules and scores come from [`nfl_data_py`](https://github.com/nflverse/nfl_data_py).
- **Backend (`app.py`):** a Flask app. `get_team_data(team)` filters the season to one team's games. Each row only has a home score and an away score, so a row-wise pandas `apply` works out which score belongs to the selected team, who the opponent was, and whether it was a win or a loss.
- **API:**
  - `GET /api/scores/<team>`: week, opponent, scores, and result for every game
  - `GET /api/home_away/<team>`: wins, losses, and average points scored and allowed, split by home and away
- **Frontend (`Teams.html`, `Team.js`):** a 32-team picker. Selecting a team loads its charts with Chart.js.
- **`test.py` and `dashboard.html`:** the original Eagles-only prototype, kept for history. `dashboard.html` calls the old `/api/scores` endpoints, which no longer exist, so it won't load data in the current version.

Team codes are the standard abbreviations, for example `PHI`, `DAL`, `KC`.

## How to run

Requires Python 3 and an internet connection (the game data is downloaded on each request).

```bash
git clone https://github.com/JP05165/nfl-analytics-dashboard.git
cd nfl-analytics-dashboard
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

Then open **http://127.0.0.1:5002** and pick a team.

You can also call the API directly: http://127.0.0.1:5002/api/scores/PHI

## Tech

Python · Flask · pandas · nfl_data_py · JavaScript · Chart.js
