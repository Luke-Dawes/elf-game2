import tkinter as tk
import random


class SnowAnimation:
    def __init__(self, root):
        self.root = root
        self.canvas = None

    def move_snow(self, times: int=0) -> None:

        if times >= 50: return

        for particle in self.snow_list:
            self.canvas.move(particle, 0, 1)  # makes the y coordinate of particle decrease by 1

        self.root.after(33, self.move_snow)  # async (keeps this function running every .3) but lets the game continue

    def stop_snow(self) -> None:  # deletes all the snow
        for snow in self.snow_list:
            self.canvas.delete(snow)  # deletes the snow from the canvas
        self.snow_list.clear()  # clears the list
        self.canvas.destroy()  # destroys the canvas (the background)

    def play(self) -> None:
        # get current window size
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # canvas for animation
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg='Black')
        self.canvas.pack()

        self.snow_list = []
        for _ in range(50):
            size = 5
            x = random.randint(0, width - size)
            y = random.randint(0, height - size)

            snow = self.canvas.create_rectangle(x, y, x + size, y + size, fill='white',
                                                outline='')  # create rectangles for snow

            self.snow_list.append(snow)  # add it to the list

        self.move_snow()  # call the move snow func once, thought it runs async

        self.root.after(4000, self.stop_snow)  # animation for 4s
