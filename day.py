import random

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
            {"name": "Elf Workshop" , "probability": 0.2, "prompt": " ☆ You have been approached by Santa Claus, who is selling off his elves! ☆ \nHow many will you buy?"},
            {"name": "Mysterious Stranger", "probability": 0.2, "prompt": "☆ A mysterious stranger has appeared at the factory... ☆"},
            {"name": "Elf Migration", "probability": 0.2, "prompt": "☆ Due to the working conditions, an elf has wandered off... ☆"},
            {"name": "Elf Strike" , "probability": 0.2, "prompt": " ☆ The elves have decided to go on strike... ☆ "}, #add label new line stating who this has affected
            {"name": "No Event", "probability": 1.0, "prompt": "No events are happening today."}
        ]
        self.current_event = self.events[-1] #last index since this is will ALWAYS be no event (default case)

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
            
        if chance > 0.9: chance = 0.9

        return self.probability_generator(chance=chance)
    
    def calculate_event_chance(self):
        pass

    def select_new_event(self):
        for event in self.events:
            if self.probability_generator(event["probability"]):
                self.current_event = event
                break
        




    


    
