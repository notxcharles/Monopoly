from unittest import defaultTestLoader
from board_info.spaces import spaces
from board_info.properties import properties
import config
import random

player_stats = []


def initialiseGame(cfg):
    for x in range(cfg.numberOfPlayers):
        player = {
            "player": int(x),
            "current_position": float(0),
            "balance": int(cfg.startingBalance),
            "doubles_rolled_streak": int(0),
            "turns": int(0),
            "in_jail": False,
            "turns_left_jail": int(0),
        }
        player_stats.append(player)
    return


def rollDice():
    # Return rolls and if player rolled double
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    print("rollDice returns ", (dice1 + dice2))
    if dice1 == dice2:
        return (dice1 + dice2), True  # Ignoring '3 doubles = jail' for now
    else:
        return (dice1 + dice2), False


def logSpaceLandedOn(currentPosition):
    for space in spaces:
        if space["position"] == currentPosition:
            space["landed_on"] += 1
    # print("log ", spaces)


def playerMove(player, diceRoll, jail=False):
    currentPosition = player["current_position"]
    currentPosition += diceRoll
    # Board has 40 positions 0-39, if player rolls eg 6 whilst in position 39, their new positon = 45, should be 5
    if currentPosition >= 40:
        currentPosition -= 40
    print("playerMove returns ", currentPosition)
    logSpaceLandedOn(currentPosition)
    return currentPosition


def playerAction(player):
    diceRoll, rolledDoubles = rollDice()
    newPosition = playerMove(player, diceRoll)

    player["current_position"] = newPosition

    print("playerAction returns ", player)
    return player


def playGame():
    initialiseGame(config)
    # print(player_stats)
    for turn in range(config.turnsPerPlayer):
        for x in range(config.numberOfPlayers):
            a = playerAction(player_stats[x])
            print(player_stats[x])
            # print(x, " moved, turn ", turn, " pos ", pos)
    print("\n\n Game Complete: ", spaces)
    print("\n Players Stats: ", player_stats)


playGame()
