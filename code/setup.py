import grid as grid
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
import numpy as np
import json

current_mode = "colony"  # colony, food, obstacle
env = None
size = 9
fig, ax = None, None
cell_artists = {}
colony_set = False

buttons = []            # store button references
selected_button = None  # currently selected button


def draw_grid():
    global ax, fig, cell_artists
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_xticks(np.arange(0, size + 1))
    ax.set_yticks(np.arange(0, size + 1))
    ax.grid(True)
    ax.set_aspect("equal")
    fig.canvas.mpl_connect("button_press_event", on_click)
    fig.canvas.mpl_connect('motion_notify_event', on_drag)
    cell_artists = {}
    plt.subplots_adjust(bottom=0.25)


def update_display(x, y):
    global cell_artists, env
    key = (x, y)
    # remove existing if any
    if key in cell_artists:
        cell_artists[key].remove()
        del cell_artists[key]

    val = env.grid[x, y]
    if val == 0:
        fig.canvas.draw()
        return

    # Map grid coordinates to matplotlib rectangle coords (remember y inverted)
    rect = patches.Rectangle(
        (x, y), 1, 1,
        facecolor='white',  # Use white as default background color, not empty string
        edgecolor='black',
        linewidth=1,
        zorder=4
    )
    if val == 1:
        rect.set_facecolor('red')
    elif val == 2:
        rect.set_facecolor('green')
    elif val == 3:
        rect.set_facecolor('black')

    ax.add_patch(rect)
    cell_artists[key] = rect
    fig.canvas.draw()


def erase_all(event):
    global colony_set
    # Clear data
    env.grid[:, :] = 0
    env.food_positions.clear()
    env.obstacle_positions.clear()
    env.colony_position = None
    colony_set = False

    # Remove all cell patches from the axes
    for art in cell_artists.values():
        art.remove()
    cell_artists.clear()

    # Redraw the grid (just the lines, no colored cells)
    fig.canvas.draw()
    print("All cells erased.")


def redraw_all():
    # Clear all patches then redraw entire grid from env.grid
    for art in cell_artists.values():
        art.remove()
    cell_artists.clear()
    for x in range(size):
        for y in range(size):
            if env.grid[x, y] != 0:
                update_display(x, y)


def on_click(event):
    global current_mode, env, colony_set
    if event.inaxes != ax:
        return
    x, y = int(event.xdata), int(event.ydata)
    if x < 0 or x >= size or y < 0 or y >= size:
        return

    if event.button == 3:  # Right-click to erase
        env.grid[x, y] = 0
        if (x, y) in env.food_positions:
            env.food_positions.remove((x, y))
        if (x, y) in env.obstacle_positions:
            env.obstacle_positions.remove((x, y))
        if (x, y) == env.colony_position:
            env.colony_position = None
            global colony_set
            colony_set = False
        update_display(x, y)
        return

    # Left-click to place
    if current_mode == "colony":
        if colony_set:
            print("Colony already set! Right-click to erase.")
            return
        env.place_colony((x, y))
        colony_set = True
    elif current_mode == "food":
        if (x, y) not in env.food_positions:
            env.add_food((x, y))
    elif current_mode == "obstacle":
        if (x, y) not in env.obstacle_positions:
            env.add_obstacle((x, y))
    update_display(x, y)


def on_drag(event):
    if event.inaxes != ax:
        return
    x, y = int(event.xdata), int(event.ydata)
    if x < 0 or x >= size or y < 0 or y >= size:
        return

    # Left-drag to add obstacle
    if event.button == 1 and current_mode == "obstacle":
        if (x, y) not in env.obstacle_positions:
            env.add_obstacle((x, y))
            update_display(x, y)
    # Right-drag to erase
    elif event.button == 3:
        env.grid[x, y] = 0
        if (x, y) in env.food_positions:
            env.food_positions.remove((x, y))
        if (x, y) in env.obstacle_positions:
            env.obstacle_positions.remove((x, y))
        if (x, y) == env.colony_position:
            env.colony_position = None
            global colony_set
            colony_set = False
        update_display(x, y)


def set_mode(label, btn):
    global current_mode, buttons, selected_button
    current_mode = label
    print(f"Mode: {label}")

    # Reset all buttons color
    for b in buttons:
        b.ax.set_facecolor('lightgray')
        b.ax.figure.canvas.draw_idle()

    # Highlight selected button
    btn.ax.set_facecolor('lightblue')
    btn.ax.figure.canvas.draw_idle()

    selected_button = btn


def done(event):
    global fig
    try:
        print("Done clicked!")
        data = {
            "size": env.size,
            "colony": env.colony_position,
            "food": list(env.food_positions),
            "obstacles": list(env.obstacle_positions)
        }
        with open("environment.json", "w") as f:
            json.dump(data, f, indent=2)
        print("Saved environment.json")

        fig.savefig("environment.png")
        print("Saved environment.png")

        plt.close(fig)
    except Exception as e:
        print(f"Error in done(): {e}")


def create_buttons():
    global buttons
    modes = [("Colony", "colony"), ("Food", "food"),
             ("Obstacle", "obstacle")]
    button_width = 0.12
    spacing = 0.01
    start_x = 0.05

    color_map = {
        "colony": "red",
        "food": "green",
        "obstacle": "black"
    }

    buttons.clear()

    for i, (label, name) in enumerate(modes):
        ax_btn = plt.axes(
            [start_x + i * (button_width + spacing), 0.05, button_width, 0.06])
        btn = Button(ax_btn, label)
        buttons.append(btn)
        btn.label.set_fontweight('bold')
        btn.label.set_color(color_map[name])
        btn.on_clicked(lambda event, n=name, b=btn: set_mode(n, b))

    set_mode("colony", buttons[0])

    # Done button
    ax_done = plt.axes(
        [start_x + len(modes) * (button_width + spacing), 0.05, 0.12, 0.06])
    btn_done = Button(ax_done, "Done")
    btn_done.on_clicked(done)
    buttons.append(btn_done)  # <-- Add this line!

    ax_erase = plt.axes([start_x + (len(modes) + 1) *
                        (button_width + spacing), 0.05, 0.12, 0.06])
    btn_erase = Button(ax_erase, "Erase All")
    btn_erase.on_clicked(erase_all)
    buttons.append(btn_erase)

    # Add text box for erase instruction
    ax_txt = plt.axes([start_x + (len(modes) + 2) *
                      (button_width + spacing) + 0.01, 0.05, 0.20, 0.06])
    ax_txt.axis('off')
    ax_txt.text(0, 0.5, 'Right-click to erase',
                fontsize=10, verticalalignment='center')


def setup_env():
    global env, size
    try:
        size = int(input("Enter grid size (e.g., 9): "))
    except:
        size = 9
    env = grid.Grid(size)
    draw_grid()
    create_buttons()
    plt.show()

    return env


if __name__ == "__main__":
    env = setup_env()
