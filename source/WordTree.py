class WordTree(object):
    """
    This decision tree tracks valid words as a decision tree of nodes: each node having a single letter. To determine
    whether a word is valid, start at the root and build a word by travelling down the node representing the next letter
    of the word. When at the final node, a boolean True/False will give whether the constructed word is valid.
    """

    class Node(object):
        def __init__(self):
            self.is_word = False
            self.child_nodes = {}   # dictionary of letter to following nodes

    @staticmethod
    def __travel_to(word, index, node, generate):
        """
        Travels to and returns the node representing the final character of the given word.

        :param word: (string) word directing travel through the tree
        :param index: (int) position to which to travel from current node
        :param node: (WordTree.Node object) current node from which to travel
        :param generate: (boolean) gives whether lack of a branch yields a new branch (fails otherwise)

        :return: (WordTree.Node object) node representing the final word letter; None if unreachable
        """

        # RECURSIVE CASE: still have letters directing travel
        if index < len(word):
            # Get decision tree branch to follow
            next_letter = word[index]
            if next_letter not in node.child_nodes:
                if generate:
                    node.child_nodes[next_letter] = WordTree.Node()
                else:
                    return None

            # Give the node returned by travelling down branch
            return WordTree.__travel_to(word, index+1, node, generate)

        else:
            return node

    def __init__(self):
        self.root = WordTree.Node()

    def is_member(self, word):
        word_node = WordTree.__travel_to(word, 0, self.root, False)
        if word_node is not None:
            return word_node.is_word
        return False

    def add_word(self, word):
        word_node = WordTree.__travel_to(word, 0, self.root, True)

        # Put word information into the node
        word_node.is_word = True    # declare that the string does represent a word

    def get_branches(self, word):
        # Get the node representing the word
        word_node = WordTree.__travel_to(word, 0, self.root, False)
        if word_node is None:
            branches = list()
        else:
            branches = word_node.child_nodes.keys()

        return branches

    def __contains__(self, word):
        return self.is_member(word) is not None
