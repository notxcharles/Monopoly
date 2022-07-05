# Trying to update the original monopoly to use classes

import time

start_time = time.time()

import random
import config
from classes import Player, ChanceCard, CommunityChestCard, Space


players = []
board = []
jail_space = None
chance_cards = []
community_chest_cards = []


def createChanceCards(shuffle=True):
    """
    Creates a chance card from the current (July 2022) set of chance cards.
    """
    chance_card = ChanceCard(
        name="Advance to Go (Collect £200)",
        reward_type=["balance", "goto_position"],
        reward=[200, 0],
        punishment_type=None,
        punishment=None,
    )
    chance_cards.append(chance_card)

    chance_card = ChanceCard(
        name="Advance to Trafalgar Square. If you pass Go, collect £200",
        reward_type=["goto_position"],
        reward=[24],
        punishment_type=None,
        punishment=None,
    )
    chance_cards.append(chance_card)

    chance_card = ChanceCard(
        name="Advance to Pall Mall. If you pass Go, collect £200",
        reward_type=["goto_position"],
        reward=[11],
        punishment_type=None,
        punishment=None,
    )
    chance_cards.append(chance_card)

    chance_card = ChanceCard(
        name="Advance to Nearest Station",
        reward_type=["station"],
        reward=None,
        punishment_type=None,
        punishment=None,
    )
    chance_cards.append(chance_card)

    chance_card = ChanceCard(
        name="Advance to Nearest Station",
        reward_type=["station"],
        reward=None,
        punishment_type=None,
        punishment=None,
    )
    chance_cards.append(chance_card)

    chance_card = ChanceCard(
        name="Advance to Utility",
        reward_type=["utility"],
        reward=None,
        punishment_type=None,
        punishment=None,
    )
    chance_cards.append(chance_card)

    chance_card = ChanceCard(
        name="Bank pays you dividend of £50",
        reward_type=["balance"],
        reward=[50],
        punishment_type=None,
        punishment=None,
    )
    chance_cards.append(chance_card)
    chance_card = ChanceCard(
        name="Get Out of Jail Free",
        reward_type=["card"],
        reward=None,
        punishment_type=None,
        punishment=None,
    )
    chance_cards.append(chance_card)

    chance_card = ChanceCard(
        name="Go Back 3 Spaces",
        reward_type=None,
        reward=None,
        punishment_type=["position_change"],
        punishment=[-3],
        # If we're going back 3 spaces we also need to do what is on the space we land
    )
    chance_cards.append(chance_card)

    chance_card = ChanceCard(
        name="Go to Jail. Go directly to Jail, do not pass Go, do not collect £200",
        reward_type=None,
        reward=None,
        punishment_type=["goto_position"],
        punishment=[10.5],
    )
    chance_cards.append(chance_card)

    chance_card = ChanceCard(
        name="Speeding fine £15",
        reward_type=None,
        reward=None,
        punishment_type=["balance"],
        punishment=[-15],
    )
    chance_cards.append(chance_card)

    chance_card = ChanceCard(
        name="Take a trip to Kings Cross Station. If you pass Go, collect £200",
        reward_type=["goto_position"],
        reward=[5],
        punishment_type=None,
        punishment=None,
    )
    chance_cards.append(chance_card)

    chance_card = ChanceCard(
        name="You have been elected Chairman of the Board. Pay each player £50",
        reward_type=None,
        reward=None,
        punishment_type=["pay_players"],
        punishment=[50],
    )
    chance_cards.append(chance_card)

    chance_card = ChanceCard(
        name="Your building loan matures. Collect £150",
        reward_type=["balance"],
        reward=[150],
        punishment_type=None,
        punishment=None,
    )
    chance_cards.append(chance_card)

    if shuffle == True:
        random.shuffle(chance_cards)

    return


def createCommunityChestCards(shuffle=True):
    """
    Creates a community chest card from the current (July 2022) set of chance cards.
    """
    community_chest_card = CommunityChestCard(
        name="Advance to Go (Collect £200)",
        reward_type=["balance", "goto_position"],
        reward=[200, 0],
        punishment_type=None,
        punishment=None,
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="Bank error in your favour. Collect £200",
        reward_type=["balance"],
        reward=[200],
        punishment_type=None,
        punishment=None,
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="Doctor's fee. Pay £50",
        reward_type=None,
        reward=None,
        punishment_type=["balance"],
        punishment=[-50],
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="From sale of stock you get £50",
        reward_type=["balance"],
        reward=[50],
        punishment_type=None,
        punishment=None,
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="Get out of jail free",
        reward_type=["card"],
        reward=None,
        punishment_type=None,
        punishment=None,
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="Go to Jail. Go directly to jail, do not pass Go, do not collect £200",
        reward_type=None,
        reward=None,
        punishment_type=["goto_position"],
        punishment=[10.5],
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="Holiday fund matures. Recieve £100",
        reward_type=["balance"],
        reward=[100],
        punishment_type=None,
        punishment=None,
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="Income tax refund. Collect £20",
        reward_type=["balance"],
        reward=[20],
        punishment_type=None,
        punishment=None,
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="It is your birthday. Collect £10 from every player",
        reward_type=["players_pay"],
        reward=[10],
        punishment_type=None,
        punishment=None,
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="Life insurance matures. Collect £20",
        reward_type=["balance"],
        reward=[20],
        punishment_type=None,
        punishment=None,
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="Pay hospital fees of £100",
        reward_type=None,
        reward=None,
        punishment_type=["balance"],
        punishment=[-100],
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="Pay school fees of £50",
        reward_type=None,
        reward=None,
        punishment_type=["balance"],
        punishment=[-50],
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="Recieve £25 consultancy fee",
        reward_type=["balance"],
        reward=[25],
        punishment_type=None,
        punishment=None,
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="You have won second prize in a beauty contest. Collect £10",
        reward_type=["balance"],
        reward=[10],
        punishment_type=None,
        punishment=None,
    )
    community_chest_cards.append(community_chest_card)

    community_chest_card = CommunityChestCard(
        name="You inherit £100",
        reward_type=["balance"],
        reward=[100],
        punishment_type=None,
        punishment=None,
    )
    community_chest_cards.append(community_chest_card)

    if shuffle == True:
        random.shuffle(community_chest_cards)

    return


