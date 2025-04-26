# GENERATES SOLVE GRAPHS BY INTERACTION TYPE
# TODO: reverse order so team creation info can be appended instead

import pandas as pd
import plotly.graph_objects as go

colors = ['#023EFF', '#FF7C00', '#1AC938', '#E8000B', '#8B2BE2', '#9F4800', '#F14CC1', '#A3A3A3', '#FFC400', '#00D7FF']

data_folder = '2025-04-25'

in_person_start = pd.Timestamp('2025-04-12T17:30:00.000Z').tz_convert('US/Eastern')
in_person_end = pd.Timestamp('2025-04-13T23:00:00.000Z').tz_convert('US/Eastern')
remote_start = pd.Timestamp('2025-04-19T16:00:00.000Z').tz_convert('US/Eastern')
remote_end = pd.Timestamp('2025-04-25T16:00:00.000Z').tz_convert('US/Eastern')

metas = ['drop-the', 'aha-erlebnis', 'balloon-animals', 'boring-plot', 'six-degrees', 'cutting-room-floor']

solves = pd.read_csv(f'{data_folder}/bph_site_solve.csv', index_col='puzzle_id')
teams = pd.read_csv(f'{data_folder}/bph_site_team.csv', index_col='id')

solves.solve_time = pd.to_datetime(solves.solve_time, format='ISO8601').dt.tz_convert('US/Eastern')
teams.create_time = pd.to_datetime(teams.create_time, format='ISO8601').dt.tz_convert('US/Eastern')

solves = solves.loc[solves.team_id.map(teams.role) == 'user']
teams = teams.loc[teams.role == 'user']
teams.loc[(teams.interaction_type == 'remote') & teams.has_box, 'interaction_type'] = 'remote-box'

for interaction_type in ['in-person', 'remote-box', 'remote']:
    start = in_person_start if interaction_type == 'in-person' else remote_start
    end = in_person_end if interaction_type == 'in-person' else remote_end

    fig = go.Figure()
    fig.update_layout(
        title=f"Solve Progress over Time ({interaction_type.replace('-', ' ').capitalize()})",
        xaxis_title='Time',
        yaxis_title='Solves',
        xaxis=dict(range=[start, end]),
        yaxis=dict(gridcolor='lightgray', range=[0, 60]),
        template='plotly_white',
        hoverlabel=dict(font=dict(family='Courier New, monospace', size=12)),
    )

    idx = 0
    filtered = solves[solves.team_id.map(teams.interaction_type) == interaction_type]

    for username, team_solves in filtered.sort_values('solve_time').groupby('team_id'):
        meta_count = 0;
        color = colors[idx % len(colors)]

        solve_times = [teams.loc[username, 'create_time']] + team_solves.solve_time.tolist()
        puzzles = ['start'] + team_solves.index.tolist()

        marker_symbols = ['circle']
        marker_colors = [color]
        stroke_colors = [color]
        marker_sizes = [5]

        for puzzle in puzzles[1:]:
            if puzzle in metas:
                meta_count += 1
            if puzzle in metas and meta_count == len(metas):
                marker_symbols.append('star')
                marker_colors.append('gold' if team_solves.loc[puzzle, 'type'] == 'guess' else 'white')
                stroke_colors.append('gold')
                marker_sizes.append(8)
            else:
                marker_symbols.append('circle')
                marker_colors.append(color if team_solves.loc[puzzle, 'type'] == 'guess' else 'white')
                stroke_colors.append(color)
                marker_sizes.append(5)

        fig.add_trace(
            go.Scatter(
                x=solve_times,
                y=list(range(team_solves.shape[0] + 1)),
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
                hoverinfo='text',
                text=[
                    f"<b>{solve_time.strftime('%m/%d %-I:%M %p')}<br>{username} • {puzzle}</b>"
                    for (solve_time, puzzle) in zip(solve_times, puzzles)
                ],
            )
        )
        idx += 1

    fig.write_html(f'{interaction_type}-solves.html', include_plotlyjs='cdn')
