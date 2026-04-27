# GENERATES DATA TABLES
# TODO: admin statistics

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import itertools

data_folder = '2026-04-26'

# SETUP
in_person_start = pd.Timestamp('2026-04-11T17:00:00.000Z').tz_convert('US/Eastern')
in_person_end = pd.Timestamp('2026-04-12T23:00:00.000Z').tz_convert('US/Eastern')
remote_start = pd.Timestamp('2026-04-18T16:00:00.000Z').tz_convert('US/Eastern')
remote_end = pd.Timestamp('2026-04-24T16:30:00.000Z').tz_convert('US/Eastern')

# puzzle_id -> list of corresponding meta `puzzle_id`s
with open('meta_map.json', 'r') as f:
    meta_map = json.load(f)

meta_puzzles = set(itertools.chain.from_iterable(meta_map.values()))

# Data loading
unlocks = pd.read_csv(f'{data_folder}/hunt_site_unlock.csv')
answer_tokens = pd.read_csv(f'{data_folder}/hunt_site_answer_token.csv')
errata = pd.read_csv(f'{data_folder}/hunt_site_erratum.csv')
events = pd.read_csv(f'{data_folder}/hunt_site_event.csv')
feedback = pd.read_csv(f'{data_folder}/hunt_site_feedback.csv')
replies = pd.read_csv(f'{data_folder}/hunt_site_reply.csv')
guesses = pd.read_csv(f'{data_folder}/hunt_site_guess.csv')
hints = pd.read_csv(f'{data_folder}/hunt_site_hint.csv')
puzzles = pd.read_csv(f'{data_folder}/hunt_site_puzzle.csv')
solves = pd.read_csv(f'{data_folder}/hunt_site_solve.csv')
teams = pd.read_csv(f'{data_folder}/hunt_site_team.csv', index_col='id')
one_guard_no_doors = pd.read_csv(f'{data_folder}/hunt_site_one_guard_no_doors.csv')

# Timestamps
def convert_times(table):
    for col in table.columns:
        if 'time' in col.lower():
            try:
                table[col] = pd.to_datetime(table[col], format='ISO8601').dt.tz_convert('US/Eastern')
            except Exception as e:
                print(f"⚠️ Failed to convert column '{col}': {e}")
    return table

unlocks = convert_times(unlocks)
answer_tokens = convert_times(answer_tokens)
errata = convert_times(errata)
feedback = convert_times(feedback)
replies = convert_times(replies)
guesses = convert_times(guesses)
hints = convert_times(hints)
solves = convert_times(solves)
teams = convert_times(teams)

replies.rename(columns={'user_id': 'team_id'}, inplace=True)

# Filtering
unlocks = unlocks.loc[unlocks.team_id.map(teams.role) == 'user']
answer_tokens = answer_tokens.loc[answer_tokens.team_id.map(teams.role) == 'user']
feedback = feedback.loc[feedback.team_id.map(teams.role) == 'user']
replies = replies.loc[replies.team_id.map(teams.role) == 'user']
guesses = guesses.loc[guesses.team_id.map(teams.role) == 'user']
hints = hints.loc[hints.team_id.map(teams.role) == 'user']
solves = solves.loc[solves.team_id.map(teams.role) == 'user']
teams = teams.loc[teams.role == 'user']
one_guard_no_doors = one_guard_no_doors.loc[one_guard_no_doors.team_id.map(teams.role) == 'user']

# Modifications
hints.request = hints.request.fillna('')
replies['puzzle_id'] = replies.hint_id.map(hints.puzzle_id)
guesses['length'] = guesses.guess.map(len)
hints['length'] = hints.request.map(len)
teams['end_time'] = teams.interaction_type.map({
    'in-person': in_person_end,
    'remote': remote_end
})
teams['member_count'] = teams.members.map(lambda s: len(json.loads(s)))
teams['guess_count'] = guesses.groupby('team_id').size().reindex(teams.index, fill_value=0)
teams['hint_count'] = hints.groupby('team_id').size().reindex(teams.index, fill_value=0)
teams['total_hint_count'] = teams.hint_count + replies.groupby(replies.team_id).size().reindex(teams.index, fill_value=0)

