import tkinter as tk

from tkinter import messagebox
from tkinter import ttk

from team import Team
from weather import Day
from animation import SnowAnimation


"""
left to do for the base game:
    information when you start the game explaining everything
    weather in the main loop                                            -- added processing of weather 
    shop
    some end to the game
    random events i.e. random elves moving

ideas left to do:
    map/background image when looking if its a snowstorm or not?                --good plan how to implement though?
    screen-shake creating anticipation for if its a snowstorm or not
    taxes?
    come-back mechanics - however might not be as clear as who's going to win bc motivation

"""


class ElfGame:
    def __init__(self, root):
        self.setup_elves_flag = False
        self.root = root
        self.root.title("Elf Game 2")
        self.root.geometry("700x600")

        # Game State
        self.current_turn = 1
        self.current_team_idx = 0
        self.num_teams = 4

        self.waiting_for_name = tk.BooleanVar(value=False)
        self.day = Day()
        self.day.increment_day()

        #snow
        self.snow_list = []
        self.is_blizzard_done = tk.BooleanVar(value=True)
        
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
        
        self.create_teams()
        self.root.wait_variable(self.waiting_for_name) #a hold variable so tkinter runs and allows input

        self.create_widgets()
        self.refresh_ui()

    #def createTeamsSeperateWindow(self): #added func to add a name
    #    for i in range(1,5):
    #        while True: #handle for None 
    #            temp = simpledialog.askstring("Name", f"What is the name of team {i}") 
    #            if temp:
    #                break
    #        self.teams_data.append(Team(temp))

    def create_teams(self): #code from website
        self.frame = tk.Frame(self.root) #get the frame
        self.frame.pack(pady=50) #add it to the screen
        tk.Label(self.frame, text="Enter Team Names", font=("Arial", 14, "bold")).pack(pady=10) #add a label for a title
        self.names = [] #add temp names

        for i in range(4): #4
            f = tk.Frame(self.frame) #I guess we assign self.frame to f
            f.pack() #pack it?
            tk.Label(f, text=f"Team {i+1}:").pack(side="left") 
            ent = tk.Entry(f) #input
            ent.insert(0, f"Team {i+1}") #what's in the box
            ent.pack(side="left", padx=5)
            self.names.append(ent) #add it to the thing
        btn = tk.Button(self.frame, text="Start Game", command=self.save_teams_and_start) #on press run saveTeamsAndStart
        btn.pack(pady=20)

    def save_teams_and_start(self):
        for name in self.names:
            teamName = name.get().strip() or "unknown"
            self.teams_data.append(Team(teamName))
        
        self.frame.destroy()
        self.waiting_for_name.set(True)



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
            self.current_elves = tk.IntVar(self.root)
            entry = ttk.Combobox(self.input_frame, width=10, textvariable=self.current_elves)
            #entry.insert(0, "0")
            entry.grid(row=i, column=1, padx=10)
            entry.bind("<FocusIn>", self.update_remaining_elves_event)
            self.elf_entries.append(entry)

        tk.Label(self.input_frame, text="Pay Elves (£)").grid(row=5, column=0, sticky='w',pady=5)
        self.pay_entry = tk.Entry(master= self.input_frame, width=10,)
        self.pay_entry.insert(0, "0")
        self.pay_entry.grid(row=5, column=1, padx=10)

        # Submit Button
        self.submit_btn = tk.Button(self.root, text="Confirm Turn", command=self.process_turn, bg="green", fg="white", font=("Arial", 12, "bold"))
        self.submit_btn.pack(pady=10)

        # Weather
        self.weather_display = tk.LabelFrame(self.root, text= "Weather", padx=10, pady=10)
        self.weather_display.pack(fill="both", padx=20, pady=20)

        self.weather_prompt = tk.Label(self.weather_display, text=self.day.current_weather["prompt"])
        self.weather_prompt.pack(fill="both")

        # Leaderboard
        self.leaderboard_frame = tk.LabelFrame(self.root, text="Leaderboard", padx=10, pady=10)
        self.leaderboard_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        
        self.leaderboard_labels = []
        for i in range(4):
            lbl = tk.Label(self.leaderboard_frame, text="")
            lbl.pack(side="left", expand=True)
            self.leaderboard_labels.append(lbl)


    def update_remaining_elves_event(self,event):
        self.update_remaining_elves()

    def update_remaining_elves(self):
        team = self.teams_data[self.current_team_idx]
        elves_left = team.elves
        for entries in self.elf_entries:
            if not self.setup_elves_flag: 
                entries.current(0)
                self.setup_elves_flag = True
            current_input = int(entries.get())
            elves_left -= current_input
            self.setup_elf_options(elves_left, current_input)

    def setup_elf_options(self,elves_left,current_input):
        for i, drop in enumerate(self.elf_entries):
            self.valuesInDrop = [elves for elves in range(0,elves_left+current_input+1)]
            print(self.valuesInDrop)
            drop.config(values = self.valuesInDrop)    
            
    def refresh_ui(self) -> None:
        if self.current_team_idx <= self.num_teams:   team = self.teams_data[self.current_team_idx]

        self.header_label.config(text=f"Turn {self.current_turn}: {team.name}'s Move") #instead of using team["name"] it's now a class syntax
        self.team_info_label.config(text=f"Available Elves: {team.elves} | Current Money: £{team.money}") #changed here as well


        self.setup_elf_options(team.elves, 0) 
        self.update_remaining_elves()

        self.weather_display.config(text="Weather")

        for i, lbl in enumerate(self.leaderboard_labels):
            t = self.teams_data[i]
            lbl.config(text=f"{t.name}\nMoney: £{t.money}\nElves: {t.elves}\nElf Motivation: {t.motivation * 50}%") #as well as here

    def process_turn(self) -> None:
        team = self.teams_data[self.current_team_idx]

        # ===== PROCESS INPUTS =====
        try:
            allocations = [int(e.get()) for e in self.elf_entries]
            paying = int(self.pay_entry.get())
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

        # ===== PROCESS LOGIC =====
        team.sent_elves = {  # document which elves where, for calculating earnings
            self.locations[i]["name"]: allocations[i]
            for i in range(len(self.locations))
        }

        team.payed = paying

        #!delayed this until the end so it calculates it all together
        #round_income = sum(allocations[i] * self.locations[i]["payout"] for i in range(4)) #self.locations is still a dictionary
        #team.money += round_income #team.money changed from team["money"]

        # Reset entries for next team
        for entry in self.elf_entries:
            entry.delete(0, tk.END)
            entry.insert(0, "0")

        self.pay_entry.delete(0, tk.END)
        self.pay_entry.insert(0, "0")

        # Move to next team or next turn
        self.current_team_idx += 1
        print(self.day.current_weather)

        if self.current_team_idx >= self.num_teams:
            
            #show rewards
            for team in self.teams_data:
                team.money -= team.payed
                team.motivation += team.payed * 0.0005

            self.current_team_idx = 0
            self.current_turn += 1

            self.blizzard_happended = self.day.determine_blizzard()

            if not self.blizzard_happended:
                self.is_blizzard_done.set(True)

            self.rewards(self.blizzard_happended)
            
            if self.blizzard_happended:
                self.root.wait_variable(self.is_blizzard_done)

            #reset for the next turn
            self.day.increment_day()  # increment day for each new turn

            self.weather_prompt.destroy() #weather wasnt updating unless its destroyed and remade
            self.weather_prompt = tk.Label(self.weather_display, text=self.day.current_weather["prompt"]) #removing destroy just adds new labels
            self.weather_prompt.pack(fill="both")

            if self.current_turn == 7:
                self.locations.append({"name": "Mountains", "payout": 50})
                self.delete_widgets()
                self.create_widgets()

            elif self.current_turn == 14:
                self.locations.append({"name": "Volcano", "payout": 100})
                self.delete_widgets()
                self.create_widgets()
                
        self.refresh_ui()

    def blizzard_done(self):
        self.is_blizzard_done.set(True)

    def delete_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def rewards(self, snowStorm: bool) -> None:
        # process the money, maybe show a graphic of a snow storm etc. so it's all together at the end
        # snowStorm = True if self.current_turn == 7 else False

        if snowStorm:  # only runs if there is a snowstorm
            self.process_snowstorm()

        rewardMessage = ""

        for team in self.teams_data: #for each team
            totalInc = 0

            for loc in self.locations: #get the name and the amount of money
                tempInc = 0
                location = loc["name"]
                reward = loc["payout"]

                elvesSent = team.sent_elves.get(location) #get how many elves sent to each location

                # calculate money
                if snowStorm and location == "Deep Forest":
                    pass
                elif snowStorm and location == "Mountains":
                    team.elves -= elvesSent
                elif not snowStorm and location == "Volcano":
                    team.elves -= elvesSent
                else:
                    tempInc += elvesSent * reward

                # confirm what happened to elves
                if location == "Mountains" and snowStorm:
                    rewardMessage += f"☆ {team.name} sent {elvesSent} to {location} and lost all of them! ☆ \n"
                elif location == "Volcano" and not snowStorm:
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
        self.refresh_ui()

    def process_snowstorm(self):
        self.is_blizzard_done.set(False)
        self.delete_widgets()

        animation = SnowAnimation(self.root)
        animation.play()
        self.is_blizzard_done.set(True)

        self.day.last_blizzard = True  # resets luck meter
        self.create_widgets()
        self.refresh_ui()


if __name__ == "__main__":
    root = tk.Tk()
    app = ElfGame(root)
    root.mainloop()
