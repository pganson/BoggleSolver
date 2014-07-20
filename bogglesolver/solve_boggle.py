#!/usr/bin/env python

"""Class to solve the boggle boggle_board."""


from bogglesolver.boggle_board import Boggle
from bogglesolver.load_english_dictionary import Edict


class SolveBoggle:

    """
    Class to solve a boggle board.

    This initializes the dictionary and board.
    Then it searches the board for all valid words.
    """

    def __init__(self, use_test_words=False):
        self.use_test_words = use_test_words
        self.edict = Edict()
        self.edict.read_dictionary(self.use_test_words)
        self.boggle = Boggle()
        self.min_word_len = 3

    def set_board(self, columns, rows, boggle_list=None):
        """
        Set the board for the game.

        :param int columns: number of columns for the board.
        :param int rows: number of rows for the board.
        :param boggle_list: list of all the letters for the board (optional).
        :type boggle_list: list or None
        """
        self.boggle.num_columns = columns
        self.boggle.num_rows = rows
        self.boggle.size = columns * rows
        print("Size is: %s, columns are: %s, rows are: %s" % (self.boggle.size, self.boggle.num_columns, self.boggle.num_rows))
        if boggle_list is not None:
            self.boggle.set_array(boggle_list)
        else:
            self.boggle.generate_boggle_board()

    def solve(self, ignore_indexes=None, normal_adj=True):
        """
        Solve the boggle board, or get all words for scrabble.

        :param bool normal_adj: True to solve for boggle.
                                False to solve for scrabble.
        :returns: sorted list of all words found.
        """
        if ignore_indexes is None:
            ignore_indexes = []
        assert self.boggle.is_full(), "Boggle board has not been set."
        words = []
        for i, tile in enumerate(self.boggle.boggle_array):
            node = self.edict.dictionary_root
            if i not in ignore_indexes:
                ignored = ignore_indexes + [i]
                # print("Letter starting with %s" % letter)
                words += self.recurse_search_for_words(i, tile, '', node,
                                                       indexes_searched=ignored,
                                                       normal_adj=normal_adj)
        return sorted(set(words))

    def recurse_search_for_words(self, a_index, tile, word, node,
                                 indexes_searched, normal_adj=True):
        """
        Recursively search boggle board for words.

        :param int a_index: index in the word.
        :param str tile: current boggle tile.
        :param str word: current potential word.
        :param node: current node in the dictionary.
        :param indexes_searched: indexes searched already.
        :type indexes_searched: None or list.
        :param bool normal_adj: whether to solve for boggle or scrabble.
        """
        ret_val = []
        letter = tile[0]
        if len(tile) > 1:
            for l in tile[0:-1]:
                if l in node.letters.keys():
                    node = node.letters[l]
                else:
                    return ret_val
            letter = tile[-1]

        for index in self.boggle.get_adjacent(a_index, indexes_searched,
                                              normal_adj=normal_adj):
            searched = indexes_searched + [index]
            if self.edict.is_valid_path(node, letter):
                ret_val += self.recurse_search_for_words(index, self.boggle.boggle_array[index], word + tile, node.letters[letter], indexes_searched=searched, normal_adj=normal_adj)

        if self.edict.is_word(word + tile) and \
                             ((word + tile) not in ret_val) and \
                             (len(word + tile) >= self.min_word_len):
            ret_val.append(word + tile)
        return ret_val
