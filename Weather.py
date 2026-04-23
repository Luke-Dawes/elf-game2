import random

class Day:
    def __init__(self):
        self.currentDay = 0
        self.lastWeather = None
        self.minimumDays = {} #min days for each location
        self.currentWeather = None
        self.concurrentSun = 0
        self.lastBlizzard = False
        self.weathers = [ #weather, probability of blizzard and prompt to be displayed
            {"name": "promising", "probability": 0.2, "prompt": "The weather is looking promising!"},
            {"name": "okay", "probability": 0.25, "prompt": "The weather is looking okay."},
            {"name": "hopeful", "probability": 0.0001, "prompt": "The weather is looking hopeful."},
            {"name": "dreary", "probability": 0.55, "prompt": "The weather is looking dreary..."},
            {"name": "mixed", "probability": 0.5, "prompt": "The weather is looking mixed."},
            {"name": "uncertain", "probability": 0.5, "prompt": "The weather is looking uncertain..."},
            {"name": "treacherous", "probability": 0.75, "prompt": "The weather is looking treacherous..."}
        ]
    
    def probabilityGenerator(self, chance):
        print(f"Chance of success is: {chance}")
        test = random.random()
        print(test)
        return (test < chance)
        

    def selectNewWeather(self): #just chooses a random weather
        self.currentWeather = random.choice(self.weathers)

    def incrementDay(self): #updates day count -> can update labels in main based on this
        self.currentDay += 1
        self.lastWeather = self.currentWeather
        self.selectNewWeather()


    def determineBlizzard(self): #logic function determining weather outcome
        #check last weather
        #determine if series of luck or unlucky
        #tweak result probability
        #increase until ie 90% blizzard chance if example 14 non in a row
        #return outcome dependent on blizzard or not - blizzard = true, non = false

        chance = self.currentWeather["probability"]
        
        if self.lastBlizzard: self.concurrentSun = 0
        else: self.concurrentSun += 1 

        chance += ((self.concurrentSun - 1) * 0.1)
        if chance > 0.9: chance = 0.9

        return self.probabilityGenerator(chance=chance)


    


    
