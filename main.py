import tkinter as tk

wn = tk.Tk()
wn.geometry('500x350')
wn.title('Elf Game 2')
wn.config(background='lightblue')

class game:
    def __init__(self):
        pass

    def update(self):
        pass

    def clicked(self):
        print("clicked")

    def setup(self):
        b1 = tk.Button(wn, width=30, pady=40, text='Click Me', command=self.clicked)
        b1.grid(row=0, column=0)

        
game = game()
game.setup()

wn.mainloop()
