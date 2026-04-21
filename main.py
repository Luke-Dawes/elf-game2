import tkinter as tk
from tkinter import messagebox
from TeamClass import Team
import random


"""
left to do for the base game:
    information when you start the game explaning everything
    weather in the main loop
    shop
    some end to the game
    random events i.e. random elves moving

ideas left to do:
    map/background image when looking if its a snowstorm or not? 
    screenshake creating anticipation for if its a snowstorm or not
    taxes?
    comback mechanics - however might not be as clear as whos going to win bc motivation

"""


class ElfGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Elf Game 2")
        self.root.geometry("700x600")

        # Game State
        self.current_turn = 1
        self.current_team_idx = 0
        self.num_teams = 4

        self.waitingForName = tk.BooleanVar(value=False)
        self.payedToElves = 0

        #snow
        self.snowList = []
        
        # Location Multipliers (Money earned per elf)
        self.locations = [
            {"name": "Woods", "payout": 10},
            {"name": "Deep Forest", "payout": 25}
            #{"name": "Mountains", "payout": 50},
            #{"name": "Mystic Cave", "payout": 100}
        ]

        # Team Data: [Money, Total Elves]
        #self.teams_data = [Team(f"Team {i+1}") for i in range(4)] #this is now a list of teams
        #self.teams_data = [{"money": 0, "elves": 10, "name": f"Team {i+1}"} for i in range(4)]
        self.teams_data = []
        
        self.createTeams()
        self.root.wait_variable(self.waitingForName) #a hold vairable so tkinter runs and allows input

        self.create_widgets()
        self.refresh_ui()

    #def createTeamsSeperateWindow(self): #added func to add a name
    #    for i in range(1,5):
    #        while True: #handle for None 
    #            temp = simpledialog.askstring("Name", f"What is the name of team {i}") 
    #            if temp:
    #                break
    #        self.teams_data.append(Team(temp))

    def createTeams(self): #code from website
        self.frame = tk.Frame(self.root) #get the frame
        self.frame.pack(pady=50) #add it to the screen
        tk.Label(self.frame, text="Enter Team Names", font=("Arial", 14, "bold")).pack(pady=10) #add a lavel for a title
        self.names = [] #add temp names

        for i in range(4): #4
            f = tk.Frame(self.frame) #i guess we assign self.frame to f
            f.pack() #pack it?
            tk.Label(f, text=f"Team {i+1}:").pack(side="left") 
            ent = tk.Entry(f) #input
            ent.insert(0, f"Team {i+1}") #whats in the box
            ent.pack(side="left", padx=5)
            self.names.append(ent) #add it to the thing
        btn = tk.Button(self.frame, text="Start Game", command=self.saveTeamsAndStart) #on press run saveTeamsAndStart
        btn.pack(pady=20)

    def saveTeamsAndStart(self):
        for name in self.names:
            teamName = name.get().strip() or "unknwon"
            self.teams_data.append(Team(teamName))
        
        self.frame.destroy()
        self.waitingForName.set(True)



    def create_widgets(self) -> None:
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
            tk.Label(self.input_frame, text=f"{loc['name']} (£{loc['payout']}/elf):").grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(self.input_frame, width=10)
            entry.insert(0, "0")
            entry.grid(row=i, column=1, padx=10)
            self.elf_entries.append(entry)

        tk.Label(self.input_frame, text="Pay Elves (£)").grid(row=5, column=0, sticky='w',pady=5)
        self.payEntry = tk.Entry(self.input_frame, width=10)
        self.payEntry.insert(0, "0")
        self.payEntry.grid(row=5, column=1, padx=10)

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

    def refresh_ui(self) -> None:
        team = self.teams_data[self.current_team_idx]
        self.header_label.config(text=f"Turn {self.current_turn}: {team.name}'s Move") #instead of using team["name"] its now a class syntax
        self.team_info_label.config(text=f"Available Elves: {team.elves} | Current Money: £{team.money}") #changed here aswell
        
        for i, lbl in enumerate(self.leaderboard_labels):
            t = self.teams_data[i]
            lbl.config(text=f"{t.name}\nMoney: £{t.money}\nElves: {t.elves}\nElf Motivation: {t.motivation * 50}%") #as well as here

    def process_turn(self) -> None:
        team = self.teams_data[self.current_team_idx]
        try:
            allocations = [int(e.get()) for e in self.elf_entries]
            paying = int(self.payEntry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return

        if paying > team.money:
            messagebox.showwarning("Warning", "Not enough money to pay elves!")
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

        team.payed = paying
        

        #!delayed this untill the end so it calculates it all together  
        #round_income = sum(allocations[i] * self.locations[i]["payout"] for i in range(4)) #self.locations is still a dictonary
        #team.money += round_income #team.money changed from team["money"]

        # Reset entries for next team
        for entry in self.elf_entries:
            entry.delete(0, tk.END)
            entry.insert(0, "0")

        self.payEntry.delete(0, tk.END)
        self.payEntry.insert(0, "0")
        

        # Move to next team or next turn
        self.current_team_idx += 1
        if self.current_team_idx >= self.num_teams:

            #show rewards 
            
            for team in self.teams_data:
                team.money -= team.payed
                team.motivation += team.payed * 0.0005

            self.rewards()

            #reset for the next turn
            self.current_team_idx = 0
            self.current_turn += 1

            if self.current_turn == 7:
                self.locations.append({"name": "Mountains", "payout": 50})
                self.deleteWidgets()
                self.create_widgets()
                
            
            elif self.current_turn == 14:
                self.locations.append({"name": "Volcano", "payout": 100})
                self.deleteWidgets()
                self.create_widgets()
                
        self.refresh_ui()


    #SNOW
    def moveSnow(self) -> None:
        for particile in self.snowList: 
            self.canvas.move(particile, 0, 1) #makes the y coordinate of particle decrease by 1
            
        self.root.after(33, self.moveSnow) #async (keeps this function running every .3) but lets the game continue

    def stopSnow(self) -> None: #deletes all the snow
        for snow in self.snowList: 
            self.canvas.delete(snow) #deletes the snow from the canvas
        self.snowList.clear() #clears the list
        self.canvas.destroy() #destroys the canvas (the background)

    def makeSnow(self) -> None:

        self.canvas = tk.Canvas(self.root, width=700, height=600, bg='Black') 
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
        self.root.after(4005, self.create_widgets) #create the widgets again which have been deleted
        self.root.after(4006, self.refresh_ui) #refresh them so they contain the correct data
        

    def deleteWidgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def rewards(self, snowStorm: bool=True) -> None: #process the money, maybe show a graphic of a snow storm etc so its all together at the end

        if snowStorm: #only runs if there is a snowstorm
            self.deleteWidgets() 
            self.makeSnow()

        rewardMessage = ""

        for team in self.teams_data: #for each team
            totalInc = 0

            for loc in self.locations: #get the name and the amount of money
                tempInc = 0
                location = loc["name"]
                reward = loc["payout"]

                elvesSent = team.sentElves.get(location) #get how many elves sent to each location

                if snowStorm and location == "Deep Forest":
                    tempInc += 0

                elif snowStorm and location == "Mountains":
                    tempInc += 0
                    team.elves -= elvesSent

                elif not snowStorm and location == "Volcano":
                    team.elves -= elvesSent
                    tempInc += 0

                else:
                    tempInc += elvesSent * reward
                
                if loc == "Mountains" and snowStorm:
                    rewardMessage += f"☆ {team.name} sent {elvesSent} to {location} and lost all of them! ☆ \n"

                elif loc == "Volcano" and not snowStorm:
                    rewardMessage += f"☆ {team.name} sent {elvesSent} to {location} and lost all of them! ☆ \n"

                else:
                    rewardMessage += f"☆ {team.name} sent {elvesSent} to {location} and earned £{tempInc} ☆ \n"
                
                totalInc += tempInc
                

            
            team.money += totalInc

            if team.motivation >= 2:
                valueFromMotivation = max(1, min(team.motivation, 5))
                percent = valueFromMotivation * 0.1
                team.money += int(team.money * percent)

                rewardMessage += f"☆☆ {team.name} earned £{int(team.money * percent)} via extra work from their elves ☆☆"

            rewardMessage += "\n"
        
        messagebox.showinfo("rewards", rewardMessage)








if __name__ == "__main__":
    root = tk.Tk()
    app = ElfGame(root)
    root.mainloop()
