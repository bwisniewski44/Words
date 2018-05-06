class Tile(object):

    @staticmethod
    def representation_to_tile(tileface, points_by_letter):
        tile = None
        if tileface.isupper():
            tile = Tile(tileface, points_by_letter[tileface])
        else:
            tile = Wildcard(tileface.upper())

        return tile

    def __init__(self, representation, value):
        self.value = value
        self.representation = representation
        self._letter = None

    def get_representation(self):
        """
        :return: (chr) gives the string representation of the tile
        """

        return self.representation

    def get_letter(self):
        return self._letter


class Wildcard(Tile):

    OPEN_CARD = '.'

    def __init__(self, representation='.'):
        Tile.__init__(self, representation, 0)

        self.assign(representation)

    def assign(self, letter):
        if letter.isupper():
            self._letter = letter
            self.representation = letter.lower()
        else:
            if letter == Wildcard.OPEN_CARD:
                self._letter = None
                self.representation = Wildcard.OPEN_CARD
            else:
                raise ValueError("Representation '%s' is not a valid wildcard." % letter)
