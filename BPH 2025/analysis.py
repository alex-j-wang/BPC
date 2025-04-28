# GENERATES DATA TABLES
# TODO: admin statistics

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

data_folder = '2025-04-25'

# SETUP
in_person_start = pd.Timestamp('2025-04-12T17:30:00.000Z').tz_convert('US/Eastern')
in_person_end = pd.Timestamp('2025-04-13T23:00:00.000Z').tz_convert('US/Eastern')
remote_start = pd.Timestamp('2025-04-19T16:00:00.000Z').tz_convert('US/Eastern')
remote_end = pd.Timestamp('2025-04-25T16:00:00.000Z').tz_convert('US/Eastern')

# puzzle_id -> list of corresponding meta `puzzle_id`s
with open('meta_map.json', 'r') as f:
    meta_map = json.load(f)

# Data loading
unlocks = pd.read_csv(f'{data_folder}/bph_site_unlock.csv')
answer_tokens = pd.read_csv(f'{data_folder}/bph_site_answer_token.csv')
errata = pd.read_csv(f'{data_folder}/bph_site_erratum.csv')
events = pd.read_csv(f'{data_folder}/bph_site_event.csv')
feedback = pd.read_csv(f'{data_folder}/bph_site_feedback.csv')
follow_ups = pd.read_csv(f'{data_folder}/bph_site_follow_up.csv')
guesses = pd.read_csv(f'{data_folder}/bph_site_guess.csv')
hints = pd.read_csv(f'{data_folder}/bph_site_hint.csv')
m_guards_n_doors_k_choices = pd.read_csv(f'{data_folder}/bph_site_m_guards_n_doors_k_choices.csv')
puzzles = pd.read_csv(f'{data_folder}/bph_site_puzzle.csv')
solves = pd.read_csv(f'{data_folder}/bph_site_solve.csv')
teams = pd.read_csv(f'{data_folder}/bph_site_team.csv', index_col='id')
two_guards_two_doors = pd.read_csv(f'{data_folder}/bph_site_two_guards_two_doors.csv')

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
follow_ups = convert_times(follow_ups)
guesses = convert_times(guesses)
hints = convert_times(hints)
m_guards_n_doors_k_choices = convert_times(m_guards_n_doors_k_choices)
solves = convert_times(solves)
teams = convert_times(teams)
two_guards_two_doors = convert_times(two_guards_two_doors)

follow_ups.rename(columns={'user_id': 'team_id'}, inplace=True)

# Filtering
unlocks = unlocks.loc[unlocks.team_id.map(teams.role) == 'user']
answer_tokens = answer_tokens.loc[answer_tokens.team_id.map(teams.role) == 'user']
feedback = feedback.loc[feedback.team_id.map(teams.role) == 'user']
follow_ups = follow_ups.loc[follow_ups.team_id.map(teams.role) == 'user']
guesses = guesses.loc[guesses.team_id.map(teams.role) == 'user']
hints = hints.loc[hints.team_id.map(teams.role) == 'user']
m_guards_n_doors_k_choices = m_guards_n_doors_k_choices.loc[m_guards_n_doors_k_choices.team_id.map(teams.role) == 'user']
solves = solves.loc[solves.team_id.map(teams.role) == 'user']
teams = teams.loc[teams.role == 'user']
two_guards_two_doors = two_guards_two_doors.loc[two_guards_two_doors.team_id.map(teams.role) == 'user']

# Modifications
hints.request = hints.request.fillna('')
follow_ups['puzzle_id'] = follow_ups.hint_id.map(hints.puzzle_id)
guesses['length'] = guesses.guess.map(len)
hints['length'] = hints.request.map(len)
teams['end_time'] = teams.interaction_type.map({
    'in-person': in_person_end,
    'remote': remote_end
})
teams['member_count'] = teams.members.map(lambda s: len(json.loads(s)))
teams['guess_count'] = guesses.groupby(guesses.team_id).size().reindex(teams.index, fill_value=0)
teams['hint_count'] = hints.groupby(hints.team_id).size().reindex(teams.index, fill_value=0)
teams['total_hint_count'] = teams.hint_count + follow_ups.groupby(follow_ups.team_id).size().reindex(teams.index, fill_value=0)
teams.loc[(teams.interaction_type == 'remote') & teams.has_box, 'interaction_type'] = 'remote-box'

# Remove entries after time cutoff
unlocks = unlocks.loc[unlocks.unlock_time < unlocks.team_id.map(teams.end_time)]
answer_tokens = answer_tokens.loc[answer_tokens.timestamp < answer_tokens.team_id.map(teams.end_time)]
guesses = guesses.loc[guesses.submit_time < guesses.team_id.map(teams.end_time)]
m_guards_n_doors_k_choices = m_guards_n_doors_k_choices.loc[m_guards_n_doors_k_choices.time < m_guards_n_doors_k_choices.team_id.map(teams.end_time)]
solves = solves.loc[solves.solve_time < solves.team_id.map(teams.end_time)]
two_guards_two_doors = two_guards_two_doors.loc[two_guards_two_doors.time < two_guards_two_doors.team_id.map(teams.end_time)]

output = open('index.html', 'w')

# QUICK STATS
output.write('<!-- QUICK STATS -->\n')

