import heapq
import numpy as np
from support.utils import is_valid, sequencial_nums, num_faces, grid_size

def _get_empty_cells(puzzle):
    """Retorna uma lista de todas as células vazias (com valor 0)."""
    empty_cells = []
    for face in range(num_faces):
        for row in range(grid_size):
            for col in range(grid_size):
                if puzzle[face, row, col] == 0:
                    empty_cells.append((face, row, col))
    return empty_cells

def _heuristic(puzzle):
    empty_cells = _get_empty_cells(puzzle)
    return len(empty_cells)

class SudokuState:
    def __init__(self, puzzle, g_cost=0, h_cost=0, parent=None, action=None):
        self.puzzle = puzzle  # Estado atual do Sudoku
        self.g_cost = g_cost  # Custo até o momento
        self.h_cost = h_cost  # Heurística (número de células vazias)
        self.f_cost = g_cost + h_cost  # Custo total (f = g + h)
        self.parent = parent  # Referência para o estado anterior
        self.action = action  # Ação realizada (pode ser uma célula preenchida)
    
    def __lt__(self, other):
        """Compara estados para a fila de prioridade do A*."""
        return self.f_cost < other.f_cost

def a_star(puzzle, get_nums):
    initial_state = SudokuState(np.copy(puzzle), g_cost=0, h_cost=_heuristic(puzzle))
    open_list = []
    closed_list = set()
    
    heapq.heappush(open_list, initial_state)  
    visited = set()  
    
    while open_list:
        current_state = heapq.heappop(open_list)  
        
        if current_state.h_cost == 0:  # Resolvido
            puzzle[:] = current_state.puzzle
            return True
        
        visited.add(tuple(current_state.puzzle.flatten()))  # Marca o estado como visitado
        
      
        empty_cells = _get_empty_cells(current_state.puzzle)
        
        for face, row, col in empty_cells:
            for num in sequencial_nums():
                if is_valid(current_state.puzzle, face, row, col, num):
                    new_puzzle = np.copy(current_state.puzzle)
                    new_puzzle[face, row, col] = num
                    
                    # Calcula os custos
                    g_cost = current_state.g_cost + 1
                    h_cost = _heuristic(new_puzzle)
                    
                    # Novo estado
                    new_state = SudokuState(new_puzzle, g_cost, h_cost, parent=current_state, action=(face, row, col, num))
                    
                    if tuple(new_puzzle.flatten()) not in visited:
                        heapq.heappush(open_list, new_state)
    return False