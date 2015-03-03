#!/usr/bin/env python

"""Class to solve the boggle boggle_board."""


from bogglesolver.boggle_board import Boggle
from bogglesolver.adjacency import *


class SolveBoggle:

    """
    Class to solve a boggle board.

    This initializes the dictionary and board.
    Then it searches the board for all valid words.
    """

    def __init__(self, trie_root):
        self.trie_root = trie_root
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
        if boggle_list is not None:
            self.boggle.set_array(boggle_list)
        else:
            self.boggle.generate_boggle_board()
        return ''.join(self.boggle.boggle_array)

    def get_last_node(self, node, letter):
        """
        Determine if the letter provided is a valid path from the provided node.

        :param _dictnode node: node in the dictionary trie.
        :param str letter: next letter.
        :returns: True if the node has a path for the given letter, False Otherwise
        """
        for l in letter:
            if l not in node.letters.keys():
                return None
            node = node.letters[l]
        return node

    def solve(self, ignore_indexes=None, normal_adj=True, adjacency_funct=get_standard_boggle_adjacent):
        """
        Solve the boggle board, or get all words for scrabble.

        :param bool normal_adj: True to solve for boggle.
                                False to solve for scrabble.
        :returns: sorted list of all words found.
        """
        if ignore_indexes is None:
            ignore_indexes = []
        assert self.boggle.is_full(), "Boggle board has not been set."
        words = set()
        for i, letter in enumerate(self.boggle.boggle_array):
            node = self.get_last_node(self.trie_root, letter)
            if i not in ignore_indexes and node is not None:
                self.recurse_search_for_words(i, node, ignore_indexes + [i], adjacency_funct, words)
        return sorted(words)

    def recurse_search_for_words(self, a_index, node,
                                 indexes_searched, adjacency_funct, words=set()):
        """
        Recursively search boggle board for words.

        :param int a_index: current board index.
        :param indexes_searched: indexes searched already.
        :type indexes_searched: None or list.
        :param bool normal_adj: whether to solve for boggle or scrabble.
        """
        if node.word and (len(node.word) >= self.min_word_len):
            words.add(node.word)
        if not node.letters.keys():
            return
        for index in adjacency_funct(a_index, self.boggle.num_columns, self.boggle.num_rows, indexes_searched):
            new_node = self.get_last_node(node, self.boggle.boggle_array[index])
            if new_node is not None:
                self.recurse_search_for_words(index, new_node, indexes_searched + [index],
                                              adjacency_funct, words)
