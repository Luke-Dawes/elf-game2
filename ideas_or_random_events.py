import random

#already addded to the game but can be removed
"""
you decide how much you pay the elves, and if you pay them enough they will give you a % of your earnings back
(evlesPayBack function. The function isnt actually called (the maths is just in the main file), but the idea is here
"""


def tax(teams): #hurt the teams at the top more
    for team in teams:
        team.money -= team.money * 0.1 #this could underflow or go negative etc
        #deduct 10%

def ElvesPayBack(team): 
#added into the main rewards

    #would only be avalible once you reach team.motivation > 2
    #optional but once you pay them 1k? they give you compound intrest

    valueFromMotivation = max(1, min(team.motivation, 3)) #clamp between 1 and 3
    percent = valueFromMotivation * 0.1

    team.money += team.money * percent


def steal(teams, attackerIDX, defenderIDX, elvesSent):
    #send elves to sabotarge other teams instead of collecting money
    #could they steal?
    #maybe only if you have enough motivation through pay that way its only accsessable at the end
    #random chance
    
    attacker = teams[attackerIDX]
    defender = teams[defenderIDX]

    chance = random.randint(1,20)

    if elvesSent >= chance:
        amount = defender.money * 0.2
        defender.money -= amount
        attacker.money += amount
    else:
        defender.elves += elvesSent
        attacker.elves -= elvesSent


     