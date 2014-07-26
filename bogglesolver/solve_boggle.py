#!/usr/bin/env python

"""Class to solve the boggle boggle_board."""


from bogglesolver.boggle_board import Boggle
from bogglesolver.load_english_dictionary import Edict

from profilehooks import profile
import logging


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

    @profile(sort=['time', 'calls'])
    def solve(self, ignore_indexes=None, normal_adj=True):
        """
        Solve the boggle board, or get all words for scrabble.

        :param bool normal_adj: True to solve for boggle.
                                False to solve for scrabble.
        :returns: sorted list of all words found.
        """
        words = self.iterative_search_for_words(ignore_indexes, normal_adj)
#        if ignore_indexes is None:
#            ignore_indexes = []
#        assert self.boggle.is_full(), "Boggle board has not been set."
#        words = []
#        for i, tile in enumerate(self.boggle.boggle_array):
#            node = self.edict.dictionary_root
#            if i not in ignore_indexes:
#                ignored = ignore_indexes + [i]
#                # print("Letter starting with %s" % letter)
#                words += self.recurse_search_for_words(i, tile, '', node,
#                                                       indexes_searched=ignored,
#                                                       normal_adj=normal_adj)
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

        if self.edict.is_word(word + tile) and \
                             ((word + tile) not in ret_val) and \
                             (len(word + tile) >= self.min_word_len):
            ret_val.append(word + tile)

        for index in self.boggle.get_adjacent(a_index, indexes_searched,
                                              normal_adj=normal_adj):
            searched = indexes_searched + [index]
            if self.edict.is_valid_path(node, letter):
                ret_val += self.recurse_search_for_words(index, self.boggle.boggle_array[index], word + tile, node.letters[letter], indexes_searched=searched, normal_adj=normal_adj)
        return ret_val

    def iterative_search_for_words(self, visited_indexes, normal_adj=True):
        """
        Iteratively search for words.

        :retval: List of words found in the boggle board.
        """
        j = 0
        if visited_indexes is None:
            visited_indexes = []
        assert self.boggle.is_full(), "Boggle board has not been set."
        words = []

        # what structure should I use to keep track of visited paths? Let's try my dictionary structure.
        visited_paths = Edict()
        # add paths by calling visited_paths.add_words(path) where path is a string
        # check that a path exists by calling visited_paths.is_word()

        path = ['0']
        cur_word = [self.boggle.boggle_array[0]]
        cur_index = 0
        visited_paths.add_word(''.join(path))
        visited_indexes = [0]
        potential_word = ""

        while True:
            # logging.debug("Current index is: %s" % cur_index)
            # logging.debug("Visited indexes: %s" % visited_indexes)
            # logging.debug("Adjacent indexes are: %s\n" % self.boggle.get_adjacent(cur_index, visited_indexes, normal_adj=normal_adj))
            for index in self.boggle.get_adjacent(cur_index, visited_indexes, normal_adj=normal_adj):
                # logging.debug("Checking adjacent index %s for current index %s" % (index, cur_index))
                potential_word = ''.join(cur_word)
                if not visited_paths.is_word(''.join(path + [str(index)])):
                    if self.edict.is_still_potentially_valid(potential_word + self.boggle.boggle_array[index]):
                        cur_index = index
                        visited_paths.add_word(''.join(path + [str(index)]))
                        cur_word += [self.boggle.boggle_array[cur_index]]
                        path += [str(index)]
                        # logging.debug("Expanding path to: %s" % path)
                        visited_indexes.append(index)
                        break
            else:
                # back up one because there are not valid paths left off of this one.
                if len(path) > 1:
                    path.pop()
                    cur_word.pop()
                    visited_indexes.pop()
                    cur_index = int(path[-1])
                    # logging.debug("Poping off path of > 1. New path is: %s\n" % path)
                elif len(path) == 1:
                    if cur_index < self.boggle.size - 1:
                        cur_index += 1
                        visited_indexes = [cur_index]
                        path = [str(cur_index)]
                        cur_word = [self.boggle.boggle_array[cur_index]]
                        # logging.debug("incrementing current index to %s so starting letter is: %s\n" % (cur_index, self.boggle.boggle_array[cur_index]))
                    else:
                        logging.debug("leaving1")
                        break

            potential_word = ''.join(cur_word)
            # check if a word, if it is, add to words, if not, back the path up by 1 index
            if self.edict.is_word(potential_word) and len(potential_word) >= self.min_word_len:
                words.append(potential_word)
                # logging.debug("Found word %s" % ''.join(cur_word))

        return sorted(set(words))
