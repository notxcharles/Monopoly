from board_info.spaces import spaces
from board_info.properties import properties
import config
import random
import matplotlib
import cssutils
from termcolor import cprint
from bs4 import BeautifulSoup

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


def playerGoToJail(player):
    # Player in jail
    # When a player goes to jail:
    # goes straight to jail (rather than passing over spaces)
    # Has three turns to get out (must roll doubles)
    # If hasnt rolled doubles in 3 turns they must pay M50
    player["in_jail"] = True
    player["doubles_rolled_streak"] = 0
    player["turns_left_jail"] = 3
    player["current_position"] = 10.5
    print("IN JAIL", player["player"])
    return player


def rollDice():
    # Return rolls and if player rolled double
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)

    if dice1 == dice2:
        print("rollDice returns ", (dice1 + dice2), " Double")
        return (dice1 + dice2), True
    else:
        print("rollDice returns ", (dice1 + dice2))
        return (dice1 + dice2), False


def logSpaceFinishedTurnOn(currentPosition):
    for space in spaces:
        if space["position"] == currentPosition:
            space["landed_on"] += 1
    # print("log ", spaces)


def playerAction(player):
    diceRoll, rolledDoubles = rollDice()
    if player["in_jail"] == True:
        # Players in jail, so they either need to roll double or pay to get out.
        if player["turns_left_jail"] > 0:
            if rolledDoubles == True:
                # Can leave jail
                player["doubles_rolled_streak"] = 1
                player["in_jail"] = False
                player["turns_left_jail"] = 0
                # Change position to change as jail is position is set as 10.5
                player["current_position"] = 10
                player["current_position"] += diceRoll
                logSpaceFinishedTurnOn(player["current_position"])
                # Rolled a double so entitled to another go
                playerAction(player)
                return player
            else:
                player["doubles_rolled_streak"] = 0
                player["turns_left_jail"] -= 1
                logSpaceFinishedTurnOn(player["current_position"])
        else:
            # Player can just leave jail for M50 fee
            player["balance"] -= 50
            # Change position to change as jail is position is set as 10.5
            player["in_jail"] = False
            player["doubles_rolled_streak"] = 0
            player["current_position"] = 10
            player["current_position"] += diceRoll
            logSpaceFinishedTurnOn(player["current_position"])
            return player

    else:
        # Else player continues as normal, if they roll 3 doubles they go to jail
        if rolledDoubles == True:
            player["doubles_rolled_streak"] += 1
            if player["doubles_rolled_streak"] == 3:
                # Go to jail and end turn
                player = playerGoToJail(player)
                print("Rolled 3 doubles, in jail", player["current_position"])
                logSpaceFinishedTurnOn(player["current_position"])
                return player
            else:
                player["current_position"] += diceRoll
                if player["current_position"] == 30:  # Go to jail
                    player = playerGoToJail(player)
                    logSpaceFinishedTurnOn(player["current_position"])
                    return player
                # Board has 40 positions 0-39, if player rolls eg 6 whilst in position 39, their new positon = 45, should be 5
                if player["current_position"] >= 40:
                    player["current_position"] -= 40
                logSpaceFinishedTurnOn(player["current_position"])
                # Player entitled to another go
                playerAction(player)
                return player
        else:
            print("this code was run")
            player["doubles_rolled_streak"] = 0
            player["current_position"] += diceRoll
            if player["current_position"] == 30:  # Go to jail
                player = playerGoToJail(player)
                logSpaceFinishedTurnOn(player["current_position"])
                return player
            # Board has 40 positions 0-39, if player rolls eg 6 whilst in position 39, their new positon = 45, should be 5
            if player["current_position"] >= 40:
                player["current_position"] -= 40
            logSpaceFinishedTurnOn(player["current_position"])
            return player


def displayHTML(spaces):
    # Get the stats of what percentage of turns resulted on landing on x space
    completeSpaces = spaces

    for cs in completeSpaces:
        landed_on = cs["landed_on"]
        total_turns = config.turnsPerPlayer * config.numberOfPlayers
        cs["landed_on_chance_fraction"] = str(int(landed_on)) + "/" + str(total_turns)
        cs["landed_on_percentage"] = round(landed_on / total_turns * 100, 3)
    print("cs: ", completeSpaces)
    # Normalise data (0-1)
    list = []

    if not config.displayJail:
        spaces = [i for i in spaces if not (i["name"] == "Jail")]
    if not config.displayGoToJail:
        spaces = [i for i in spaces if not (i["name"] == "Go To Jail")]
    if not config.displayChance:
        spaces = [i for i in spaces if not (i["name"] == "Chance")]
    if not config.displayCommunityChest:
        spaces = [i for i in spaces if not (i["name"] == "Community Chest")]

    for space in spaces:
        list.append(space["landed_on"])

    xmin = min(list)
    xmax = max(list)
    print(xmin)
    print(xmax)
    for i, x in enumerate(list):
        list[i] = (x - xmin) / (xmax - xmin)

    # Find corresponding cmap color for normalised value
    # cmap = matplotlib.cm.get_cmap("cividis_r")
    cmap = matplotlib.cm.get_cmap("summer_r")
    print("normalized data: ", list, " ", len(list))
    print("spaces ", len(spaces))
    for id, space in enumerate(spaces):
        rgba = cmap(list[id])
        hexcolor = matplotlib.colors.rgb2hex(rgba)
        space["landed_on_normalised"] = list[id]
        space["hexcolor"] = hexcolor

    # Change CSS
    parser = cssutils.parseFile("stats.css")
    for rule in parser.cssRules:
        for space in spaces:
            id = "#position" + str(space["position"])

            if "." in id:
                id = id.replace(".", "")
            try:
                if rule.selectorText == id:
                    rule.style.backgroundColor = space["hexcolor"]
            except AttributeError as e:
                pass

    # Write to new css file for html to read
    with open("style_new.css", "wb") as f:
        f.write(parser.cssText)

    # Alter HTML to show percentage stats on mouseover

    with open("monopoly2.html", "r") as file:
        soup = BeautifulSoup(file, "html.parser")
        for space in completeSpaces:
            id = "position" + str(space["position"])

            if "." in id:
                id = id.replace(".", "")

            div = soup.find("div", {"id": id})
            if div != None:
                for s in completeSpaces:
                    if s["position"] == space["position"]:
                        title_name = s["name"]
                        title_percent = str(s["landed_on_percentage"])
                        title_fraction = s["landed_on_chance_fraction"]
                        title = (
                            title_name
                            + "\nPercentage: "
                            + title_percent
                            + "%\nFraction: "
                            + title_fraction
                        )
                        div["title"] = title

    with open("monopoly2.html", "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))


def playGame():
    initialiseGame(config)
    # print(player_stats)
    for turn in range(config.turnsPerPlayer):
        for x in range(config.numberOfPlayers):
            playerActionReturn = playerAction(player_stats[x])
            if player_stats[x]["player"] == 0:
                cprint(player_stats[x], "red")
            elif player_stats[x]["player"] == 1:
                cprint(player_stats[x], "green")
            elif player_stats[x]["player"] == 2:
                cprint(player_stats[x], "blue")
            elif player_stats[x]["player"] == 3:
                cprint(player_stats[x], "yellow")
            else:
                print(player_stats[x])
            # print(x, " moved, turn ", turn, " pos ", pos)
            player_stats[x]["turns"] += 1

    # Game Complete
    print("\n\n Game Complete:")
    for space in spaces:
        print(space)
    print("\n Players Stats: ")
    for player in player_stats:
        print(player)

    displayHTML(spaces)


playGame()
