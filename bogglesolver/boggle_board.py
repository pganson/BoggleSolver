#!/usr/bin/env python

"""Classes that keep track of the board."""


from bogglesolver.twl06 import WORD_LIST
import random


class Boggle:

    """
    The boggle board.

    This represents the physical board and where each letter is.
    """

    def __init__(self, num_columns=5, num_rows=5):
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.boggle_array = [None] * (self.num_columns * self.num_rows)
        self.size = self.num_columns * self.num_rows

    def __str__(self):
        string = ""
        if self.is_full():
            max_len = 1
            spaces = " "
            for tile in self.boggle_array:
                if len(tile) > max_len:
                    max_len = len(tile)
            for i, tile in enumerate(self.boggle_array):
                spaces = " " * (max_len - (len(tile) - 1))
                max_spaces = " " * (max_len)
                if (i % self.num_columns is 0) and (i is not 0):
                    string += "%s|\n" % spaces
                    string += " |%s%s" % (spaces, tile)
                elif i is 0:
                    string += " |%s%s" % (spaces, tile)
                else:
                    string += "%s|%s%s" % (max_spaces, spaces, tile)

            string += "%s|\n" % spaces
        return string

    def generate_boggle_board(self):
        """Generate a boggle board by randomly selecting letters from valid words."""
        combined_words = ''.join(WORD_LIST)
        self.boggle_array = []
        print("Generating boggle board of size: %s" % self.size)
        for i in range(0, self.size):
            random_number = random.randint(0, len(combined_words) - 1)
            self.boggle_array.append(combined_words[random_number])

    def is_adjacent(self, index_1, index_2):
        """
        Determine if two indexes are adjacent.

        :param int index_1: first index
        :param int index_2: second index
        :returns: True if the indexes are adjacent. False otherwise.

        ret_val = False

        row_1 = index_1 // self.num_columns
        row_2 = index_2 // self.num_columns
        column_1 = index_1 % self.num_columns
        column_2 = index_2 % self.num_columns

        rows_are_less_than_1_away = abs(row_2 - row_1) <= 1
        columns_are_less_than_1_away = abs(column_2 - column_1) <= 1
        if rows_are_less_than_1_away and columns_are_less_than_1_away:
            ret_val = True

        if (index_2 // self.num_columns)

        return ret_val
        """
        if abs((index_2 // self.num_columns) - (index_1 // self.num_columns)) <= 1 and abs((index_2 % self.num_columns) - (index_1 % self.num_columns)) <= 1:
            return True

        return False

    def get_adjacent(self, index, ignore=None, normal_adj=True):
        """
        Get all adjacent indexes.

        Ignore is meant to be the disabled or previously traversed indexes.
        Normal_adj is to toggle between finding words in a boggle board
            and finding all possible words for scrabble.
            True is find words in boggle board. False is to find scrabble
            words.

        :param int index: index to get all adjacent indexes of.
        :param list ignore: optional list of indexes to ignore.
        :param bool normal_adj: whether to use the normal is adjacent
               or ignore it.
        :returns: True if adjacent. False otherwise.
        """
        if ignore is None:
            ignore = []

        # if not normal adjacent
        if normal_adj:
            row = index // self.num_columns
            column = index % self.num_columns

            # calculate the 8 indexes that surround this index

            # index directly to the left:
            if column != 0:
                if index - 1 not in ignore:
                    yield index - 1
                # diagonal up and left
                if row != 0 and index - self.num_columns - 1 not in ignore:
                    yield index - self.num_columns - 1
                # diagonal down and left
                if row != self.num_rows - 1 and index + self.num_columns - 1 not in ignore:
                    yield index + self.num_columns - 1

            # index directly to the right:
            if column != self.num_columns - 1:
                if index + 1 not in ignore:
                    yield index + 1
                # index to the top right
                if row != 0 and index - self.num_columns + 1 not in ignore:
                    yield index - self.num_columns + 1
                # index to the bottom right
                if row != self.num_rows - 1 and index + self.num_columns + 1 not in ignore:
                    yield index + self.num_columns + 1

            # directly above
            if row != 0 and index - self.num_columns not in ignore:
                yield index - self.num_columns

            # directly below
            if row != self.num_rows - 1 and index + self.num_columns not in ignore:
                yield index + self.num_columns

        else:
            for i in range(0, self.size):
                if i not in ignore and i is not index:
                    yield i

    def insert(self, character, index):
        """
        Insert a character into the boggle array.

        :param str character: character to insert.
        :param int index: index to insert the character at.
        """
        if index < len(self.boggle_array):
            self.boggle_array[index] = character

    def is_full(self):
        """
        If the boggle board has been completely filled.

        :returns: True if full. False otherwise.
        """
        ret_val = True
        if len(self.boggle_array) == self.size:
            for i in range(0, self.size):
                if self.boggle_array[i] is None:
                    ret_val = False
                    print("Found element of array that was None.")
        else:
            print("Boggle array len: %s does not equal size: %s." % (len(self.boggle_array), self.size))
            ret_val = False
        return ret_val

    def set_array(self, array):
        """
        Set the boggle array with the one provided.

        :param list array: list to set the boggle array to.
        """
        self.boggle_array = array
