import time

start_time = time.time()
from board_info.spaces import spaces
from board_info.properties import properties
from board_info.chance_cards import chance_cards
from board_info.community_chests import community_chests
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
            "get_out_of_jail_free_cards": int(0),
        }
        player_stats.append(player)

    random.shuffle(chance_cards)
    random.shuffle(community_chests)
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
    print("Player ", player["player"], " in jail")
    return player


def playerLeaveJail(player):
    # Player leaves jail
    # Need to change position back to 10
    player["in_jail"] = False
    player["turns_left_jail"] = 0
    player["current_position"] = 10
    return player


def chanceCard(player):
    # Check if theyve landed on a chance card
    positions = []
    for space in spaces:
        if space["name"] == "Chance":
            positions.append(space["position"])
    if player["current_position"] in positions:
        # Theyve landed on a chance square
        chance = chance_cards[0]
        # Take the card from the front place it at the back
        card = chance_cards.pop(0)
        chance_cards.append(card)
        # Positions
        position_go = 0
        position_trafalgarsquare = 24
        position_pallmall = 11
        position_stations = [5, 15, 25, 35]
        position_utilities = [12, 28]
        position_kingscrossstation = 5

        if chance["name"] == "Advance to Go (Collect £200)":
            player["current_position"] = position_go
            player["balance"] += 200
            return player

        elif (
            chance["name"]
            == "Advance to Trafalgar Square. If you pass Go, collect £200"
        ):
            if player["current_position"] > position_trafalgarsquare:
                # Player is further around the board so needs to pass go
                player["balance"] += 200
            player["current_position"] = position_trafalgarsquare
            return player

        elif chance["name"] == "Advance to Pall Mall. If you pass Go, collect £200":
            if player["current_position"] > position_pallmall:
                # Player is further around the board so needs to pass go
                player["balance"] += 200
            player["current_position"] = position_trafalgarsquare
            return player

        elif chance["name"] == "Advance to Nearest Station":
            position_stations_length = len(position_stations)
            for i in range(position_stations_length):
                if player["current_position"] < position_stations[i]:
                    player["current_position"] = position_stations[i]
                    return player

                if i == position_stations_length - 1:
                    # Need to pass go and go to position 5
                    player = playerPassedGo(player)
                    player["current_position"] = 5
                    return player

        elif chance["name"] == "Advance to Utility":
            position_utilities_length = len(position_utilities)
            for i in range(position_utilities_length):
                if player["current_position"] < position_utilities[i]:
                    player["current_position"] = position_utilities[i]

                    return player

                if i == position_utilities_length - 1:
                    # Need to pass go and go to position 12
                    player = playerPassedGo(player)
                    player["current_position"] = 12
                    return player

        elif chance["name"] == "Bank pays you dividend of £50":
            player["balance"] += 50
            return player

        elif chance["name"] == "Get Out of Jail Free":
            if player["get_out_of_jail_free_cards"] < 2:
                player["get_out_of_jail_free_cards"] += 1
            return player

        elif chance["name"] == "Go Back 3 Spaces":
            # Need to go back 3 places so not only do we need to log the position
            # but also need to do whatever action is required on the new space
            # UNFINISHED
            player["current_position"] -= 3
            return player

        elif (
            chance["name"]
            == "Go to Jail. Go directly to Jail, do not pass Go, do not collect £200"
        ):
            player = playerGoToJail(player)
            return player

        elif chance["name"] == "Speeding fine £15":
            player["balance"] -= 15
            return player

        elif (
            chance["name"]
            == "Take a trip to Kings Cross Station. If you pass Go, collect £200"
        ):
            if player["current_position"] > position_kingscrossstation:
                # Player is further around the board so needs to pass go
                player["balance"] += 200
            player["current_position"] = position_kingscrossstation
            return player

        elif (
            chance["name"]
            == "You have been elected Chairman of the Board. Pay each player £50"
        ):
            total_players = config.numberOfPlayers
            player["balance"] -= 50 * (total_players - 1)  # We don't pay ourself
            for p in player_stats:
                if p["player"] != player["player"]:
                    p["balance"] += 50
            return player

        elif chance["name"] == "Your building loan matures. Collect £150":
            player["balance"] += 150
            return player

    return player


def communityChestCard(player):
    # Check if theyve landed on a chance card
    positions = []
    for space in spaces:
        if space["name"] == "Community Chest":
            positions.append(space["position"])
    if player["current_position"] in positions:
        # Theyve landed on a community chest square
        comchest = comchest[0]
        # Take the card from the front place it at the back
        card = community_chests.pop(0)
        community_chests.append(card)
        # Positions
        position_go = 0

        if comchest["name"] == "Advance to Go (Collect £200)":
            player["current_position"] = position_go
            player["balance"] += 200
            return player

        elif comchest["name"] == "Bank error in your favour. Collect £200":
            player["balance"] += 200
            return player

        elif comchest["name"] == "Doctor's fee. Pay £50":
            player["balance"] -= 50
            return player

        elif comchest["name"] == "From sale of stock you get £50":
            player["balance"] += 50
            return player

        elif comchest["name"] == "Get out of jail free":
            if player["get_out_of_jail_free_cards"] < 2:
                player["get_out_of_jail_free_cards"] += 1
            return player

        elif (
            comchest["name"]
            == "Go to Jail. Go directly to jail, do not pass Go, do not collect £200"
        ):
            player = playerGoToJail(player)
            return player

        elif comchest["name"] == "Holiday fund matures. Recieve £100":
            player["balance"] += 100
            return player

        elif comchest["name"] == "Income tax refund. Collect £20":
            player["balance"] += 20
            return player

        elif comchest["name"] == "It is your birthday. Collect £10 from every player":
            total_players = config.numberOfPlayers
            player["balance"] += 10 * (total_players - 1)
            for p in player_stats:
                if p[player] != player["player"]:
                    p["balance"] -= 10

            return player

        elif comchest["name"] == "Life insurance matures. Collect £20":
            player["balance"] += 20
            return player

        elif comchest["name"] == "Pay hospital fees of £100":
            player["balance"] -= 100
            return player

        elif comchest["name"] == "Pay school fees of £50":
            player["balance"] -= 50
            return player

        elif comchest["name"] == "Recieve £25 consultancy fee":
            player["balance"] += 25
            return player

        elif (
            comchest["name"]
            == "You have won second prize in a beauty contest. Collect £10"
        ):
            player["balance"] += 10
            return player

        elif comchest["name"] == "You inherit £100":
            player["balance"] += 100
            return player

    return player


