import numpy as np
import random

from algorithms.backtracking import backtracking
from support.utils import num_faces, grid_size, random_nums, sequencial_nums

def generate_sudoku(difficulty='medium'):
    individual = np.zeros((num_faces, grid_size, grid_size), dtype=int)

    backtracking(individual, random_nums)
    
    if difficulty == 'easy':
        num_to_remove = 50
    elif difficulty == 'medium':
        num_to_remove = 100
    elif difficulty == 'hard':
        num_to_remove = 300
    elif difficulty == 'very-hard':
        num_to_remove = 350
    else:
        num_to_remove = 50

    for _ in range(num_to_remove):
        face = random.randint(0, num_faces - 1)
        row, col = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        while individual[face, row, col] == 0:
            face = random.randint(0, num_faces - 1)
            row, col = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        individual[face, row, col] = 0

    return individual