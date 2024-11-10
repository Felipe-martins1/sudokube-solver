import numpy as np
import random

num_faces = 9
grid_size = 9

def _get_adjacent_faces(face):
    adj_faces = {
        0: [1, 2, 4, 5],
        1: [0, 3, 2, 5],
        2: [0, 1, 3, 4],
        3: [1, 2, 5, 4],
        4: [0, 2, 3, 5],
        5: [0, 1, 3, 4]
    }
    return adj_faces[face]

def is_valid(individual, face, row, col, num):
    if num in individual[face, row, :]:
        return False

    if num in individual[face, :, col]:
        return False

    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    if num in individual[face, row_start:row_start+3, col_start:col_start+3]:
        return False
    
    return True

def random_nums():
    valid_nums = list(range(1, grid_size + 1))
    random.shuffle(valid_nums)
    return valid_nums

def sequencial_nums():
    return list(range(1, grid_size + 1))