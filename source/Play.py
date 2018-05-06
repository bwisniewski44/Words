from .Board import Board


class Play(object):
    """
    Tracks information about a move in the game. Must be "finalized" before in order for summary statistics to be
    calculated.
    """

    @staticmethod
    def copy(p):
        """
        Yields a Play object equivalent to that of the argument.
        :param p: (Play object) reference to Play object to be deep copied
        :return: (Play object) a deep copy of the given play
        """

        return Play()

    def __init__(self, launch_vector):
        self.launch_vector = launch_vector
        self.word = ''
        self.connects = False

        self.inline_points = 0
        self.crossword_points = 0

        self.word_multiplier = 1
        self._lay_count = 0  # number of tiles laid (as opposed to absorbed)

    def finalize(self):
        """
        Assesses statistics about play.
        :return:
        """

    def absorb(self, tile):
        """
        Appends tile to play as if the tile already exists on the board (not laying down the play).
        :param tile: (Tile object) tile to append to this play
        :return: None
        """

        self.word += tile.get_letter()
        self.inline_points += tile.value
        self.connects = True

    def append(self, tile, multiplier, encounters_crossword=False, crossword_value=0):
        """
        Modifies the Play by appending a letter.
        :param tile: (Tile object) tile to be appended to this Play
        :param absorbing: (bool) TRUE if Tile is already on board; FALSE if laying tile to expand play
        :param multiplier: (Multiplier object) multiplier onto which a tile is being laid
        :param crossword_value: (int) value of cross-direction tiles connecting to appending tile
        :return:
        """

        self._lay_count += 1

        inline_points = tile.value
        if multiplier.scope == Board.Multiplier.LETTER:
            inline_points *= multiplier.magnitude

        # No multiplier can be
        if absorbing:
            multiplier = None
            crossword_value = 0

        pass

    def __len__(self):
        return len(self.word)

    def get_lay_count(self):
        return self._lay_count