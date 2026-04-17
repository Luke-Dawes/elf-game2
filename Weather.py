class Day:
    def __init__():
        Day.currentDay = 0
        Day.currentWeather = None
        Day.weathers = [
            {name: "promising", probability: 0.2, prompt: "The weather is looking promising!"},
            {name: "okay", probability: 0.25, prompt: "The weather is looking okay."},
            {name: "hopeful", probability: 0.15, prompt: "The weather is looking hopeful."},
            {name: "dreary", probability: 0.55, prompt: "The weather is looking dreary..."},
            {name: "mixed", probability: 0.5, prompt: "The weather is looking mixed."},
            {name: "uncertain", probability: 0.5, prompt: "The weather is looking uncertain..."},
            {name: "treacherous", probability: 0.75, prompt: "The weather is looking treacherous..."}
        ]
