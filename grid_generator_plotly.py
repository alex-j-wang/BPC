import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go

import time
import json
import sys

ATTEMPT_LIMIT : int = 100
horizontal_word : str = 'BROWN'
vertical_word : str = 'PUZZLEHUNT'

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

z, y, x = np.where(voxels)
z = CHAR_HEIGHT - z
x = -x

x = (x * 4/3).astype(int)
y = (y * 4/3).astype(int)

scatter = go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=10,
        color='turquoise'
    )
)

layout = go.Layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        camera=dict(projection={"type": "orthographic"}),
        aspectmode='data'
    ),
    hovermode=False
)

fig = go.Figure(data=[scatter], layout=layout)
fig.write_html('grid.html')