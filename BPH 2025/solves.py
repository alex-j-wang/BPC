# TODO: reverse order so team creation info can be appended instead

import pandas as pd
import plotly.graph_objects as go

colors = ["#023EFF", "#FF7C00", "#1AC938", "#E8000B", "#8B2BE2", "#9F4800", "#F14CC1", "#A3A3A3", "#FFC400", "#00D7FF"]
metas = ["drop-the", "aha-erlebnis", "balloon-animals", "boring-plot", "six-degrees", "cutting-room-floor"]

start = pd.to_datetime('2025-04-12T17:30:00.000Z', format='ISO8601').tz_convert('US/Eastern')
end = pd.to_datetime('2025-04-13T23:00:00.000Z', format='ISO8601').tz_convert('US/Eastern')

teams = pd.read_csv('bph_site_team.csv', index_col='id', date_format='ISO8601')
teams.create_time = pd.to_datetime(teams.create_time, format='ISO8601').dt.tz_convert('US/Eastern')
solves = pd.read_csv('bph_site_solve.csv', index_col='puzzle_id')
solves.solve_time = pd.to_datetime(solves.solve_time, format='ISO8601').dt.tz_convert('US/Eastern')

fig = go.Figure()
fig.update_layout(
    title="Solve Progress over Time",
    xaxis_title="Time",
    yaxis_title="Solves",
    xaxis=dict(range=[start, end]),
    yaxis=dict(gridcolor="lightgray", range=[0, 60]),
    template="plotly_white",
    hoverlabel=dict(font=dict(family="Courier New, monospace", size=12)),
)

idx = 0

for username, solves in solves.sort_values('solve_time').groupby('team_id'):
    if teams.loc[username, 'role'] == 'user':
        meta_count = 0;
        color = colors[idx % len(colors)]

        solve_times = [teams.loc[username, 'create_time']] + solves.solve_time.tolist()
        puzzles = ['start'] + solves.index.tolist()

        marker_symbols = ["circle"]
        marker_colors = [color]
        stroke_colors = [color]
        marker_sizes = [5]

        for puzzle in puzzles[1:]:
            if puzzle in metas:
                meta_count += 1
            if puzzle in metas and meta_count == len(metas):
                marker_symbols.append("star")
                marker_colors.append("gold" if solves.loc[puzzle, 'type'] == 'guess' else 'white')
                stroke_colors.append("gold")
                marker_sizes.append(8)
            else:
                marker_symbols.append("circle")
                marker_colors.append(color if solves.loc[puzzle, 'type'] == 'guess' else 'white')
                stroke_colors.append(color)
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
                    line=dict(color=stroke_colors),
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

fig.write_html("solves.html", include_plotlyjs='cdn')
fig.show()