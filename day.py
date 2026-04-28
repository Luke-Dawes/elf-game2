import random
import tkinter as tk


class Day:
    def __init__(self):

        # ==WEATHER== 

        self.current_day = 0
        self.last_weather = None
        self.minimum_days = {}  # min days for each location
        self.current_weather = None
        self.concurrent_sun = 0
        self.last_blizzard = False
        self.weathers = [  # weather, probability of blizzard and prompt to be displayed
            {"name": "hopeful", "probability": 0.1, "prompt": "☀️☀️☀️ The weather is looking great! ☀️☀️☀️"},
            {"name": "promising", "probability": 0.2, "prompt": "🌤️🌤️🌤️ The weather is looking promising! 🌤️🌤️🌤️"},
            {"name": "okay", "probability": 0.3, "prompt": "⛅⛅⛅ The weather is looking okay. ⛅⛅⛅"},
            {"name": "mixed", "probability": 0.4, "prompt": "🌥️🌥️🌥️ The weather is looking mixed. 🌥️🌥️🌥️"},
            {"name": "uncertain", "probability": 0.5, "prompt": "☁️☁️☁️ The weather is looking uncertain... ☁️☁️☁️"},
            {"name": "dreary", "probability": 0.6, "prompt": "🌦️🌦️🌦️ The weather is looking dreary... 🌦️🌦️🌦️"},
            {"name": "treacherous", "probability": 0.8, "prompt": "⛈️⛈️⛈️ The weather is looking treacherous... ⛈️⛈️️⛈️"}
        ]

        # ==EVENTS==

        self.days_since_event = 0
        self.events = [
            {"name": "elf_workshop" , "probability": 0.5, "prompt": " ☆ You have been approached by Santa Claus, who is selling off his elves! ☆ \nHow many will you buy? (£80)"},
            {"name": "mysterious_stranger", "probability": 0.2, "prompt": "☆ A mysterious stranger has appeared at the factory... ☆"},
            {"name": "elf_migration", "probability": 0.2, "prompt": "☆ Due to the working conditions, an elf has wandered off... ☆"},
            {"name": "elf_strike" , "probability": 0.2, "prompt": " ☆ The elves have decided to go on strike... ☆ "}, #add label new line stating who this has affected
            {"name": "no_event", "probability": 1.0, "prompt": "No events are happening today."}
        ]
        self.current_event = self.events[-1] #last index since this is will ALWAYS be no event (default case)
        self.activated_button_in_turn = False

        # ==METHODS==
    
    def probability_generator(self, chance):
        print(f"Chance of success is: {chance}")
        test = random.random()
        print(test)
        return (test < chance)

    def select_new_weather(self):  # just chooses a random weather
        self.current_weather = random.choice(self.weathers)

    def increment_day(self):  # updates day count -> can update labels in main based on this
        self.current_day += 1
        self.last_weather = self.current_weather
        self.select_new_weather()

    def determine_blizzard(self):  # logic function determining weather outcome

        chance = self.current_weather["probability"]
        
        if self.last_blizzard:
            self.concurrent_sun = 0
        else:
            self.concurrent_sun += 1
            chance += ((self.concurrent_sun - 1) * 0.1)

        if self.current_day > 8: chance *= 1.05    
        if chance > 0.9: chance = 0.9

        return self.probability_generator(chance=chance)
    
    def calculate_event_chance(self):
        pass

    def select_new_event(self):
        for event in self.events:
            if self.probability_generator(event["probability"]):
                self.current_event = event
                break
        

    # ==EVENT HANDLERS==

    def event_runner(self, events_box, team_data):
        
        self.local_team_data = team_data
        print("inside event runner", self.local_team_data)
        self.local_events_box = events_box
        self.current_team_index = 0

        event_name_to_function_map = {
            "elf_workshop": self.elf_workshop,
            "mysterious_stranger": self.mysterious_stranger,
            "elf_migration": self.elf_migration,
            "elf_strike": self.elf_strike,
            "no_event": self.no_event,
        }
        try:
            return event_name_to_function_map[self.current_event['name']]()
        except TypeError:
            pass

    def elf_workshop(self):
        # ==ENTRY BOXES==
        
        self.input_box = tk.Entry(self.local_events_box)
        self.input_box.pack(padx=10, pady=10)
        self.input_box.insert(0,"0")

        self.submit_event_button = tk.Button(self.local_events_box, command= self.elf_workshop_functioning, width=10, height=1, bg="green", text="PURCHASE", font=("Arial", 12, "bold"), fg="white")
        self.submit_event_button.pack(padx=10, pady=10)

        return self.local_team_data

        # ==PROCESSING==

    def elf_workshop_functioning(self):
        #update team stuff
        if self.submit_event_button.cget("state") != "disabled" and not self.activated_button_in_turn:
            self.submit_event_button.config(state="disabled")
            team_max_team_money = self.local_team_data[self.current_team_index].money
            print(f"£{team_max_team_money}")
            no_elves = int(self.input_box.get())
            self.activated_button_in_turn = True
        
        else:
            self.submit_event_button.config(state="normal")
            self.activated_button_in_turn = False
            self.current_team_index += 1



    def mysterious_stranger(self):
        print('run event')
        return self.local_team_data

    def elf_migration(self):
        print('run event')
        return self.local_team_data

    def elf_strike(self):
        print('run event')
        return self.local_team_data

    def no_event(self, **kwargs):
        return self.local_team_data

    
    


    
