import numpy as np
import random

from support.utils import num_faces, grid_size, is_valid

def backtracking(individual, get_nums):
    for face in range(num_faces):
        for row in range(grid_size):
            for col in range(grid_size):
                if individual[face, row, col] == 0:
                    for num in get_nums():
                        if is_valid(individual, face, row, col, num):
                            individual[face, row, col] = num
                            if backtracking(individual, get_nums):
                                return True
                            individual[face, row, col] = 0
                    return False
    return True
