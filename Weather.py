import random

class Day:
    def __init__(self):
        self.currentDay = 0
        self.lastWeather = None
        self.minimumDays = {} #min days for each location
        self.currentWeather = None
        self.weathers = [ #weather, probability of blizzard and prompt to be displayed
            {"name": "promising", "probability": 0.2, "prompt": "The weather is looking promising!"},
            {"name": "okay", "probability": 0.25, "prompt": "The weather is looking okay."},
            {"name": "hopeful", "probability": 0.15, "prompt": "The weather is looking hopeful."},
            {"name": "dreary", "probability": 0.55, "prompt": "The weather is looking dreary..."},
            {"name": "mixed", "probability": 0.5, "prompt": "The weather is looking mixed."},
            {"name": "uncertain", "probability": 0.5, "prompt": "The weather is looking uncertain..."},
            {"name": "treacherous", "probability": 0.75, "prompt": "The weather is looking treacherous..."}
        ]

    def selectNewWeather(self): #just chooses a random weather time
        self.currentWeather = random.choice(self.weathers)['name']

    def enterNextDay(self): #updates day count -> can update labels in main based on this
        self.currentDay += 1
        self.lastWeather = self.currentWeather
        self.selectNewWeather()

    def determineBlizzard(self): #logic function determining weather outcome
        #check last weather
        #determine if series of luck or unlucky
        #tweak result probability
        #increase until ie 90% blizzard chance if example 14 non in a row
        #return outcome dependent on blizzard or not - blizzard = true, non = false
        pass

    


    
