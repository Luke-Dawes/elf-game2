import tkinter as tk
import random


class SnowAnimation:
    def __init__(self, root):
        self.root = root
        self.canvas = None

        self.blizzard_prompt = ["B","L","I","Z","Z","A","R","D", "!"]
        self.clear_prompt = ["C","l","e","a","r"," ","S","k","i","e","s", "!"]

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

    def end_tension(self):
        self.canvas.destroy()

    def play(self, snowstorm) -> None:
        # get current window size

        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg='White')
        self.canvas.pack()

        self.text_id = self.canvas.create_text(
        width // 2, height // 2,  # Center it using the real width/height
        text="", 
        fill="black",           # Ensure it's visible on white
        font=("Terminal", 20)
    )


        self.building_tension(snowstorm, "", reset_msg=False)

    def building_tension(self, snowStorm, msg: str, num: int=0, reset_msg: bool=False):
        message_added = False
        if num >= 27:
            if not reset_msg: 
                
                msg = ""
                reset_msg = True

            if snowStorm: 
                
                if num >= 36:
                    #time.sleep(1)
                    if num >= 50:
                        self.start_snow()
                        return
                    message_added = True
                else:
                    msg += self.blizzard_prompt[num-27]
                    message_added = True
            
            else:
                if num >= 39:
                    #time.sleep(1)
                    if num >= 50:
                        self.start_sun()
                        return
                    message_added = True

                else:
                    msg += self.clear_prompt[num-27]
                    message_added = True

            
            
        
        if not message_added: msg += '.'

        self.canvas.itemconfig(self.text_id, text=msg)
        self.root.after(99, self.building_tension, snowStorm, msg, num +1, reset_msg)
    
    def start_snow(self):
        # canvas for animation
        self.canvas.delete(self.text_id)
        self.canvas.config(bg="black")
        self.canvas.pack()

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()


        self.snow_list = []
        for _ in range(100):
            size = 5
            x = random.randint(0, width - size)
            y = random.randint(0, height - size)

            snow = self.canvas.create_rectangle(x, y, x + size, y + size, fill='white',
                                                outline='')  # create rectangles for snow

            self.snow_list.append(snow)  # add it to the list

        self.move_snow()  # call the move snow func once, thought it runs async

        self.root.after(4000, self.stop_snow)  # animation for 4s

    def start_sun(self):
        self.canvas.delete(self.text_id)
        self.canvas.config(bg="lightblue")
        self.canvas.pack()

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        r = 50
        x, y = width-(3*r), 3*r
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="yellow", outline="yellow")  # sun

        self.canvas.create_polygon((-100, height), (width+400, height), (width/2+150, height - 500), fill="dimgrey")  # volcano
        self.canvas.create_polygon((width/2-200, height-400), (width/2+500, height-400), (width/2+150, height-510), fill="lightblue")  # top of volcano
        self.canvas.create_arc((width/2+30, height-380), (width/2+270, height-420), extent=180, start=180, fill="red", outline="red")  # lava

        self.canvas.create_polygon((0, height), (400, height), (200, height - 400), fill="grey")  # mountain 1
        self.canvas.create_polygon((170, height-344), (230, height-344), (200, height - 400), fill="white")  # mountain 1 top
        self.canvas.create_polygon((0, height), (250, height), (125, height - 300), fill="grey")  # mountain 2

        self.canvas.create_arc(0, height-100, width, height+100, extent=180, fill="lightgreen", outline="lightgreen")  # hill

        # trees
        w, h = 40, 60
        tree_coords_1 = [(10, 10), (50, 10), (110, 50), (170, 80)]
        for (x, y) in tree_coords_1:
            self.canvas.create_polygon((x, height-y), (x+w, height-y), (x+w/2, height-y-h), fill="forestgreen", outline="forestgreen")
        w, h = 40, 60
        tree_coords_2 = [(400, 100), (500, 60), (420, 80), (390, 50), (480, 20), (450, 40), (520, 10), (370, 5), (600, 40), (700, 5), (400, -10)]
        for (x, y) in tree_coords_2:
            self.canvas.create_arc(x, height-y, x+w, height-y-h, extent=359, fill="darkgreen", outline="darkgreen")


        self.birds = []
        for i in range(50, 200, 30):
            bird = self.canvas.create_line(i, i, i, i+1, arrow="last", arrowshape=(8, 20, 40), fill="grey")
            self.birds.append(bird)

        self.animate_clear_day()

        self.root.after(3000, self.canvas.destroy)

    def animate_clear_day(self, n=0):
        for bird in self.birds:
            self.canvas.move(bird, 1, 0)
        n += 1
        if n > 50:
            return
        self.root.after(33, self.animate_clear_day(n))