# Remove entries after time cutoff
unlocks = unlocks[unlocks.unlock_time < unlocks.team_id.map(teams.end_time)]
answer_tokens = answer_tokens[answer_tokens.timestamp < answer_tokens.team_id.map(teams.end_time)]
guesses = guesses[guesses.submit_time < guesses.team_id.map(teams.end_time)]
solves = solves[solves.solve_time < solves.team_id.map(teams.end_time)]

# Finisher mask
finishers = teams.finish_time.notna() & (teams.finish_time < teams.end_time)

output = open('index.html', 'w')

# QUICK STATS
print('<!-- QUICK STATS -->', file=output)

quick_stats = pd.DataFrame(columns=['in-person', 'remote'])
quick_stats.loc['teams'] = teams.interaction_type.value_counts()
quick_stats.loc['finishers'] = teams[finishers].interaction_type.value_counts()
quick_stats.loc['meta solves'] = solves.loc[solves.puzzle_id.map(lambda pid: pid in meta_puzzles), 'team_id'].map(teams.interaction_type).value_counts()
quick_stats.loc['participants'] = teams.groupby(teams.interaction_type).member_count.sum()
quick_stats.loc['hints asked'] = hints.groupby(hints.team_id.map(teams.interaction_type)).size()
quick_stats.loc['guesses'] = guesses.groupby(guesses.team_id.map(teams.interaction_type)).size()
quick_stats.loc['solves'] = solves.groupby(solves.team_id.map(teams.interaction_type)).size()

quick_stats['total'] = quick_stats.sum(axis=1)
print(quick_stats.to_html(), file=output)

# TEAM STATS
print('<!-- TEAM STATS -->', file=output)

print('<!-- fewest guesses (finishers) -->', file=output)
print(
    teams.loc[finishers, ['display_name', 'guess_count']]
    .sort_values(by='guess_count').head(10).to_html(index=False), file=output)

print('<!-- most guesses (finishers) -->', file=output)
print(
    teams.loc[finishers, ['display_name', 'guess_count']]
    .sort_values(by='guess_count', ascending=False).head(10).to_html(index=False), file=output)

print('<!-- fewest hints (finishers) -->', file=output)
print(
    teams.loc[finishers, ['display_name', 'hint_count']]
    .sort_values(by='hint_count').head(40).to_html(index=False), file=output)

print('<!-- most hints (finishers) -->', file=output)
print(
    teams.loc[finishers, ['display_name', 'hint_count']]
    .sort_values(by='hint_count', ascending=False).head(10).to_html(index=False), file=output)

print('<!-- most hints + replies (finishers) -->', file=output)
print(
    teams.loc[finishers, ['display_name', 'total_hint_count']]
    .sort_values(by='total_hint_count', ascending=False).head(10).to_html(index=False), file=output)

# PUZZLE STATS
puzzle_stats = pd.DataFrame(index=puzzles.id, columns=['guesses', 'solves', 'backsolves', 'hints', 'hints + replies', 'tokens'])
puzzle_stats.guesses = guesses.puzzle_id.value_counts().reindex(puzzle_stats.index, fill_value=0)
puzzle_stats.solves = solves.puzzle_id.value_counts().reindex(puzzle_stats.index, fill_value=0)

# Backsolves
print('<!-- PUZZLE STATS -->', file=output)

solves['meta_ids'] = solves['puzzle_id'].map(meta_map)
solves_exploded = solves.explode('meta_ids')
merged = solves_exploded.merge(
    solves,
    left_on=['team_id', 'meta_ids'],
    right_on=['team_id', 'puzzle_id'],
    suffixes=('', '_meta')
)
filtered = merged[merged.solve_time_meta < merged.solve_time].drop_duplicates(subset=['team_id', 'puzzle_id'])
puzzle_stats.backsolves = filtered.puzzle_id.value_counts().reindex(puzzle_stats.index, fill_value=0)

