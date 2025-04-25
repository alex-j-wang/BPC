import pandas as pd

# Load data (replace with actual file/database loading)
hints = pd.read_csv("bph_site_hint.csv")
follow_ups = pd.read_csv("bph_site_follow_up.csv")
guesses = pd.read_csv("bph_site_guess.csv")
solves = pd.read_csv("bph_site_solve.csv")
unlocks = pd.read_csv("bph_site_unlock.csv")
teams = pd.read_csv("bph_site_team.csv", index_col='id', date_format='ISO8601')

hints = hints.loc[hints['team_id'].map(teams.role) == 'user']
follow_ups = follow_ups.loc[follow_ups['user_id'].map(teams.role) == 'user']
guesses = guesses.loc[guesses['team_id'].map(teams.role) == 'user']
solves = solves.loc[solves['team_id'].map(teams.role) == 'user']
unlocks = unlocks.loc[unlocks['team_id'].map(teams.role) == 'user']

follow_ups['puzzle_id'] = follow_ups['hint_id'].map(hints.puzzle_id)
solves['solve_time'] = pd.to_datetime(solves['solve_time'], format='ISO8601').dt.tz_convert('US/Eastern')
unlocks['unlock_time'] = pd.to_datetime(unlocks['unlock_time'], format='ISO8601').dt.tz_convert('US/Eastern')

# Most hint requests
# hint_counts = hints['puzzle_id'].value_counts()
# follow_up_counts = follow_ups['puzzle_id'].value_counts()
# total_hint_requests = hint_counts.add(follow_up_counts, fill_value=0)
# most_hints = total_hint_requests.sort_values(ascending=False).head(1)
most_hints = hints['puzzle_id'].value_counts().head(1)

# Most guesses
most_guesses = guesses['puzzle_id'].value_counts().head(1)

# Most solves
most_solves = solves['puzzle_id'].value_counts().head(1)

# Fastest solve
merged = pd.merge(solves, unlocks, on=['team_id', 'puzzle_id'])
merged['duration'] = merged['solve_time'] - merged['unlock_time']
fastest_solves = merged[['puzzle_id', 'team_id', 'duration', 'type_x', 'type_y']].sort_values(by='duration', ascending=True).head(20)

# Display results
print("Most Hint Requests:", most_hints)
print("Most Guesses:", most_guesses)
print("Most Solves:", most_solves)
print("Fastest Solves:")
print(fastest_solves)