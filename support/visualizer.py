import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button

class Sudoku3DVisualizer:
    def __init__(self, puzzle, solved_puzzle=None):
        self.original_puzzle = np.copy(puzzle)  # Armazena o estado inicial (antes da resolução)
        self.solved_puzzle = solved_puzzle if solved_puzzle is not None else puzzle
        self.puzzle = self.solved_puzzle
        self.num_faces = puzzle.shape[0]
        self.grid_size = puzzle.shape[1]
        self.colors = {
            1: 'lightgreen',
            2: 'lightblue',
            3: 'lightcoral',
            4: 'lightpink',
            5: 'lightyellow',
            6: 'lightgray',
            7: 'lightsalmon',
            8: 'lightcyan',
            9: 'lightgoldenrodyellow'
        }
        self.highlighted_value = None
        self.mouse_enabled = True
        self.painted_all = False
        self.show_original = False  # Estado para mostrar o original ou o resolvido
        self.fig, self.axs = plt.subplots(3, 3, figsize=(12, 8))  # Alterado para 3x3
        self.axs = self.axs.flatten()  # Garantir que axs seja um array unidimensional
        self.rects = []
        self.texts = []  # Armazena os textos para cada célula
        self.init_ui()

    def init_ui(self):
        # Botão para pintar todos e alternar a pintura
        try:
            paint_button_ax = self.fig.add_axes([0.4, 0.01, 0.2, 0.05])
            self.paint_all_button = Button(paint_button_ax, 'Pintar Todos')
            self.paint_all_button.on_clicked(self.toggle_paint_all)

            # Botão para alternar entre o original e o resolvido
            toggle_button_ax = self.fig.add_axes([0.7, 0.01, 0.2, 0.05])
            self.toggle_puzzle_button = Button(toggle_button_ax, 'Mostrar original')
            self.toggle_puzzle_button.on_clicked(self.toggle_puzzle_view)

            # Conectar o evento de clique
            self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        except Exception as e:
            print(f"Erro ao inicializar a interface: {e}")

    def display(self):
        try:
            for face in range(self.num_faces):
                ax = self.axs[face]
                ax.set_title(f"Face {face + 1}")
                ax.set_xticks(np.arange(self.grid_size + 1) - 0.5)
                ax.set_yticks(np.arange(self.grid_size + 1) - 0.5)
                ax.set_xticklabels([])
                ax.set_yticklabels([])
                ax.grid(True)

                # Ajustar limites para garantir que os quadrados estejam visíveis
                ax.set_xlim(-0.5, self.grid_size - 0.5)
                ax.set_ylim(self.grid_size - 0.5, -0.5)

                # Desenhar as linhas do subgrid 3x3
                for i in range(0, self.grid_size, 3):
                    ax.axhline(i - 0.5, color='black', linewidth=2)
                    ax.axvline(i - 0.5, color='black', linewidth=2)

                for row in range(self.grid_size):
                    for col in range(self.grid_size):
                        value = self.puzzle[face, row, col]
                        rect = Rectangle((col - 0.5, row - 0.5), 1, 1, facecolor='white', edgecolor='black')
                        ax.add_patch(rect)
                        self.rects.append((face, row, col, rect))
                        if value != 0:
                            text = ax.text(col, row, str(value), ha='center', va='center', fontsize=12, color='black')
                            self.texts.append(text)  # Armazena o texto para poder limpar depois

            plt.tight_layout(rect=[0, 0.1, 1, 1])  # Espaço para os botões
            plt.show()
        except Exception as e:
            print(f"Erro ao exibir o Sudoku: {e}")

    def on_click(self, event):
        try:
            if self.mouse_enabled and event.inaxes:
                # Obtém o índice da face a partir do subplot atual
                face_index = np.where(self.axs == event.inaxes)[0][0]

                # Obtém a linha e a coluna a partir das coordenadas do mouse
                row = int(np.floor(event.ydata + 0.5))
                col = int(np.floor(event.xdata + 0.5))

                if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                    value = self.puzzle[face_index, row, col]
                    if value != self.highlighted_value:
                        self.highlighted_value = value
                        self.highlight_cells(value)
        except Exception as e:
            return

    def highlight_cells(self, value):
        """Destaca células com o mesmo valor."""
        try:
            for face, row, col, rect in self.rects:
                if self.puzzle[face, row, col] == value:
                    rect.set_facecolor(self.colors.get(value, 'white'))
                else:
                    rect.set_facecolor('white')
            self.fig.canvas.draw_idle()
        except Exception as e:
            print(f"Erro ao destacar células: {e}")

    def toggle_paint_all(self, event):
        """Alterna entre pintar todos os números e desabilitar o efeito do clique."""
        try:
            if self.painted_all:
                self.unpaint_all()
            else:
                self.paint_all()
        except Exception as e:
            print(f"Erro ao alternar a pintura de todas as células: {e}")

    def paint_all(self):
        """Pinta todos os números e desabilita a interação de clique."""
        try:
            self.mouse_enabled = False
            self.painted_all = True
            self.paint_all_button.label.set_text('Remover Pintura')
            for face, row, col, rect in self.rects:
                value = self.puzzle[face, row, col]
                if value != 0:
                    rect.set_facecolor(self.colors.get(value, 'white'))
            self.fig.canvas.draw_idle()
        except Exception as e:
            print(f"Erro ao pintar todas as células: {e}")

    def unpaint_all(self):
        """Remove todas as cores e reabilita a interação de clique."""
        try:
            self.mouse_enabled = True
            self.painted_all = False
            self.paint_all_button.label.set_text('Pintar Todos')
            for face, row, col, rect in self.rects:
                rect.set_facecolor('white')
            self.fig.canvas.draw_idle()
        except Exception as e:
            print(f"Erro ao remover pintura: {e}")

    def toggle_puzzle_view(self, event):
        """Alterna entre mostrar o puzzle original e o resolvido."""
        try:
            if self.show_original:
                self.puzzle = np.copy(self.solved_puzzle)  # Mostra o Sudoku resolvido
                self.toggle_puzzle_button.label.set_text('Mostrar original')
            else:
                self.puzzle = np.copy(self.original_puzzle)  # Mostra o Sudoku original
                self.toggle_puzzle_button.label.set_text('Mostrar Resolvido')
            self.show_original = not self.show_original
            self.update_display()
        except Exception as e:
            print(f"Erro ao alternar entre o puzzle original e resolvido: {e}")

    def update_display(self):
        """Atualiza a exibição do puzzle após alternar entre original e resolvido."""
        try:
            # Limpa todos os textos antigos
            for text in self.texts:
                text.remove()
            self.texts = []

            # Atualiza o display com o puzzle atual
            for face, row, col, rect in self.rects:
                rect.set_facecolor('white')  # Reseta a cor de fundo
                value = self.puzzle[face, row, col]
                if value != 0:
                    text = self.axs[face].text(col, row, str(value), ha='center', va='center', fontsize=12, color='black')
                    self.texts.append(text)
            self.fig.canvas.draw_idle()
        except Exception as e:
            print(f"Erro ao atualizar o display: {e}")
