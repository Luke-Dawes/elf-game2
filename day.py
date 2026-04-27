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
            {"name": "promising", "probability": 0.2, "prompt": "🌤️🌤️🌤️ The weather is looking promising. 🌤️🌤️🌤️"},
            {"name": "okay", "probability": 0.3, "prompt": "⛅⛅⛅ The weather is looking okay. ⛅⛅⛅"},
            {"name": "mixed", "probability": 0.4, "prompt": "🌥️🌥️🌥️ The weather is looking mixed. 🌥️🌥️🌥️"},
            {"name": "uncertain", "probability": 0.5, "prompt": "☁️☁️☁️ The weather is looking uncertain... ☁️☁️☁️"},
            {"name": "dreary", "probability": 0.6, "prompt": "🌦️🌦️🌦️ The weather is looking dreary... 🌦️🌦️🌦️"},
            {"name": "treacherous", "probability": 0.8, "prompt": "⛈️⛈️⛈️ The weather is looking treacherous... ⛈️⛈️️⛈️"}
        ]

        # ==EVENTS==

        self.days_since_event = 0
        self.events = [
            {"name": "Elf Workshop" , "prompt": " ☆ You have been approached by Santa Claus, who is selling off his elves! ☆ \nHow many will you buy?"},
            {"name": "Elf Strike" , "prompt": " ☆ The elves have decided to go on strike ☆ "}, #add label new line stating who this has affected
            {"name": "Mysterious Stranger", "prompt": "☆"}
        ]



    
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
        """
        check last weather
        determine if series of luck or unlucky
        tweak result probability
        increase until ie 90% blizzard chance if example 14 non in a row
        return outcome dependent on blizzard or not - blizzard = true, non = false
        """

        print(self.current_weather["name"], "is chosen")
        chance = self.current_weather["probability"]
        
        if self.last_blizzard:
            self.concurrent_sun = 0
        else:
            self.concurrent_sun += 1
            chance += ((self.concurrent_sun - 1) * 0.1)
            
        if chance > 0.9: chance = 0.9

        return self.probability_generator(chance=chance)
    
def calculate_shop_chance():
    pass




    


    
