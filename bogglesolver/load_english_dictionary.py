#!/usr/bin/env python

"""Stores the dictionary in a linked list."""


from bogglesolver.twl06 import WORD_LIST
from bogglesolver.twl06 import TEST_WORD_LIST


class _dictnode:

    """
    An element of the dictionary.

    Each element represents one letter in a word.
    Each element contains an array of potential next elements.
    This means that look-up time for a word depends only on the
        length of the word.
    It also means that if you have a partial word,
        all potential endings are further down the tree.
    """

    def __init__(self):
        self.is_word = False
        self.letters = {}
        self.word = ""


class Edict:

    """
    The interface for the dictionary.

    Contains the root element of the dictionary.
    Contains helpful functions for creating, adding to,
    and accessing the dictionary elements.
    """

    def __init__(self):
        self.dictionary_root = _dictnode()

    def read_dictionary(self, use_test_words=False):
        """
        Read in the list of valid words and add them to the dictionary.

        :param bool use_test_words: whether to use
            the test words or actual words.
        """
        words = None
        if use_test_words:
            words = TEST_WORD_LIST
        else:
            words = WORD_LIST
        for word in words:
            self.add_word(word.lower())

    def is_word(self, word):
        """
        Determine if a word is in the dictionary.

        Lookup in the dictionary is O(n)

        :param str word: word to look for in the dictionary.
        :returns: True if word is in dictionary. Otherwise False.
        """
        ret_val = False
        node = self.get_node(word)
        if node is not None:
            ret_val = node.is_word
        return ret_val

    def add_word(self, word):
        """
        Add a word to the dictionary.

        This is for extending the dictionary.

        :param str word: word to add.
        """
        node = self.dictionary_root
        length = len(word)
        for i, letter in enumerate(word.lower()):
            if letter in node.letters.keys():
                node = node.letters[letter]
            else:
                node.letters[letter] = _dictnode()
                node = node.letters[letter]
            if (length - 1) == i:
                node.is_word = True
                node.word = word.lower()

    def get_words(self, node, all_words=[]):
        """
        Get all words from the specified node on down.

        If called with the root node passed in,
            returns all words in the dictionary.

        :param _dictnode node: node to get all words from.
        :param list all_words: list of all words found so far.
        :returns: all words from the node on down.
        """
        for a_node in node.letters.keys():
            all_words = self.get_words(node.letters[a_node], all_words)
        if node.is_word and node.word not in all_words:
            all_words.append(node.word)
        return all_words

    def get_node(self, string):
        """
        Get a node based on the provided word.

        Used to determine if a string is still potentially a valid word.

        :param str string: find the node at the end of the string.
        :returns: node of the dictionary node that corresponds to
                  the end of the string or None if the string is not on
                  a valid dictionary path.
        """
        word = string.lower()
        node = self.dictionary_root
        for letter in word:
            if letter in node.letters.keys():
                node = node.letters[letter]
            else:
                node = None
                break
        return node

    def is_still_potentially_valid(self, word):
        """
        Determine if a possible word is still potentially valid.

        :param word: word to test for validity.
        """
        node = self.get_node(word)
        return node is not None

    def is_valid_path(self, node, letter):
        """
        Determine if the letter provided is a valid path from the provided node.

        :param _dictnode node: node in the Edict.
        :param str letter: next letter.
        :returns: True if the node has a path for the given letter, False Otherwise
        """
        if node:
            return letter in node.letters.keys()
        else:
            return False