quick_stats = pd.DataFrame(columns=['in-person', 'remote-box', 'remote'])
quick_stats.loc['teams'] = teams.interaction_type.value_counts()
quick_stats.loc['finishers'] = teams.loc[teams.finish_time.notna() & (teams.finish_time < teams.end_time)].interaction_type.value_counts()
quick_stats.loc['action meta solves'] = solves.loc[solves.puzzle_id == 'drop-the', 'team_id'].map(teams.interaction_type).value_counts()
quick_stats.loc['participants'] = teams.groupby(teams.interaction_type).member_count.sum()
quick_stats.loc['hints asked'] = hints.groupby(hints.team_id.map(teams.interaction_type)).size()
quick_stats.loc['guesses'] = guesses.groupby(guesses.team_id.map(teams.interaction_type)).size()
quick_stats.loc['solves'] = solves.groupby(solves.team_id.map(teams.interaction_type)).size()

quick_stats['total'] = quick_stats.sum(axis=1)
output.write(quick_stats.to_html())

# TEAM STATS
output.write('<!-- TEAM STATS -->\n')

output.write('<!-- fewest guesses -->\n')
output.write(
    teams.loc[teams.finish_time.notna() & (teams.finish_time < teams.end_time), ['display_name', 'guess_count']]
    .sort_values(by='guess_count').head(10).to_html(index=False))

output.write('<!-- most guesses -->\n')
output.write(teams[['display_name', 'guess_count']].sort_values(by='guess_count', ascending=False).head(10).to_html(index=False))

output.write('<!-- fewest hints -->\n')
output.write(
    teams.loc[teams.finish_time.notna() & (teams.finish_time < teams.end_time), ['display_name', 'hint_count']]
    .sort_values(by='hint_count').head(15).to_html(index=False))

output.write('<!-- most hints -->\n')
output.write(teams[['display_name', 'hint_count']].sort_values(by='hint_count', ascending=False).head(10).to_html(index=False))

output.write('<!-- most hints + replies -->\n')
output.write(teams[['display_name', 'total_hint_count']].sort_values(by='total_hint_count', ascending=False).head(10).to_html(index=False))

# PUZZLE STATS
puzzle_stats = pd.DataFrame(index=puzzles.id, columns=['guesses', 'solves', 'backsolves', 'hints', 'hints + replies', 'tokens'])
puzzle_stats.guesses = guesses.puzzle_id.value_counts().reindex(puzzle_stats.index, fill_value=0)
puzzle_stats.solves = solves.puzzle_id.value_counts().reindex(puzzle_stats.index, fill_value=0)

# Backsolves
output.write('<!-- PUZZLE STATS -->\n')

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
puzzle_stats['hints + replies'] = puzzle_stats.hints + follow_ups.puzzle_id.value_counts().reindex(puzzles.id, fill_value=0)
puzzle_stats.tokens = solves.loc[solves.type == 'answer_token', 'puzzle_id'].value_counts().reindex(puzzle_stats.index, fill_value=0)

output.write('<!-- primary stats -->\n')
output.write(puzzle_stats.reset_index().to_html(index=False))

other_stats = guesses.loc[~guesses.is_correct].groupby(guesses.puzzle_id).guess.value_counts().reset_index(level=1)
other_stats = other_stats.loc[~other_stats.index.duplicated(keep='first')]
other_stats.rename(columns={'guess': 'top_incorrect', 'count': 'relative_frequency'}, inplace=True)
other_stats.relative_frequency = other_stats.relative_frequency / puzzle_stats.solves * 100
other_stats.sort_values(by='relative_frequency', ascending=False, inplace=True)
other_stats.relative_frequency = other_stats.relative_frequency.round(1)

output.write('<!-- secondary stats -->\n')
output.write(other_stats.reset_index().to_html(index=False))

# MISCELLANEOUS STATS
output.write('<!-- MISCELLANEOUS STATS -->\n')

first_solves = (
    solves
    .sort_values(by='solve_time')
    .assign(interaction_type=solves.team_id.map(teams.interaction_type))
    .groupby('interaction_type')
    .head(1)
)
first_solves['display_name'] = first_solves.team_id.map(teams.display_name)
first_solves['solve_duration'] = (first_solves.solve_time - first_solves.interaction_type.map({
    'in-person': in_person_start,
    'remote-box': remote_start,
    'remote': remote_start,
})).apply(lambda td: (
    f'{int(td.total_seconds() // 60)}m {td.total_seconds() % 60:.3f}s'
))

output.write('<!-- first solves -->\n')
output.write(first_solves[['interaction_type', 'puzzle_id', 'display_name', 'solve_duration']].to_html(index=False))

output.write('<!-- longest guesses -->\n')
output.write(guesses.sort_values(by='length', ascending=False)[['guess', 'length']].head(25).to_html(index=False))
output.write('<!-- shortest guesses -->\n')
output.write(guesses.sort_values(by='length')[['guess', 'length']].head(10).to_html(index=False))

output.write('<!-- longest hints -->\n')
output.write(hints.sort_values(by='length', ascending=False)[['request', 'length']].head(1).to_html(index=False))
output.write('<!-- shortest hints -->\n')
output.write(hints.sort_values(by='length')[['request', 'length']].head(10).to_html(index=False))

# EVENT STATS
event_stats = pd.DataFrame(columns=['submitted', 'used'])
for event in answer_tokens.event_id.unique():
    event_stats.loc[event, 'submitted'] = (answer_tokens.event_id == event).sum()
    event_stats.loc[event, 'used'] = ((answer_tokens.event_id == event) & answer_tokens.puzzle_id).sum()

output.write('<!-- EVENT STATS -->\n')
output.write(event_stats.to_html())

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
