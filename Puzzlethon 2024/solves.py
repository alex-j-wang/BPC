import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

start = pd.to_datetime('2024-11-24T17:00:00.000Z', format='ISO8601').tz_convert('US/Eastern')
end = pd.to_datetime('2024-12-01T17:00:00.000Z', format='ISO8601').tz_convert('US/Eastern')

teams = pd.read_csv('bph_site_team.csv', index_col='id', date_format='ISO8601')
teams.create_time = pd.to_datetime(teams.create_time, format='ISO8601').dt.tz_convert('US/Eastern')
guesses = pd.read_csv('bph_site_guess.csv')
guesses.submit_time = pd.to_datetime(guesses.submit_time, format='ISO8601').dt.tz_convert('US/Eastern')
guesses['username'] = guesses.team_id.map(teams.username)
teams.index = teams.username

guesses = guesses.loc[guesses.is_correct & (guesses.submit_time < end), ['username', 'submit_time']]

fig = go.Figure()
fig.update_layout(
    title="Solve Progress over Time",
    xaxis_title="Time",
    yaxis_title="Solves",
    xaxis=dict(range=[start, end]),
    yaxis=dict(gridcolor="lightgray"),
    template="plotly_white"
)

for username, solves in guesses.sort_values('submit_time').groupby('username'):
    if teams.loc[username, 'role'] != 'admin':
        solve_times = pd.concat(
            [pd.Series([teams.loc[username, 'create_time']]), solves.submit_time]
        )
        fig.add_trace(
            go.Scatter(
                x=solve_times,
                y=list(range(solves.shape[0] + 1)),
                mode="lines",
                name=username,
                line_shape="hv"
            )
        )

fig.write_html("solve_progress.html", include_plotlyjs='cdn')
fig.show()