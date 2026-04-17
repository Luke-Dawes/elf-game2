class Day:
    def __init__():
        Day.currentDay = 0
        Day.currentWeather = None
        Day.weatherProbabilities = { #weather name and associated probability of blizzard
            "promising" : 0.25,
            "clear" : 0.2,
            "hopeful" : 0.3,
            "mixed" : 0.5,
            "dreary" : 0.5,
            "treacherous" : 0.6,
            "okay" : 0.25
        }