def playerPassedGo(player):
    player["current_position"] -= 40
    player["balance"] += 200
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
                player = playerLeaveJail(player)
                player["current_position"] += diceRoll

                player = chanceCard(player)
                logSpaceFinishedTurnOn(player["current_position"])

                # Rolled a double so entitled to another go
                playerAction(player)

                return player
            else:
                # Still in jail
                player["doubles_rolled_streak"] = 0
                player["turns_left_jail"] -= 1
                logSpaceFinishedTurnOn(player["current_position"])
                return player
        else:
            # Player can just leave jail for M50 fee
            # Can leave jail
            if player["get_out_of_jail_free_cards"] > 0:
                player["get_out_of_jail_free_cards"] -= 1
            else:
                player["balance"] -= 50
            player["doubles_rolled_streak"] = 0
            player = playerLeaveJail(player)
            player["current_position"] += diceRoll
            player = chanceCard(player)
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
                if player["current_position"] == 30:
                    player = playerGoToJail(player)
                    logSpaceFinishedTurnOn(player["current_position"])
                    return player

                # Board has 40 positions 0-39, if player rolls eg 6 whilst in position 39, their new positon = 45, should be 5
                if player["current_position"] >= 40:
                    player = playerPassedGo(player)

                player = chanceCard(player)
                logSpaceFinishedTurnOn(player["current_position"])
                # Player entitled to another go
                playerAction(player)

                return player
        else:
            player["doubles_rolled_streak"] = 0

            player["current_position"] += diceRoll

            if player["current_position"] == 30:
                player = playerGoToJail(player)
                logSpaceFinishedTurnOn(player["current_position"])

                return player
            # Board has 40 positions 0-39, if player rolls eg 6 whilst in position 39, their new positon = 45, should be 5
            if player["current_position"] >= 40:
                player = playerPassedGo(player)

            player = chanceCard(player)
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

    # Ignore type of space depending on space
    list = []
    if not config.displayJail:
        spaces = [i for i in spaces if not (i["name"] == "Jail")]
    if not config.displayGoToJail:
        spaces = [i for i in spaces if not (i["name"] == "Go To Jail")]

    for space in spaces:
        list.append(space["landed_on"])
    # Normalise data (0-1)
    xmin = min(list)
    xmax = max(list)
    print(xmin)
    print(xmax)
    for i, x in enumerate(list):
        list[i] = (x - xmin) / (xmax - xmin)

    # Find corresponding cmap color for normalised value
    cmap = matplotlib.cm.get_cmap("cividis_r")
    # cmap = matplotlib.cm.get_cmap("summer_r")
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
                    rule.style.color = "Lavender"
            except AttributeError as e:
                pass

        if not config.displayJail:
            id = "#position105"
            try:
                if rule.selectorText == id:
                    rule.style.backgroundColor = "White"
            except AttributeError as e:
                pass
        if not config.displayGoToJail:
            id = "#position30"
            try:
                if rule.selectorText == id:
                    rule.style.backgroundColor = "White"
            except AttributeError as e:
                pass

    # Write to new css file for html to read
    with open("stats.css", "wb") as f:
        f.write(parser.cssText)

    # Alter HTML to show percentage stats on mouseover
    with open("monopoly.html", "r") as file:
        soup = BeautifulSoup(file, "html.parser")
        for space in completeSpaces:
            id = "position" + str(space["position"])

            if "." in id:
                id = id.replace(".", "")

            div = soup.find("div", {"id": id})
            if div != None:
                for cs in completeSpaces:
                    if cs["position"] == space["position"]:
                        title_name = cs["name"]
                        title_percent = str(cs["landed_on_percentage"])
                        title_fraction = cs["landed_on_chance_fraction"]
                        title = (
                            title_name
                            + "\nPercentage: "
                            + title_percent
                            + "%\nFraction: "
                            + title_fraction
                        )
                        div["title"] = title

    with open("monopoly.html", "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))


def playGame():
    initialiseGame(config)
    # print(player_stats)
    for turn in range(config.turnsPerPlayer):
        for x in range(config.numberOfPlayers):
            playerActionReturn = playerAction(player_stats[x])
            # To make debugging easier, players 0-3 have different colours
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

end_time = time.time()
print("Execution time:", end_time - start_time)
