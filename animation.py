import tkinter as tk
import random
import time


class SnowAnimation:
    def __init__(self, root):
        self.root = root
        self.canvas = None
        self.tension = tk.BooleanVar(value=False)

        self.blizzard_prompt = ["B","L","I","Z","Z","A","R","D"]
        self.clear_prompt = ["C","l","e","a","r"," ","S","k","i","e","s"]

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
        width // 2, height // 2, # Center it using the real width/height
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
                
                if num >= 35:
                    #time.sleep(1)
                    if num >= 50:
                        self.start_snow()
                        return
                    message_added = True
                else:
                    msg += self.blizzard_prompt[num-27]
                    message_added = True
            
            else:
                if num >= 38:
                    #time.sleep(1)
                    if num >= 50:
                        self.end_tension()
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


