from .Board import Board
from .WordTree import WordTree
from .Tile import *
import heapq
from .Play import Play
from .Tilerack import Tilerack

class Abutments(object):
    """
    Gives information for open spaces regarding any surrounding words.
    """

    class Substring(object):
        def __init__(self):
            self.body = ''
            self.value = 0

    class WordInfo(object):
        def __init__(self):
            self.prefix = Abutments.Substring()
            self.suffix = Abutments.Substring()

    class SpaceInfo(object):
        def __init__(self):
            self.prefix = Abutments.WordInfo()
            self.suffix = Abutments.WordInfo()
            self.illegal_letters = set()
            self.has_adjacency = False  # gives whether the space is free AND has a tile next to it

    def __init__(self, dictionary):


    def _get_space_information(self, board, position, orientation):
        info = Abutments.WordInfo()

        prefix_data = board.get_adjacency(position, orientation, Board.Vector.REVERSE)
        suffix_data = board.get_adjacency(position, orientation, Board.Vector.FORWARD)

        info.prefix.body = prefix_data[0]
        info.prefix.value = prefix_data[1]

        info.suffix.body = suffix_data[0]
        info.suffix.value = suffix_data[1]

        node = self.word_tree.get_root()

        i = 0
        while i < len(info.prefix.body):

        if len(info.suffix.body) > 0:
            i = 0
            while i < len

        return info

    def poll(self, position, board):
        """
        Sets the definition
        :param position: (Board.Coordinate object)
        :param board: (Board object)
        :return:
        """

        space_info =

        # Collect the specifics
        adjacency = board.get_adjacency(position)

        if board.is_in_bounds(position):


def get_next_position(play):
    """
    :param play: (Play object) existing play onto which an appendage is considered
    :return: (Board.Coordinate object) position from which to append onto play
    """

    launch_vector = play.launch_vector
    v = Board.Vector(launch_vector.orientation, launch_vector.row, launch_vector.column)
    v.advance(len(play))

    return v.position

def expand_and_submit(plays, incoming_play, board, tile_rack, word_tree_node, depth, abutments):

    incoming_is_playable = True  # assume that the incoming Play may itself be played without expansion

    # Find position onto which to extend play
    lay_position = get_next_position(incoming_play)
    if board.is_in_bounds(lay_position):

        # If there is already a tile on the board at the position of expansion
        induced_expansion = board.get_tile(lay_position)  # get any Tile the incoming Play runs up against
        if induced_expansion:
            incoming_is_playable = False  # incoming play cannot stand alone; must include abutting tile

            # If the expansion could lead to a valid play...
            expanding_letter = induced_expansion.get_letter()
            if expanding_letter in word_tree_node.child_nodes:
                # ... extend the play by absorbing the tile on the board
                extended_play = incoming_play.duplicate()
                extended_play.absorb(induced_expansion)

                expand_and_submit(plays, extended_play, board, tile_rack, word_tree_node, depth)

        # Otherwise (space is open for a play to occur)
        else:
            # If allowed another lay...
            if len(tile_rack) > 0 and incoming_play.get_lay_count() < depth:
                # Determine which letters held can possibly lead to a solution
                theoretical_leads = tile_rack.keys().intersection(word_tree_node.child_nodes.keys())
                theoretical_leads.difference(illegals)  # discard those letters which cannot contribute to a solution

                # If there are any viable candidates...
                if len(theoretical_leads) > 0:
                    # Get general information about the space
                    multiplier = board.get_multiplier(lay_position)
                    encounters_crossword = True     # but really??
                    crossword_points = 0

                    # For each distinct literal tile...
                    for letter in theoretical_leads:
                        # Temporarily pull the tile
                        literal_tile = tile_rack.pop(letter)
                        extended_play = Play.copy(incoming_play)
                        extended_play.append(literal_tile, multiplier, encounters_crossword, crossword_points)

                        # Recursively find further plays
                        expand_and_submit(
                            plays,
                            extended_play,
                            board,
                            tile_rack,
                            word_tree_node.child_nodes[letter],
                            depth,
                            abutments
                        )

                        # Replace the tile
                        tile_rack.replace()

                    # If a wildcard is available...
                    if Wildcard.OPEN_CARD in tile_rack:
                        wildcard = tile_rack.pop(Wildcard.OPEN_CARD)

                        # For each possible resolution...
                        for resolution in theoretical_leads:
                            wildcard.assign(resolution)

                            extended_play = Play.copy(incoming_play)
                            extended_play.append(wildcard, multiplier, encounters_crossword, crossword_points)

                            expand_and_submit(
                                plays,
                                extended_play,
                                board,
                                tile_rack,
                                word_tree_node[resolution],
                                depth,
                                abutments
                            )

    # Add incoming to play if is word
    if incoming_is_playable and incoming_play.get_lay_count() > 0 and word_tree_node.is_word:
        # add play to result set
        heapq.heappush(plays, incoming_play)
