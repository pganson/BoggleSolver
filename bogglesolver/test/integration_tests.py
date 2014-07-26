#!/usr/bin/env python

"""Integration tests for all boggle classes."""


import sys
import unittest
import os.path
import time
import sqlite3
import os

from bogglesolver.load_english_dictionary import Edict
from bogglesolver.boggle_board import Boggle
from bogglesolver.solve_boggle import SolveBoggle

from bogglesolver.twl06 import WORD_LIST
from bogglesolver.twl06 import TEST_WORD_LIST

from bogglesolver.test import ENV, REASON

import boggleboard


@unittest.skipUnless(os.getenv(ENV), REASON)
class test_everything(unittest.TestCase):

    """
    All integration Tests.

    These tests all take a somewhat significant amount of time, usually due to loading in the dictionary.
    Could speed these up a lot if I store that dictionary globally.
    """

    # @unittest.skip("Skipping integration tests.")
    def test_solves_Boggle(self):
        """Test solving the boggle board."""
        columns = 4
        rows = 4
        array = "a b c d e f g h i j k l m n o p".split()

        assert len(array) == columns * rows

        solve_game = SolveBoggle()
        solve_game.set_board(columns, rows, array)

        # found words from: http://www.bogglecheat.net/, though may not be in my dictionary
        known_words = ["knife", "mino", "bein", "fink", "nife", "glop", "polk", "mink", "fino", "jink", "nief", "knop", "ink", "fin", "jin", "nim", "kop", "pol", "fab", "fie", "nie", "kon", "lop", "ab", "ef", "if", "mi", "be", "jo", "ch", "on", "lo", "ae", "ea", "in", "ba", "fa", "no", "ko", "op", "po"]
        for word in known_words:
            solve_game.edict.add_word(word)

        solve_game.min_word_len = 5
        solved = solve_game.solve()

        for word in known_words:
            if len(word) >= solve_game.min_word_len:
                assert word in solved
            else:
                assert word not in solved

        solve_game.min_word_len = 0
        solved = solve_game.solve()

        for word in known_words:
            if len(word) >= solve_game.min_word_len:
                assert word in solved
            else:
                assert word not in solved

    # @unittest.skip("Skipping integration tests.")
    def test_search_speed_vs_raw_read(self):
        """Test search speed."""
        my_dict = Edict()
        my_dict.read_dictionary()

        test_words = TEST_WORD_LIST

        allwords = ' '.join(WORD_LIST)
        alllines = WORD_LIST

        num_slower_than_read = 0
        num_slower_than_readlines = 0

        time1 = time.time()
        time2 = time.time()

        for a_word in test_words:
            word = a_word
            lower = a_word.lower().strip()
            if not my_dict.is_word(lower):
                print(word)

            time1 = time.time()
            assert my_dict.is_word(lower)
            time2 = time.time()
            dict_time = time2 - time1

            time1 = time.time()
            if word not in allwords:
                assert False
            time2 = time.time()
            all_time = time2 - time1

            time1 = time.time()
            if word not in alllines:
                assert False
            time2 = time.time()
            line_time = time2 - time1

            if dict_time > all_time:
                # print (word)
                num_slower_than_read += 1
            if dict_time > line_time:
                # print (word)
                num_slower_than_readlines += 1

        assert num_slower_than_read <= 1
        assert num_slower_than_readlines <= 1

    # @unittest.skip("Skipping integration tests.")
    def test_loads_all_words(self):
        """Test the dictionary can load all the words."""
        my_dict = Edict()
        my_dict.read_dictionary()

        for line in WORD_LIST:
            my_dict.is_word(line.lower())
            assert my_dict.is_word(line.lower())


