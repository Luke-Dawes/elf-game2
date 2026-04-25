import tkinter as tk
import random


class SnowAnimation:
    def __init__(self, root):
        self.root = root

    def move_snow(self) -> None:
        for particle in self.snow_list:
            self.canvas.move(particle, 0, 1)  # makes the y coordinate of particle decrease by 1

        self.root.after(33, self.move_snow)  # async (keeps this function running every .3) but lets the game continue

    def stop_snow(self) -> None:  # deletes all the snow
        for snow in self.snow_list:
            self.canvas.delete(snow)  # deletes the snow from the canvas
        self.snow_list.clear()  # clears the list
        self.canvas.destroy()  # destroys the canvas (the background)

    def play(self) -> None:
        self.canvas = tk.Canvas(self.root, width=700, height=600, bg='Black')
        self.canvas.config(width=1920, height=1080)
        self.canvas.pack()  # display the canvas

        self.snow_list = []
        for _ in range(50):
            x = random.randint(0, 700)
            y = random.randint(0, 500)
            size = 5

            snow = self.canvas.create_rectangle(x, y, x + size, y + size, fill='white',
                                                outline='')  # create rectangles for snow

            self.snow_list.append(snow)  # add it to the list

        self.move_snow()  # call the move snow func once, thought it runs async

        self.root.after(4000, self.stop_snow)  # after like 3 seconds it calls stop snow which deletes everything
        # self.root.after(4005, self.create_widgets) #create the widgets again which have been deleted
        # self.root.after(4020, self.refresh_ui) #refresh them so they contain the correct data
        # self.root.after(4030, self.blizzard_done)