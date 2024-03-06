import pandas as pd
import numpy as np
import logging
import time
import json
import sys

ATTEMPT_LIMIT : int = 100

# Load dimensions
with open('pixel_font/dim.json', 'r') as f:
    dims = json.load(f)
    CHAR_WIDTH : int = dims['width']
    CHAR_HEIGHT : int = dims['height']
    B_RATIO : float = (CHAR_WIDTH + 1) / CHAR_WIDTH # Buffer size ratio

# Load pixel font
with open('pixel_font/map.json', 'r') as f:
    char_grids = {}
    for char, grid in json.load(f).items():
        char_grids[char] = np.array([[c == '█' for c in line] for line in grid.split('\n')], dtype=bool)

class AttemptLimitReached(Exception):
    '''Raised when attempt limit is reached'''
    pass

def word_to_grid(word : str) -> np.ndarray:
    '''Converts a word to its pixel array'''
    word_grid = np.zeros((CHAR_HEIGHT, CHAR_WIDTH * len(word)), dtype=bool)
    for i, char in enumerate(word):
        word_grid[:, i * CHAR_WIDTH: (i + 1) * CHAR_WIDTH] = char_grids[char]
    return word_grid

def mesh_indices(horizontal_grid : np.ndarray, vertical_grid : np.ndarray, operator) -> np.ndarray:
    '''Splits the input grids by layer. For each layer, performs an operation on
    each pairwise combination of inputs.'''
    output_mesh = np.zeros((CHAR_HEIGHT, vertical_grid.shape[1], horizontal_grid.shape[1]), dtype=bool)
    for height in range(CHAR_HEIGHT):
        layer_mesh = np.meshgrid(horizontal_grid[height], vertical_grid[height])
        output_mesh[height] = operator(*layer_mesh)
    return output_mesh

def buffer_indices(dim : int) -> np.ndarray:
    '''Returns a buffered array of indices of length dim'''
    return (np.arange(dim) * B_RATIO).astype(int)

def generate_grids(horizontal_word : str, vertical_word : str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''Returns a grid representing two uppercase input words and their respective grids.'''
    horizontal_grid : np.ndarray = word_to_grid(horizontal_word)
    vertical_grid : np.ndarray = word_to_grid(vertical_word)
    attempts : int = 0

    while attempts < ATTEMPT_LIMIT:

        voxels : np.ndarray = mesh_indices(horizontal_grid, vertical_grid, np.bitwise_and)
        # NOTE: voxels[0] represents the topmost pixels
        
        stack_counts : np.ndarray = voxels.sum(axis=0)
        col_counts : np.ndarray = voxels.sum(axis=1)
        row_counts : np.ndarray = voxels.sum(axis=2)

        # Initialize array to store whether each voxel is necessary
        necessary : np.ndarray = mesh_indices(col_counts == 1, row_counts == 1, np.bitwise_or)

        stack_target : int = CHAR_HEIGHT - 1
        while stack_target >= 0:
            change : bool = False # Flag variable
            overstacked : np.ndarray = np.tile(stack_counts > stack_target, (CHAR_HEIGHT, 1, 1)) # Columns with too many voxels
            check_indices : np.ndarray = np.column_stack(np.where(overstacked & voxels)) # List of indices to be checked
            np.random.shuffle(check_indices)

            # Iterate through indices to be checked for removal
            for height, row, col in check_indices:
                if stack_counts[row, col] > stack_target and not necessary[height, row, col]:
                    voxels[height, row, col] = False
                    stack_counts[row, col] -= 1
                    if voxels[height, row].sum() == 1:
                        necessary[height, row] = True
                    if voxels[height, :, col].sum() == 1:
                        necessary[height, :, col] = True
                    change = True

            if not change:
                if stack_counts.max() > stack_target:
                    break
                stack_target -= 1
        
        attempts += 1
        if stack_counts.max() <= 1:
            break

    if stack_counts.max() > 1:
        logging.warning(f'Reached limit of {attempts} attempt(s)')
        logging.warning(f'Could not succeed without stacking for "{horizontal_word}" and "{vertical_word}"')
        raise AttemptLimitReached

    voxel_display : np.ndarray = np.where(stack_counts, CHAR_HEIGHT - np.argmax(voxels, axis=0), 0)

    rows, cols = stack_counts.shape
    b_rows = int(rows * B_RATIO) - 1
    b_cols = int(cols * B_RATIO) - 1
    
    final_grid : np.ndarray = np.zeros((b_rows, b_cols), dtype=int)
    buffered_indices : np.ndarray = np.meshgrid(buffer_indices(rows), buffer_indices(cols))
    final_grid[buffered_indices[0].flatten(), buffered_indices[1].flatten()] = voxel_display.T.flatten()

    horizontal_grid : np.ndarray = np.full((CHAR_HEIGHT, b_cols), ' ')
    horizontal_grid[:, buffer_indices(cols)] = np.where(voxels.sum(axis=1), '█', ' ')

    vertical_grid : np.ndarray = np.full((CHAR_HEIGHT, b_rows), ' ')
    vertical_grid[:, buffer_indices(rows)] = np.where(voxels.sum(axis=2), '█', ' ')

    logging.info(f'Succeeded for "{horizontal_word}" and "{vertical_word}" in {attempts} attempt(s)')
    return final_grid, horizontal_grid, vertical_grid

def main():
    '''Main function for grid generation. Generates a grid for two words and saves the results to files.'''
    logging.basicConfig(filename='status.log', level=logging.INFO,
                        format='[%(asctime)s] %(filename)s > %(levelname)s : %(message)s')
    # Load words
    if len(sys.argv) != 3:
        exit('Usage: python grid_generator.py <word1> <word2>')
    w1, w2 = sys.argv[1].upper(), sys.argv[2].upper()
    if not w1.isalpha() or not w2.isalpha():
        exit('Both words must be alphabetic')
    
    # Time execution
    t0 : float = time.perf_counter()

    # Generate grid
    try:
        final_grid, horizontal_grid, vertical_grid = generate_grids(w1, w2)
        logging.info(f'Operation succeeded ({round((time.perf_counter() - t0) * 1000, 3)} ms)')
        print(f'Found solution for "{w1}" and "{w2}"')
    except AttemptLimitReached:
        logging.info(f'Operation failed ({round((time.perf_counter() - t0) * 1000, 3)} ms)')
        exit('Could not succeed without stacking')

    # Save results
    pd.DataFrame(final_grid).to_csv('grid.csv', index=False, header=False)
    with open('horizontal.txt', 'w') as f:
        f.write('\n'.join(''.join(line) for line in horizontal_grid))
    with open('vertical.txt', 'w') as f:
        f.write('\n'.join(''.join(line) for line in vertical_grid))

if __name__ == '__main__':
    main()