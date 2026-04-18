import tkinter as tk
from tkinter import messagebox
from TeamClass import Team

class ElfGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Elf Resource Manager - Turn Based")
        self.root.geometry("700x600")

        # Game State
        self.current_turn = 1
        self.current_team_idx = 0
        self.num_teams = 4
        
        # Location Multipliers (Money earned per elf)
        self.locations = [
            {"name": "Woods", "payout": 10},
            {"name": "Deep Forest", "payout": 25},
            {"name": "Mountains", "payout": 50},
            {"name": "Mystic Cave", "payout": 100}
        ]

        # Team Data: [Money, Total Elves]
        self.teams_data = [Team(f"Team {i+1}") for i in range(4)]
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
        self.header_label.config(text=f"Turn {self.current_turn}: {team.name}'s Move")
        self.team_info_label.config(text=f"Available Elves: {team.elves} | Current Money: ${team.money}")
        
        for i, lbl in enumerate(self.leaderboard_labels):
            t = self.teams_data[i]
            lbl.config(text=f"{t.name}\nMoney: ${t.money}\nElves: {t.elves}")

    def process_turn(self):
        team = self.teams_data[self.current_team_idx]
        try:
            allocations = [int(e.get()) for e in self.elf_entries]
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return

        total_sent = sum(allocations)
        if total_sent > team.elves:
            messagebox.showwarning("Warning", f"You only have {team.elves} elves!")
            return

        # Calculate Earnings
        round_income = sum(allocations[i] * self.locations[i]["payout"] for i in range(4))
        team.money += round_income

        # Reset entries for next team
        for entry in self.elf_entries:
            entry.delete(0, tk.END)
            entry.insert(0, "0")

        # Move to next team or next turn
        self.current_team_idx += 1
        if self.current_team_idx >= self.num_teams:
            self.current_team_idx = 0
            self.current_turn += 1
            messagebox.showinfo("New Round", f"Round {self.current_turn} begins!")

        self.refresh_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = ElfGame(root)
    root.mainloop()
