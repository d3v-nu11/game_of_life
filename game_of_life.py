import tkinter as tk
import random

GRID_WIDTH = 40
GRID_HEIGHT = 40
CELL_SIZE = 10

SURVIVAL_RULE = [2, 3]
BIRTH_RULE = [3]

GRID = [[random.randint(0, 1) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]


def update_grid(survival_rule, birth_rule):
    new_grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dy == 0 and dx == 0:
                        continue
                    elif y + dy < 0 or y + dy >= GRID_HEIGHT or x + dx < 0 or x + dx >= GRID_WIDTH:
                        continue
                    elif GRID[y+dy][x+dx] == 1:
                        neighbors += 1
            if GRID[y][x] == 1 and neighbors in survival_rule:
                new_grid[y][x] = 1
            elif GRID[y][x] == 0 and neighbors in birth_rule:
                new_grid[y][x] = 1
    return new_grid


def draw_grid(canvas):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if GRID[y][x] == 1:
                canvas.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill="white", outline="black")
            else:
                canvas.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill="black", outline="black")


def start_simulation(survival_rule, birth_rule):
    global GRID
    SURVIVAL_RULE = survival_rule
    BIRTH_RULE = birth_rule

    stop_simulation = False

    def on_closing():
        nonlocal stop_simulation
        stop_simulation = True
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)
    while not stop_simulation:
        GRID = update_grid(SURVIVAL_RULE, BIRTH_RULE)
        if canvas.winfo_exists() and window.winfo_exists():
            canvas.delete("all")
            draw_grid(canvas)
            canvas.update()
        else:
            break


window = tk.Tk()
window.title("Game of Life")

canvas = tk.Canvas(window, width=GRID_WIDTH*CELL_SIZE, height=GRID_HEIGHT*CELL_SIZE)
canvas.pack()

survival_rule_label = tk.Label(window, text="Survival rule:")
survival_rule_label.pack()
survival_rule_entry = tk.Entry(window)
survival_rule_entry.insert(0, "2,3")
survival_rule_entry.pack()

birth_rule_label = tk.Label(window, text="Birth rule:")
birth_rule_label.pack()
birth_rule_entry = tk.Entry(window)
birth_rule_entry.insert(0, "3")
birth_rule_entry.pack()

start_button = tk.Button(window,text="Start", command=lambda: start_simulation(list(map(int, survival_rule_entry.get().split(","))), list(map(int, birth_rule_entry.get().split(",")))))
start_button.pack()

window.mainloop()
