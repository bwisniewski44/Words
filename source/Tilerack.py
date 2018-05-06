from .Tile import Tile


class TileRack(object):

    def __init__(self):
        self._count_by_letter = dict()
        self._last_letter = None
        self._total_tiles = 0

    def __len__(self):
        return self._total_tiles

    def push(self, representation, count=1):
        """
        Places a tile representation into this tilerack.

        :param representation: (str) representation of tile
        :param count: (int) number of tile instances to add

        :return:
        """

        self._total_tiles += 1
        current_count = self._count_by_letter.get(representation, 0)
        new_count = current_count + count
        self._count_by_letter[representation] = new_count

    def pop(self, representation, values_by_tileface):
        """
        Draws a tile from this object.

        :param representation: (str) tile face representation (wildcard, or uppercase or capital letter)

        :return: (Tile object) drawn tile
        """

        self._modify(representation, -1)
        self._last_letter = representation

        # Return a Tile
        return Tile.representation_to_tile(representation, values_by_tileface)

    def _modify(self, letter, amount):
        """
        Ensures that the count associated with the given letter is adjusted by the given amount (or removed from the
        structure if the adjustment would otherwise leave the letter with a non-positive count).

        :param letter: (str) letter to adjust
        :param amount: (int) amount to add to the count

        :return:
        """

        current_count = self._count_by_letter.get(letter, 0)
        new_amount = max(0, current_count + amount)
        adjustment = new_amount - current_count
        if new_amount > 0:
            self._count_by_letter[letter] = new_amount
        else:
            self._count_by_letter.pop(letter)
        self._total_tiles += adjustment

    def restore(self):
        """
        Returns the last-drawn tile to the rack.
        :return:
        """

        if self._last_letter is not None:
            self._modify(self._last_letter, 1)
            self._last_letter = None

    def keys(self):
        """
        Gives a copy of the list of distinct tile faces.
        :return: (list of str) letters tracked in this object
        """

        return list(self._count_by_letter)
