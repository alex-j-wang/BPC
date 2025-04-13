# TODO: reverse order so team creation info can be appended instead

import pandas as pd
import plotly.graph_objects as go

colors = ["#023EFF", "#FF7C00", "#1AC938", "#E8000B", "#8B2BE2", "#9F4800", "#F14CC1", "#A3A3A3", "#FFC400", "#00D7FF"]

start = pd.to_datetime('2025-04-12T17:30:00.000Z', format='ISO8601').tz_convert('US/Eastern')
end = pd.to_datetime('2025-04-13T23:00:00.000Z', format='ISO8601').tz_convert('US/Eastern')

teams = pd.read_csv('bph_site_team.csv', index_col='id', date_format='ISO8601')
teams.create_time = pd.to_datetime(teams.create_time, format='ISO8601').dt.tz_convert('US/Eastern')
solves = pd.read_csv('bph_site_solve.csv')
solves.solve_time = pd.to_datetime(solves.solve_time, format='ISO8601').dt.tz_convert('US/Eastern')

solves = solves[['puzzle_id', 'team_id', 'solve_time']]

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

for username, solves in solves.sort_values('solve_time').groupby('team_id'):
    if teams.loc[username, 'role'] == 'user':
        color = colors[idx % len(colors)]

        solve_times = [teams.loc[username, 'create_time']] + solves.solve_time.tolist()
        puzzles = ['start'] + solves.puzzle_id.tolist()

        marker_symbols = []
        marker_colors = []
        marker_sizes = []

        for puzzle in puzzles:
            if puzzle == "cutting-room-floor":
                marker_symbols.append("star")
                marker_colors.append("gold")
                marker_sizes.append(8)
            else:
                marker_symbols.append("circle")
                marker_colors.append(color)
                marker_sizes.append(5)

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
                marker=dict(
                    symbol=marker_symbols,
                    color=marker_colors,
                    line=dict(color=marker_colors),
                    size=marker_sizes,
                    opacity=1
                ),
                hoverinfo="text",
                text=[
                    f"<b>{solve_time.strftime('%m/%d %-I:%M %p')}<br>{username} • {puzzle}</b>"
                    for (solve_time, puzzle) in zip(solve_times, puzzles)
                ],
            )
        )
        idx += 1

fig.update_yaxes(range=[0, 60])
fig.write_html("solves.html", include_plotlyjs='cdn')
fig.show()