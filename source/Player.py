
class Player(object):

    class Decisions:
        RESIGN = 0
        PASS = 1
        SWAP = 2
        LAY = 3

    def __init__(self, display_name, consecutive_passes=0):
        self.display_name = display_name
        self.consecutive_passes = consecutive_passes

    def get_decision(self):
        """
        Gives the enumerated decision value indicating how the Player proceeds with play.

        :return: (int) enumerated decision value
        """

        raise NotImplementedError

    def get_play(self):
        """
        Gives a Play object representing the tiles the Player intends to put onto the board.

        :return: (Play object) play to be put to the board
        """

        raise NotImplementedError

    def restore_tiles(self, tilebag):
        """
        Reaches into bag of remaining tiles to restore player's tile rack.

        :return: n/a
        """

        while len(tilebag) > 0 and len(self.tiles) < TILE_GOAL:
            self.tiles.add(tilebag.draw())

    def take_turn(self):
        decision = self.get_decision()

        if decision == Player.Decisions.PASS:
            self.consecutive_passes += 1
        else:
            self.consecutive_passes = 0

        if decision == Player.Decisions.SWAP:
            pass
        elif decision == Player.Decisions.LAY:
            play = self.get_play()
            board.apply(play)


class Human(Player):

    @staticmethod
    def _get_input(prompt=None, data_type=None):
        """
        Gives the value input by the user.
        :param prompt: (str, optional) message printed to user to direct input
        :param data_type: (data type, optional) type to which to convert string input; defaults to string

        :return: (type value) value given by user
        """

        result = None

        if data_type is None:
            data_type = str

        good_input = False
        while not good_input:
            try:
                result = data_type(input(prompt))
            except ValueError:
                print("That was not a valid input.")

        return result

    def __init__(self):
        Player.__init__(self)

    def get_decision(self):
        """
        Prompts player for a decision on how the player wishes to proceed.

        :return: (int) decision enumeration
        """

        # Prompt user for input
        prompt = "Select an option: [%d] Resign, [%d] Pass, [%d] Swap, [%d] Lay" % (Player.Decisions.RESIGN, Player.Decisions.PASS, Player.Decisions.SWAP, Player.Decisions.LAY))
        decision = Human._get_input(prompt, int)


class Bot(Player):

    def __init__(self):
        Player.__init__(self)
