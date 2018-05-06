from .Tile import Tile


class Board(object):
    """
    Positive magnitudes represent right and downwards movement (for horizontal and vertical orientations, respectively).
    Negative magnitudes represent the opposite direction of their positive counterparts.
    """

    class Coordinate(object):
        def __init__(self, row=-1, column=-1):
            self.row = row
            self.column = column

    class Vector(object):
        HORIZONTAL = 0
        VERTICAL = 1

        FORWARD = 0
        REVERSE = 1

        @staticmethod
        def flip(direction):
            if direction:
                return 0
            else:
                return 1
            return 1 & (direction+1)    # one of these will probably run faster
            return 1 & (1 ^ direction)  # one of these will probably run faster

        def _move_vertically(self, magnitude=1):
            self.position.row += magnitude * self._advancement_direction

        def _move_horizontally(self, magnitude=1):
            self.position.column += magnitude * self._advancement_direction

        def __init__(self, row, column, orientation, direction=FORWARD):
            self.orientation = orientation
            self.position = Board.Coordinate(row, column)
            self._advancement_method = None     # function in which advancement is effected
            self._advancement_direction = 0     # direction in which advancement occurs (forward/reverse)

            self.set_orientation(orientation)
            self.set_direction(direction)

        def set_orientation(self, orientation):
            if orientation == Board.Vector.HORIZONTAL:
                self._advancement_method = Board.Vector._move_horizontally
            elif orientation == Board.Vector.VERTICAL:
                self._advancement_method = Board.Vector._move_vertically
            else:
                self._advancement_method = None

        def get_direction(self):
            if self._advancement_direction < 0:
                direction = Board.Vector.REVERSE
            elif self._advancement_direction > 0:
                direction = Board.Vector.FORWARD
            else:
                direction = None

            return direction

        def set_direction(self, direction):
            if direction == Board.Vector.FORWARD:
                self._advancement_direction = 1
            elif direction == Board.Vector.REVERSE:
                self._advancement_direction = -1
            else:
                self._advancement_direction = 0

        def advance(self, magnitude=1):
            self._advancement_method(magnitude)

    class Multiplier(object):
        LETTER = 0
        WORD = 1

        LETTER_FLAG = 'L'
        WORD_FLAG = 'W'

        scope_by_flag = {
            LETTER_FLAG: LETTER,
            WORD_FLAG: WORD
        }

        def __init__(self, magnitude=1, scope=LETTER):
            self.magnitude = magnitude
            self.scope = scope

    class Space(object):
        def __init__(self):
            self.tile = None
            self.multiplier = None

        def define(self, s, points_by_letter):
            """
            Sets the state of a Space. May be either a letter (Tile representation) or a Multiplier representation.

            Multiplier representations take the form <a><b>, where <a> is an integer representation and <b> is one
            of the following characters: Multiplier.LETTER_FLAG, Multiplier.WORD_FLAG

            :param s: (str) space representation; either a letter or a multiplier representation (or empty string)
            :param points_by_letter: (dictionary, chr to int) gives the points per letter
            :return:
            """

            if len(s) == 1:
                self.tile = Tile(s[0], points_by_letter)
            elif len(s) > 1:
                # Extract the pieces of information from the representation
                scope_flag = s[-1]                      # final letter gives the scope
                magnitude_representation = s[0:-1]      # everything up to the final letter gives the magnitude

                # Parse meaning from representation
                magnitude = int(magnitude_representation)
                scope = Board.Multiplier.scope_by_flag[scope_flag]

                # Initialize the multiplier object
                self.multiplier = Board.Multiplier(magnitude, scope)

    def __init__(self):
        self.height = 0
        self.width = 0
        pass

    def load(self, s, points_by_tile):
        """
        Loads the board state from s, a string that is a CSV.

        :param s:

        :return:
        """

        lines = s.split('\n')
        height = len(lines)

        cells = list()
        width = None
        i = 0
        while i < len(lines):
            # Get the next line's cell definitions and ensure they meet the width specification
            cell_definitions = lines[i].split(',')
            if width is None:
                width = len(cell_definitions)
            else:
                if len(cell_definitions) != width:
                    raise Exception("%d cells loaded into a board of width %d." % (len(cell_definitions), width))

            j = 0
            while j < len(cell_definitions):
                pass


        pass

    def is_in_bounds(self, position):
        """
        :param position: (Board.Coordinate object) position under consideration
        :return: TRUE/FALSE to indicate whether the position is on the board
        """

        return (0 <= position.row <= self.height) and (0 <= position.column <= self.width)

    def _get_space(self, position, orientation=None, direction=Vector.FORWARD, magnitude=1):
        """
        :param position: (Board.Coordinate object) position from which to fetch a Space
        :param orientation (Board.Vector orientation enum int) vert/horiz nature of traversal
        :param direction (Board.Vector direction enum int) forward/reverse nature of traversal
        :param magnitude (int) magnitude of traversal, if any is specified
        :return: (Space object) board space representation
        """

        # If traversal is required...
        if orientation is not None:
            v = Board.Vector(position.row, position.column, orientation, direction)
            v.advance(magnitude)
            position = v.position

        return Board.Space()
        pass

    def get_tile(self, position):
        """
        :param position: (Board.Coordinate object) position from which to fetch a laid Tile
        :return: (Tile object) tile at given position
        """

        return self._get_space(position).tile

    def get_multiplier(self, position):
        """
        :param position: (Board.Coordinate object) position from which to fetch a multiplier
        :return: (Board.Multiplier object) multiplier available at the given position
        """

        pass

    @staticmethod
    def get_relative_position(position, orientation, direction, magnitude=1):
        """"
        Advances in the given orientation/direction to yield the resulting space.
        :param position: (Board.Coordinate object) reference position
        :param orientation: (int)
        :param direction: (int)
        :param magnitude: (int)
        :return: (Board.Coordinate object)
        """

        v = Board.Vector(position.row, position.column, orientation, direction)
        v.advance(magnitude)
        return v.position

    # def connects(self, position):
    #     """
    #     :param position: (Board.Coordinate object) position
    #     :return: TRUE if the position is adjacent to any laid Tile
    #     """
    #
    #     is_connected = False
    #
    #     if self.get_tile(position) is not None:
    #         is_connected = True
    #     elif self.get_tile(
    #         Board.get_relative_position(position, Board.Vector.VERTICAL, Board.Vector.REVERSE)
    #     ) is not None:
    #         is_connected = True
    #     elif self.get_tile(
    #         Board.get_relative_position(position, Board.Vector.VERTICAL, Board.Vector.FORWARD)
    #     ) is not None:
    #         is_connected = True
    #     elif self.get_tile(
    #         Board.get_relative_position(position, Board.Vector.HORIZONTAL, Board.Vector.REVERSE)
    #     ) is not None:
    #         is_connected = True
    #     elif self.get_tile(
    #         Board.get_relative_position(position, Board.Vector.HORIZONTAL, Board.Vector.FORWARD)
    #     ) is not None:
    #         is_connected = True
    #
    #     return is_connected

    def tiles_until_connection(self, position, orientation, direction=Vector.FORWARD, cutoff=None):
        """
        :param position: (Board.Coordinate object) position from which to begin counting
        :param orientation: (int) Board.Vector enumeration giving whether advancement occurs horizontally or vertically
        :param direction: (int) Board.Vector enumeration giving whether advancement occurs forward, or in reverse
        :param cutoff: (int, optional) maximum count before returning None
        :return: (int, or None) number of Tiles required to be laid from pos in order to form a crossword, or None if no
        such count exists
        """

        # Get a vector by which to advance towards laid tiles
        v = Board.Vector(position.row, position.column, orientation, direction)
        cross_direction = Board.Vector.flip(direction)  # the cross-direction will become important

        # Advance towards any existing tiles
        connects = False  # assume no connection is made
        tiles_laid = 0
        while self.is_in_bounds(v.position):
            # Check to see if there's an existing tile
            if self.get_tile(v.position) is None:
                # lay a tile
                tiles_laid += 1
                if cutoff is not None:
                    if tiles_laid > cutoff:
                        break

                # check to see if there's a tile adjacent to the position within the cross-direction
                if self.get_tile(
                        Board.get_relative_position(v.position, cross_direction, Board.Vector.REVERSE)
                ) is not None:
                    connects = True
                    break
                elif self.get_tile(
                    Board.get_relative_position(v.position, cross_direction, Board.Vector.FORWARD)
                ) is not None:
                    connects = True
                    break
            else:
                connects = True
                break

            v.advance()

        # Return the number of tiles laid (
        if connects:
            return tiles_laid
        else:
            return None

    def get_adjacency(self, position, orientation, direction):
        """
        Collects the string of letters in a given orientation which either lead up to or follow a position.

        :param position: (Board.Coordinate)
        :param orientation: (int)
        :param direction: (int)
        :return: (str, int) word, sum value tiles
        """

        # Initialize empty result
        adjacency = ''
        value = 0

        vector = Board.Vector(position.row, position.column, orientation, direction)
        vector.advance()
        while self.is_in_bounds(vector.position):
            tile = self.get_tile(vector.position)
            if tile is None:
                break

            adjacency = tile.get_letter() + adjacency
            value += tile.value

            vector.advance()

        return adjacency, value
