import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

start = pd.to_datetime('2024-11-24T17:00:00.000Z', format='ISO8601').tz_convert('US/Eastern')
end = pd.to_datetime('2024-12-01T17:00:00.000Z', format='ISO8601').tz_convert('US/Eastern')

teams = pd.read_csv('bph_site_team.csv', index_col='id', date_format='ISO8601')
teams.create_time = pd.to_datetime(teams.create_time, format='ISO8601').dt.tz_convert('US/Eastern')
hints = pd.read_csv('bph_site_hint.csv')
hints.response_time = pd.to_datetime(hints.response_time, format='ISO8601').dt.tz_convert('US/Eastern')
hints['requester'] = hints.team_id.map(teams.username)
hints['responder'] = hints.claimer.map(teams.username)
teams.index = teams.username

hints = hints[['requester', 'responder', 'response_time']]

fig = go.Figure()
fig.update_layout(
    title="Hint Progress over Time",
    xaxis_title="Time",
    yaxis_title="Hints",
    xaxis=dict(range=[start, end]),
    yaxis=dict(gridcolor="lightgray"),
    template="plotly_white"
)

for responder, hints in hints.sort_values('response_time').groupby('responder'):
    if teams.loc[responder, 'role'] == 'admin':
        hints = hints[(teams.loc[hints.requester, 'role'] != 'admin').values]
        hint_times = pd.concat(
            [pd.Series([hints.response_time.iloc[0]]), hints.response_time]
        )
        fig.add_trace(
            go.Scatter(
                x=hint_times,
                y=list(range(hints.shape[0] + 1)),
                mode="lines+markers",
                name=responder,
                # line_shape="hv"
            )
        )

fig.write_html("hints.html", include_plotlyjs='cdn')
fig.show()