def createBoard():
    """
    Create the regular spaces for monopoly.
    """
    space = Space("Go", 0, "Go", None)
    board.append(space)

    space = Space("Old Kent Road", 1, "Property", "Brown")
    board.append(space)

    space = Space("Community Chest", 2, "Community Chest", None)
    board.append(space)

    space = Space("Whitechapel Road", 3, "Property", "Brown")
    board.append(space)

    space = Space("Income Tax", 4, "Tax", None)
    board.append(space)

    space = Space("Kings Cross Station", 5, "Property", "Station")
    board.append(space)

    space = Space("The Angel Islington", 6, "Property", "Light blue")
    board.append(space)

    space = Space("Chance", 7, "Chance", None)
    board.append(space)

    space = Space("Euston Road", 8, "Property", "Light blue")
    board.append(space)

    space = Space("Pentonville Road", 9, "Property", None)
    board.append(space)

    space = Space("Just Visiting", 10, "Just Visiting", None)
    board.append(space)

    space = Space("Pall Mall", 11, "Property", "Pink")
    board.append(space)

    space = Space("Electric Company", 12, "Property", "Utility")
    board.append(space)

    space = Space("Whitehall", 13, "Property", "Pink")
    board.append(space)

    space = Space("Northumberland Avenue", 14, "Property", "Pink")
    board.append(space)

    space = Space("Marylebone Station", 15, "Property", "Station")
    board.append(space)

    space = Space("Bow Street", 16, "Property", "Orange")
    board.append(space)

    space = Space("Community Chest", 17, "Community Chest", None)
    board.append(space)

    space = Space("Marlborough Street", 18, "Property", "Orange")
    board.append(space)

    space = Space("Vine Street", 19, "Property", "Orange")
    board.append(space)

    space = Space("Free Parking", 20, "Free Parking", None)
    board.append(space)

    space = Space("Strand", 21, "Property", "Red")
    board.append(space)

    space = Space("Chance", 22, "Chance", None)
    board.append(space)

    space = Space("Fleet Street", 23, "Property", "Red")
    board.append(space)

    space = Space("Trafalgar Square", 24, "Property", "Red")
    board.append(space)

    space = Space("Fenchurch St. Station", 25, "Property", "Station")
    board.append(space)

    space = Space("Leicester Square", 26, "Property", "Yellow")
    board.append(space)

    space = Space("Coventry Street", 27, "Property", "Yellow")
    board.append(space)

    space = Space("Water Works", 28, "Property", "Utility")
    board.append(space)

    space = Space("Piccadilly", 29, "Property", "Yellow")
    board.append(space)

    space = Space("Go To Jail", 30, "Jail", None)
    board.append(space)

    space = Space("Regent Street", 31, "Property", "Green")
    board.append(space)

    space = Space("Oxford Street", 32, "Property", "Green")
    board.append(space)

    space = Space("Community Chest", 33, "Community Chest", None)
    board.append(space)

    space = Space("Bond Street", 34, "Property", "Green")
    board.append(space)

    space = Space("Liverpool St. Station", 35, "Property", "Station")
    board.append(space)

    space = Space("Chance", 36, "Chance", None)
    board.append(space)

    space = Space("Park Lane", 37, "Property", "Blue")
    board.append(space)

    space = Space("Super Tax", 38, "Tax", None)
    board.append(space)

    space = Space("Mayfair", 39, "Property", "Blue")
    board.append(space)

    jail_space = Space("Jail", 10.5, "Jail", None)


def initialiseGame(config):
    """
    Start the game, we need to create the number of players (chosen in the config), the chance and community chest cards (as well as shuffle them)
    """
    for x in range(config.numberOfPlayers):
        player = Player(
            player_number=x,
            current_position=config.startingPosition,
            starting_balance=config.startingBalance,
        )
        players.append(player)

    createBoard()
    createChanceCards(shuffle=True)
    createCommunityChestCards(shuffle=True)


initialiseGame(config)

end_time = time.time()
print("Execution time:", end_time - start_time)
