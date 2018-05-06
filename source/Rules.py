from .WordTree import WordTree
import pymysql


class Rules(object):
    """
    Contains game parameters.
    """

    def __init__(self, dictionary_path):
        """

        :param dictionary_path: (str) path to dictionary file; one word per line
        """
        self.points_by_letter = dict()
        self.wildcard_value = 0
        self.dictionary = WordTree()
        self.max_consecutive_passes_per_player = 1
        self.alphabet = set()

        with open(dictionary_path, )