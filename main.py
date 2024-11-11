import numpy as np
import random
import time
import psutil

from support.visualizer import Sudoku3DVisualizer
from support.utils import sequencial_nums, grid_size, num_faces
from support.generator import generate_sudoku

from algorithms.backtracking import backtracking
from algorithms.a_star import a_star
from algorithms.ag import genetic_algorithm

from metrics.metrics import start_metrics, stop_metrics

def print_visual_feedback(message, is_success=True):
    if is_success:
        print(f"\033[92m{message}\033[0m")
    else:
        print(f"\033[91m{message}\033[0m") 

def choose_algorithm():
    print("\nEscolha o algoritmo para resolver o SudoKube:")
    print("1 - Backtracking")
    print("2 - A*")
    print("3 - Genetic Algorithm*")
    choice = input("Digite o número correspondente ao algoritmo: ")
    
    if choice == '1':
        return backtracking
    elif choice == '2':
        return a_star
    elif choice == '3':
        return genetic_algorithm
    else:
        print("Escolha inválida. Utilizando Backtracking por padrão.")
        return backtracking

def choose_difficulty():
    print("\nEscolha a dificuldade:")
    print("1 - Fácil")
    print("2 - Média")
    print("3 - Difícil")
    print("4 - Muito Difícil")
    choice = input("Digite o número correspondente à dificuldade: ")
    
    if choice == '1':
        return 'easy'
    elif choice == '2':
        return 'medium'
    elif choice == '3':
        return 'hard'
    elif choice == '4':
        return 'very-hard'
    else:
        print("Escolha inválida. Utilizando dificuldade 'média' por padrão.")
        return 'medium'


print("Iniciando a geração do SudoKube...")


difficulty = choose_difficulty()


puzzle = generate_sudoku(difficulty)
generated = np.copy(puzzle)

print_visual_feedback("SudoKube gerado com sucesso!", is_success=True)

algorithm = choose_algorithm()

start_metrics()

print("\nExecutando algoritmo para resolver o SudoKube...")
solved = algorithm(puzzle, sequencial_nums)

stop_metrics()

if solved:
    print_visual_feedback(f"SudoKube Resolvido com sucesso!", is_success=True)
else:
    print_visual_feedback("Sudokube sem solução encontrada!", is_success=False)

print("\nExibindo o SudoKube...")
Sudoku3DVisualizer(generated, puzzle).display()
