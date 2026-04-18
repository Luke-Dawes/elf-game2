import tkinter as tk
from tkinter import messagebox
from TeamClass import Team
import random
import time

class ElfGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Elf Resource Manager - Turn Based")
        self.root.geometry("700x600")

        # Game State
        self.current_turn = 1
        self.current_team_idx = 0
        self.num_teams = 4

        #snow
        self.snowList = []
        
        # Location Multipliers (Money earned per elf)
        self.locations = [
            {"name": "Woods", "payout": 10},
            {"name": "Deep Forest", "payout": 25},
            {"name": "Mountains", "payout": 50},
            {"name": "Mystic Cave", "payout": 100}
        ]

        # Team Data: [Money, Total Elves]
        self.teams_data = [Team(f"Team {i+1}") for i in range(4)] #this is now a list of teams
        #self.teams_data = [{"money": 0, "elves": 10, "name": f"Team {i+1}"} for i in range(4)]
        
        self.create_widgets()
        self.refresh_ui()

    def create_widgets(self):
        # Header Info
        self.header_label = tk.Label(self.root, text="", font=("Arial", 16, "bold"))
        self.header_label.pack(pady=10)

        self.team_info_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.team_info_label.pack()

        # Input Area
        self.input_frame = tk.LabelFrame(self.root, text="Send Elves to Locations", padx=20, pady=20)
        self.input_frame.pack(pady=20)

        self.elf_entries = []
        for i, loc in enumerate(self.locations):
            tk.Label(self.input_frame, text=f"{loc['name']} (${loc['payout']}/elf):").grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(self.input_frame, width=10)
            entry.insert(0, "0")
            entry.grid(row=i, column=1, padx=10)
            self.elf_entries.append(entry)

        # Submit Button
        self.submit_btn = tk.Button(self.root, text="Confirm Turn", command=self.process_turn, bg="green", fg="white", font=("Arial", 12, "bold"))
        self.submit_btn.pack(pady=10)

        # Leaderboard
        self.leaderboard_frame = tk.LabelFrame(self.root, text="Leaderboard", padx=10, pady=10)
        self.leaderboard_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        
        self.leaderboard_labels = []
        for i in range(4):
            lbl = tk.Label(self.leaderboard_frame, text="")
            lbl.pack(side="left", expand=True)
            self.leaderboard_labels.append(lbl)

    def refresh_ui(self):
        team = self.teams_data[self.current_team_idx]
        self.header_label.config(text=f"Turn {self.current_turn}: {team.name}'s Move") #instead of using team["name"] its now a class syntax
        self.team_info_label.config(text=f"Available Elves: {team.elves} | Current Money: ${team.money}") #changed here aswell
        
        for i, lbl in enumerate(self.leaderboard_labels):
            t = self.teams_data[i]
            lbl.config(text=f"{t.name}\nMoney: ${t.money}\nElves: {t.elves}") #as well as here

    def process_turn(self):
        team = self.teams_data[self.current_team_idx]
        try:
            allocations = [int(e.get()) for e in self.elf_entries]
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return

        total_sent = sum(allocations)
        if total_sent > team.elves:
            messagebox.showwarning("Warning", f"You only have {team.elves} elves!") #here
            return

        # Calculate Earnings
        team.sentElves = {
            self.locations[i]["name"]: allocations[i]
            for i in range(len(self.locations))
        }

        #!delayed this untill the end so it calculates it all together  
        #round_income = sum(allocations[i] * self.locations[i]["payout"] for i in range(4)) #self.locations is still a dictonary
        #team.money += round_income #team.money changed from team["money"]

        # Reset entries for next team
        for entry in self.elf_entries:
            entry.delete(0, tk.END)
            entry.insert(0, "0")

        # Move to next team or next turn
        self.current_team_idx += 1
        if self.current_team_idx >= self.num_teams:

            #show rewards 
            self.rewards()

            #reset for the next turn
            self.current_team_idx = 0
            self.current_turn += 1
            messagebox.showinfo("New Round", f"Round {self.current_turn} begins!")

        self.refresh_ui()


    #SNOW
    #https://www.tutorialspoint.com/article/how-to-clear-tkinter-canvas#:~:text=In%20order%20to%20clear%20a,present%20in%20a%20Tkinter%20frame. 
    #https://stackoverflow.com/questions/45388420/python-3-tkinter-how-to-use-after-on-canvas-graphics 
    def moveSnow(self):
        for particile in self.snowList: 
            self.canvas.move(particile, 0, 1) #makes the y coordinate of particle decrease by 1

            #x1, y1, x2, y2 = self.canvas.coords(particile)

        self.root.after(33, self.moveSnow) #async (keeps this function running every .3) but lets the game continue

    def stopSnow(self): #deletes all the snow
        for snow in self.snowList: 
            self.canvas.delete(snow) #deletes the snow from the canvas
        self.snowList.clear() #clears the list
        self.canvas.destroy() #destroys the canvas (the background)

    def makeSnow(self):

        self.canvas = tk.Canvas(self.root, width=700, height=600, bg='Black') #BROKEN ===================================== doesnt fully cover the screen
        self.canvas.pack() #display the canvas

        self.snowList = []
        for _ in range(50):
            x = random.randint(0,700)
            y = random.randint(0,500)
            size = 5

            snow = self.canvas.create_rectangle(x, y, x + size, y + size, fill='white', outline='') #ceate rectangles for snow

            self.snowList.append(snow) #add it to the list
        
        self.moveSnow() #call the move snow func once, thought it runs async

        self.root.after(4000, self.stopSnow) #after like 3 seconds it calls stop snow which deletes everthting
        




    def rewards(self, snowStorm: bool=True): #process the money, maybe show a graphic of a snow storm etc so its all together at the end

        if snowStorm: #only runs if there is a snowstorm
            self.makeSnow()

        for team in self.teams_data: #for each team
            totalInc = 0

            for loc in self.locations: #get the name and the amount of money
                location = loc["name"]
                reward = loc["payout"]

                elvesSent = team.sentElves.get(location) #get how many elves sent to each location

                if snowStorm and location == "Deep Forrest":
                    totalInc += 0

                elif snowStorm and location == "Mountains":
                    totalInc += 0
                    team.elves -= elvesSent

                else:
                    totalInc += elvesSent * reward
            
            team.money += totalInc








if __name__ == "__main__":
    root = tk.Tk()
    app = ElfGame(root)
    root.mainloop()
