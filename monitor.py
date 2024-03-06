import json
import time
import logging

import gspread
from google.oauth2 import service_account

import numpy as np
import grid_generator

DIMENSIONS : tuple = (53, 53)
OUTPUT_RANGE : str = 'A1:BA53'

logging.basicConfig(filename='status.log', level=logging.INFO,
                    format='[%(asctime)s] %(filename)s > %(levelname)s : %(message)s')

with open('setup.json', 'r') as f:
    setup = json.load(f)

scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(setup["key_file"], scopes=scope)
client = gspread.authorize(creds)

spreadsheet = client.open_by_key(setup["spreadsheet_id"])
input_sheet = spreadsheet.worksheet(setup["input_sheet"])
output_sheet = spreadsheet.worksheet(setup["output_sheet"])
previous_value = input_sheet.cell(3, 2).value

def calculate(input_string, output_sheet):
    if not(input_string) or len(words := input_string.split()) < 2:
        logging.warning('Input shorter than two words')
        return 'Too short!'
    if len(words) > 2:
        logging.warning('Input longer than two words')
        return 'Too long!'
    horizontal_word = words[0].upper()
    vertical_word = words[1].upper()
    if not horizontal_word.isalpha() or not vertical_word.isalpha():
        logging.warning('Input contains non-alphabetic characters')
        return '???'
    if len(horizontal_word) > 13 or len(vertical_word) > 13:
        logging.warning('Input word(s) too long')
        return 'Too long!'
    
    t0 = time.perf_counter()
    try:
        grid, _, _ = grid_generator.generate_grids(horizontal_word, vertical_word)
        logging.info(f'Operation succeeded ({round((time.perf_counter() - t0) * 1000, 3)} ms)')
    except grid_generator.AttemptLimitReached:
        logging.info(f'Operation failed ({round((time.perf_counter() - t0) * 1000, 3)} ms)')
        return 'Too hard!'
    extended_grid = np.full(DIMENSIONS, -1)
    extended_grid[1:grid.shape[0] + 1, 1:grid.shape[1] + 1] = grid
    extended_grid = [[n if n >= 0 else '' for n in row] for row in extended_grid.tolist()]
    output_sheet.update(extended_grid, OUTPUT_RANGE)
    return 'Updated!'

while True:
    current_value = input_sheet.cell(3, 2).value
    if current_value != previous_value:
        logging.info(f'Detected update to "{current_value}" for Interactive')
        result = calculate(current_value, output_sheet)
        if result != 'Updated!':
            output_sheet.clear()
        input_sheet.update_cell(6, 2, result)
        previous_value = current_value
    time.sleep(1)