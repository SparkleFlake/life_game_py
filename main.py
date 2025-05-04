import tkinter as tk
import random
import copy

cell_size = 10
canvas_width = 1000
canvas_height = 900
update_delay = 100
initial_density = 0.3


grid_width = canvas_width // cell_size
grid_height = canvas_height // cell_size


color_dead = 'white'
color_alive = 'black'
color_grid = '#CCCCCC'

logical_grid = []
canvas_cells = []
is_running = False
root = None
canvas = None
start_stop_button = None


def count_neighbors(grid,row,col):
    live_neighbours = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0:
                continue
            neighbour_r = (row + i) % grid_height
            neighbour_c = (col + j) % grid_width
            if grid[neighbour_r][neighbour_c] == 1:
                live_neighbours +=1
    return live_neighbours

def calculate_next_generation(current_grid):
    """Вычисляет следующее поколение логической сетки."""
    next_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    
    for r in range(grid_height):
        for c in range(grid_width):
            live_neighbors = count_neighbors(current_grid,r,c)
            cell_state = current_grid[r][c]
            
            if cell_state == 1:
                if live_neighbors == 3 or live_neighbors == 2 or live_neighbors == 1:
                    next_grid[r][c] = 1 # выживает
            else:
                if live_neighbors == 2 or live_neighbors == 1:
                    next_grid[r][c] = 1 # рождается
    return next_grid

def create_grids():
    """Создает логическую сетку и сетку ID для холста."""
    global logical_grid, canvas_cells
    logical_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    canvas_cells = [[None for _ in range(grid_width)] for _ in range(grid_height)]


def draw_grid_on_canvas():
    """Рисует сетку из прямоугольников на холсте."""
    global canvas, canvas_cells
    for r in range(grid_height):
        for c in range(grid_width):
            x1 = c*cell_size
            y1 = r*cell_size
            x2 = x1*cell_size
            y2 = y1*cell_size
            
            cell_id = canvas.create_rectangle(x1,y1,x2,y2, fill = color_dead, outline = color_grid)
            canvas_cells[r][c] = cell_id
            canvas.tag_bind(cell_id,'<Button-1>',lambda event,row=r,col=c: handle_cell_click(event,row,col))
            
def update_visuals():
    """Обновляет цвета клеток на холсте в соответствии с логической сеткой."""
    global logical_grid, canvas, canvas_cells
    for r in range(grid_height):
        for c in range(grid_width):
            cell_id = canvas_cells[r][c]
            color = color_alive if logical_grid[r][c] ==1 else color_dead
            canvas.itemconfig(cell_id,fill=color)

def randomize_grid():
    """Заполняет логическую сетку случайно и обновляет холст."""
    global logical_grid
    if is_running:
        return
    for r in range(grid_height):
        for c in range(grid_width):
            if random.random() < initial_density:
                logical_grid[r][c] = 1
            else:
                logical_grid[r][c] = 0
    update_visuals()
    
def clear_grid():
    """Очищает сетку (делает все клетки мертвыми)."""
    global logical_grid
    if is_running:
        return
    for r in range(grid_height):
        for c in range(grid_width):
            logical_grid[r][c] = 0
    
    update_visuals()

def handle_cell_click(event, row, col):
    """Обрабатывает клик по клетке (только если симуляция остановлена)."""
    global logical_grid, canvas, canvas_cells
    if not is_running:
        logical_grid[row][col] = 1 - logical_grid[row][col]
        cell_id = canvas_cells[row][col]
        color = color_alive if logical_grid[row][col] == 1 else color_dead
        canvas.itemconfig(cell_id, fill=color)
        

def simulation_step():
    """Выполняет один шаг симуляции и планирует следующий."""
    global logical_grid, is_running
    if not is_running:
        return
    
    next_gen_grid = calculate_next_generation(logical_grid)
    logical_grid = next_gen_grid
    update_visuals()
    
    root.after(update_delay,simulation_step)
    
def perform_single_step():
    """Выполняет только один шаг симуляции (для кнопки Step)."""
    global logical_grid
    if is_running:
        return
    
    next_gen_grid = calculate_next_generation(logical_grid)
    logical_grid = next_gen_grid
    update_visuals()

def toggle_simulation():
    """Запускает или останавливает симуляцию."""
    global is_running,start_stop_button
    if is_running:
        is_running=False
        start_stop_button.config(text='Старт')
    else:
        is_running = True
        start_stop_button.config(text='Стоп')
        simulation_step() # продолжаем жить
   
   
        
# --- Настройка GUI ---
def setup_gui():
    global root, canvas, start_stop_button

    root = tk.Tk()
    root.title("Игра 'Жизнь' на Python/Tkinter")

    # Создаем холст
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg=color_dead)
    canvas.pack(pady=10) # pack размещает виджет, pady добавляет отступ

    # Создаем логическую и визуальную сетки
    create_grids()
    draw_grid_on_canvas() # Рисуем клетки на холсте

    # Создаем фрейм для кнопок
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    # Кнопка Start/Stop
    start_stop_button = tk.Button(button_frame, text="Start", width=10, command=toggle_simulation)
    start_stop_button.pack(side=tk.LEFT, padx=5)

    # Кнопка Step
    step_button = tk.Button(button_frame, text="Step", width=10, command=perform_single_step)
    step_button.pack(side=tk.LEFT, padx=5)

    # Кнопка Randomize
    random_button = tk.Button(button_frame, text="Randomize", width=10, command=randomize_grid)
    random_button.pack(side=tk.LEFT, padx=5)

    # Кнопка Clear
    clear_button = tk.Button(button_frame, text="Clear", width=10, command=clear_grid)
    clear_button.pack(side=tk.LEFT, padx=5)

# --- Запуск ---
if __name__ == "__main__":
    setup_gui()
    root.mainloop() # Запускаем главный цикл Tkinter