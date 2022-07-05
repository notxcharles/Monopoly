class Player:
    """
    Class used to represent a player

    ...

    Attributes
    ----------
    player_number : int
        a number for the player, 1-max players
    current_position : int
        player's current position on the board (0-39)
    balance : int
        player's current balance
    doubles_rolled_streaks : int
        number of doubles the player has rolled in a row
    in_jail : Boolean
        whether the player is in jail or not
    turns_left_in_jail : int
        number of turns left for the player before he is released from jail
    get_out_of_jail_free_cards : int
        number of get out of jail free cards in the player's possession

    Methods
    -------

    """

    doubles_rolled_streak = 0
    in_jail = False
    turns_left_in_jail = 0
    get_out_of_jail_free_cards = 0

    def __init__(self, player_number, current_position=0, starting_balance=1500):
        """
        Parameters
        ----------
        player_number : int
            a number for the player, 1-max players
        current_position : int
            player's current position on the board (0-39)
        balance : int
            player's current balance
        """
        self.player_number = player_number
        self.current_position = current_position
        self.balance = starting_balance

    def goToJail(self):
        self.in_jail = True
        self.doubles_rolled_streak = 0
        self.turns_left_in_jail = 3
        self.current_position = 10.5

    def leaveJail(self):
        self.in_jail = False
        self.turns_left_in_jail = 0
        self.current_position = 10


class ChanceCard:
    """
    Class used to represent a chance card

    ...

    Attributes
    ----------
    name : str
        name of chance card
    reward_type : list
        type of reward
    reward : list
        reward of the card
    punishment_type : list
        type of punishment
    punishment : list
        punishment of the card

    Methods
    -------
    executeCard(player)
        executes chance card on behalf of player
    """

    def __init__(self, name, reward_type, reward, punishment_type, punishment):
        """
        name : str
            name of chance card
        reward_type : list
            type of reward
        reward : list
            reward of the card
        punishment_type : list
            type of punishment
        punishment : list
            punishment of the card
        """
        self.name = name
        self.reward_type = reward_type
        self.reward = reward
        self.punishment_type = punishment_type
        self.punishment = punishment

    def executeCard(self, player):
        """
        Executes chance card on behalf of player

        Parameters
        ----------
        player : object
            player created by player class
        """
        for i in range(len(self.reward_type)):
            r_type = self.reward_type[i]
            if r_type == "balance":
                player.balance += self.reward[i]
            elif r_type == "goto_position":
                if player.current_position >= self.reward[i]:  # Player passed go
                    player.balance += 200  # Player passed go
                player.current_position = self.reward[i]
            elif r_type == "station":
                # Go to nearest station
                if player.current_position >= 5:
                    player.current_position = 15
                elif player.current_position >= 15:
                    player.current_position = 25
                elif player.current_position >= 25:
                    player.current_position = 35
                elif player.current_position >= 35:
                    player.current_position = 5
            elif r_type == "utility":
                if player.current_position >= 12:
                    player.current_position = 28
                elif player.current_position >= 28:
                    player.current_position = 12
            elif r_type == "card":
                player.get_out_of_jail_free_cards += 1
            elif r_type == "position_change":
                player.current_position += self.reward[i]

        for i in range(len(self.punishment_type)):
            p_type = self.punishment_type[i]
            if p_type == "position_change":
                player.current_position += self.punishment[i]
            if p_type == "goto_position":
                player.current_position = self.punishment[i]
            if p_type == "balance":
                player.balance += self.punishment[i]
            if p_type == "pay_players":
                totalOthers = len(players) - 1
                player.balance -= 50 * totalOthers
                for i in range(len(players)):
                    if i.player_number == player.player_number:
                        continue
                    else:
                        i.balance += 50


class CommunityChestCard:
    """
    Class used to represent a community chest card

    ...

    Attributes
    ----------
    name : str
        name of community chest card
    reward_type : list
        type of reward
    reward : list
        reward of the card
    punishment_type : list
        type of punishment
    punishment : list
        punishment of the card

    Methods
    -------
    executeCard(player)
        executes community chest card on behalf of player
    """

    def __init__(self, name, reward_type, reward, punishment_type, punishment):
        """
        name : str
            name of community chest card
        reward_type : list
            type of reward
        reward : list
            reward of the card
        punishment_type : list
            type of punishment
        punishment : list
            punishment of the card
        """
        self.name = name
        self.reward_type = reward_type
        self.reward = reward
        self.punishment_type = punishment_type
        self.punishment = punishment

    def executeCard(self, player):
        """
        Executes community chest card on behalf of player

        Parameters
        ----------
        player : object
            player created by player class
        """
        for i in range(len(self.reward_type)):
            r_type = self.reward_type[i]
            if r_type == "balance":
                player.balance += self.reward[i]
            elif r_type == "goto_position":
                if player.current_position >= self.reward[i]:  # Player passed go
                    player.balance += 200  # Player passed go
                player.current_position = self.reward[i]
            elif r_type == "card":
                player.get_out_of_jail_free_cards += 1
            elif r_type == "players_pay":
                totalOthers = len(players) - 1
                player.balance += 50 * totalOthers
                for i in range(len(players)):
                    if i.player_number == player.player_number:
                        continue
                    else:
                        i.balance -= 50

        for i in range(len(self.punishment_type)):
            p_type = self.punishment_type[i]
            if p_type == "goto_position":
                player.current_position = self.punishment[i]
            elif p_type == "balance":
                player.balance += self.punishment[i]


class Space:
    """
    Class used to represent a space

    ...

    Attributes
    ----------
    name : str
            name of space
    space : int
        position on board (0-39)
    type : str
        space type, property, community chest, tax, chance, just visiting, jail, free parking
    set : str
        type of set, colour set, utility, station
    landed_on : int
        times space has been landed on


    Methods
    -------
    """

    landed_on = 0

    def __init__(self, name, position, type, set):
        """
        name : str
            name of space
        space : int
            position on board (0-39)
        type : str
            space type, property, community chest, tax, chance, just visiting, jail, free parking
        set : str
            type of set, colour set, utility, station
        """
        self.name = name
        self.position = position
        self.type = type
        self.set = set