# @unittest.skipUnless(os.getenv(ENV), REASON)
class test_speed_against_other_libraries(unittest.TestCase):

    """Test my boggle library against other boggle libraries."""

    def test_pypi_init_speeds(self):
        """Test how fast they load."""
        other_default_size = 4
        letters = ['i', 'r', 'e', 'e', 'r', 'i', 'u', 'c', 't', 's', 'i', 'e', 'a', 'n', 'i', 'a']

        t1 = time.time()
        their_boggle = boggleboard.BoggleBoard(other_default_size, letters)
        their_trie = boggleboard.Trie(WORD_LIST)
        t2 = time.time()

        their_time = t2 - t1

        t1 = time.time()
        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size, letters)
        t2 = time.time()

        my_time = t2 - t1

        print("My init time is: %s" % my_time)
        print("Their init time is: %s" % their_time)
        print("Mine is %s slower." % (my_time / their_time))
        assert my_time / their_time < 1

    def test_pypi_4_by_4(self):
        """Test 4x4 against the current boggle board on pypi."""
        other_default_size = 4
        letters = ['i', 'r', 'e', 'e',
                   'r', 'i', 'u', 'c',
                   't', 's', 'i', 'e',
                   'a', 'n', 'i', 'a']

        their_boggle = boggleboard.BoggleBoard(other_default_size, letters)
        their_trie = boggleboard.Trie(WORD_LIST)

        t1 = time.time()
        their_words = their_boggle.findWords(their_trie)
        t2 = time.time()

        their_solve_time = t2 - t1

        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size, letters)

        t1 = time.time()
        my_words = my_boggle.solve()
        t2 = time.time()

        my_solve_time = t2 - t1

        time_difference = my_solve_time / their_solve_time

        print("I found %s words." % len(my_words))
        print("They found %s words." % len(their_words))
        print("Mine is %s percent slower" % time_difference)
        print("My total time %s\nTheir total time %s" % (my_solve_time, their_solve_time))

        for word in their_words:
            if word not in my_words:
                print("I didn't find: %s" % word)
                assert my_boggle.edict.is_word(word)
        for word in my_words:
            assert word in their_words
        assert len(my_words) == len(their_words)
        assert time_difference < 1

    def test_pypi_10_by_10(self):
        """Test 10x10 against the current boggle board on pypi."""
        other_default_size = 10
        letters = ['o', 'i', 's', 'r', 'l', 'm', 'i', 'e', 'a', 't',
                   'g', 'e', 't', 'y', 'r', 'b', 'd', 's', 's', 'h',
                   'f', 'r', 'h', 'r', 'a', 'e', 'd', 'g', 'l', 'u',
                   'e', 'i', 'e', 'r', 's', 's', 'o', 'n', 'o', 'a',
                   'o', 'd', 'e', 'g', 'a', 'o', 'e', 't', 's', 'm',
                   'e', 'y', 's', 'e', 'e', 'b', 'i', 'd', 't', 'h',
                   'y', 'm', 'i', 'r', 'p', 'c', 's', 'm', 'r', 'e',
                   'b', 't', 'o', 'o', 'e', 'i', 'p', 's', 'r', 'u',
                   's', 'l', 'w', 'o', 'k', 'l', 'c', 't', 's', 'l',
                   'n', 'l', 'r', 'r', 'e', 'i', 'e', 's', 'g', 't']

        their_boggle = boggleboard.BoggleBoard(other_default_size, letters)
        their_trie = boggleboard.Trie(WORD_LIST)

        t1 = time.time()
        their_words = their_boggle.findWords(their_trie)
        t2 = time.time()

        their_solve_time = t2 - t1

        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size, letters)

        t1 = time.time()
        my_words = my_boggle.solve()
        t2 = time.time()

        my_solve_time = t2 - t1

        time_difference = my_solve_time / their_solve_time

        print("I found %s words." % len(my_words))
        print("They found %s words." % len(their_words))

        print("Mine is %s percent slower" % time_difference)
        print("My total time %s\nTheir total time %s" % (my_solve_time, their_solve_time))
        for word in their_words:
            if word not in my_words:
                print("I didn't find: %s" % word)
                assert my_boggle.edict.is_word(word)
        for word in my_words:
            assert word in their_words
        assert len(my_words) == len(their_words)
        assert time_difference < 1


if __name__ == '__main__':
    unittest.main()
