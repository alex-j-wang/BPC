# TODO: reverse order so team creation info can be appended instead

import pandas as pd
import plotly.graph_objects as go

colors = ["#023EFF", "#FF7C00", "#1AC938", "#E8000B", "#8B2BE2", "#9F4800", "#F14CC1", "#A3A3A3", "#FFC400", "#00D7FF"]

start = pd.to_datetime('2024-11-24T17:00:00.000Z', format='ISO8601').tz_convert('US/Eastern')
end = pd.to_datetime('2024-12-01T17:00:00.000Z', format='ISO8601').tz_convert('US/Eastern')

teams = pd.read_csv('bph_site_team.csv', index_col='id', date_format='ISO8601')
teams.create_time = pd.to_datetime(teams.create_time, format='ISO8601').dt.tz_convert('US/Eastern')
guesses = pd.read_csv('bph_site_guess.csv')
guesses.submit_time = pd.to_datetime(guesses.submit_time, format='ISO8601').dt.tz_convert('US/Eastern')
guesses['username'] = guesses.team_id.map(teams.username)
teams.index = teams.username

guesses = guesses.loc[guesses.is_correct, ['puzzle_id', 'username', 'submit_time']]

fig = go.Figure()
fig.update_layout(
    title="Solve Progress over Time",
    xaxis_title="Time",
    yaxis_title="Solves",
    xaxis=dict(range=[start, end]),
    yaxis=dict(gridcolor="lightgray"),
    template="plotly_white",
    hoverlabel=dict(font=dict(family="Courier New, monospace", size=12)),
)

idx = 0

for username, solves in guesses.sort_values('submit_time').groupby('username'):
    if teams.loc[username, 'role'] != 'admin':
        color = colors[idx % len(colors)]
        solve_times = [teams.loc[username, 'create_time']] + solves.submit_time.tolist()
        puzzles = ['start'] + solves.puzzle_id.tolist()
        fig.add_trace(
            go.Scatter(
                x=solve_times,
                y=list(range(solves.shape[0] + 1)),
                mode='lines+markers',
                name=username,
                line=dict(color=color),
                hoverlabel=dict(
                    bgcolor='white',
                    font=dict(color=color),
                    bordercolor=color,
                ),
                hoverinfo="text",
                text=[
                    f"<b>{solve_time.strftime('%m/%d %-I:%M %p')}<br>{username} • {puzzle}</b>"
                    for (solve_time, puzzle) in zip(solve_times, puzzles)
                ],
            )
        )
        idx += 1

fig.write_html("solves.html", include_plotlyjs='cdn')
fig.show()