puzzle_stats.hints = hints.puzzle_id.value_counts().reindex(puzzle_stats.index, fill_value=0)
puzzle_stats['hints + replies'] = puzzle_stats.hints + replies.puzzle_id.value_counts().reindex(puzzles.id, fill_value=0)
puzzle_stats.tokens = solves.loc[solves.type == 'answer_token', 'puzzle_id'].value_counts().reindex(puzzle_stats.index, fill_value=0)

print('<!-- primary stats -->', file=output)
print(puzzle_stats.reset_index().to_html(index=False), file=output)

other_stats = guesses[~guesses.is_correct].groupby(guesses.puzzle_id).guess.value_counts().reset_index(level=1)
other_stats = other_stats[~other_stats.index.duplicated(keep='first')]
other_stats.rename(columns={'guess': 'top_incorrect', 'count': 'relative_frequency'}, inplace=True)
other_stats.relative_frequency = other_stats.relative_frequency / puzzle_stats.solves * 100
other_stats.sort_values(by='relative_frequency', ascending=False, inplace=True)
other_stats.relative_frequency = other_stats.relative_frequency.round(1)

print('<!-- secondary stats -->', file=output)
print(other_stats.reset_index().to_html(index=False), file=output)

# MISCELLANEOUS STATS
print('<!-- MISCELLANEOUS STATS -->', file=output)

first_solves = (
    solves
    .sort_values(by='solve_time')
    .assign(interaction_type=solves.team_id.map(teams.interaction_type))
    .groupby('interaction_type')
    .head(10)
)
first_solves['display_name'] = first_solves.team_id.map(teams.display_name)
first_solves['solve_duration'] = (first_solves.solve_time - first_solves.interaction_type.map({
    'in-person': in_person_start,
    'remote-box': remote_start,
    'remote': remote_start,
})).apply(lambda td: (
    f'{int(td.total_seconds() // 60)}m {td.total_seconds() % 60:.3f}s'
))

print('<!-- first solves -->', file=output)
print(first_solves[['interaction_type', 'puzzle_id', 'display_name', 'solve_duration']].to_html(index=False), file=output)

print('<!-- longest guesses -->', file=output)
print(guesses.sort_values(by='length', ascending=False)[['guess', 'length']].head(10).to_html(index=False), file=output)
print('<!-- one-character guesses -->', file=output)
print(guesses.loc[guesses.length == 1, 'guess'].value_counts().to_frame().reset_index().to_html(index=False), file=output)

print('<!-- longest hints -->', file=output)
print(hints.sort_values(by='length', ascending=False)[['request', 'length']].head(1).to_html(index=False), file=output)
print('<!-- shortest hints -->', file=output)
print(hints.sort_values(by='length')[['request', 'length']].head(10).to_html(index=False), file=output)

# EVENT STATS
event_stats = pd.DataFrame(columns=['submitted', 'used'])
for event in answer_tokens.event_id.unique():
    event_stats.loc[event, 'submitted'] = (answer_tokens.event_id == event).sum()
    event_stats.loc[event, 'used'] = ((answer_tokens.event_id == event) & answer_tokens.puzzle_id).sum()

print('<!-- EVENT STATS -->', file=output)
print(event_stats.to_html(), file=output)

output.close()

# Plot guess accuracy
guesses.sort_values(by='submit_time', inplace=True)
accuracy = guesses.is_correct.cumsum() / (1 + np.arange(len(guesses)))

plt.plot(guesses.submit_time, accuracy)
plt.xticks(rotation=-45, ha='left', rotation_mode='anchor')
plt.xlabel('Time')
plt.ylabel('Cumulative Accuracy')
plt.title('Guess Accuracy Over Time')
plt.grid(True)
plt.tight_layout()
plt.savefig('accuracy.svg')
