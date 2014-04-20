import unittest
import os.path
import sys
sys.path.insert(0,'..\\')
from load_english_dictionary import e_dict
from boggle_board import boggle

test_name = "..\\..\\docs\\test_words.txt"

class test_boggle_adjacent(unittest.TestCase):
    def test_four_by_four(self):
        b = boggle(4,4)
        assert b.is_adjacent(0,1)
        assert b.is_adjacent(1,2)
        assert b.is_adjacent(2,3)
        assert False is b.is_adjacent(3,4)
        assert False is b.is_adjacent(3,5)
        assert False is b.is_adjacent(3,11)
        assert b.is_adjacent(4,5)
        assert b.is_adjacent(6,7)
        assert b.is_adjacent(8,9)
        assert b.is_adjacent(10,11)
        assert b.is_adjacent(12,13)
        assert b.is_adjacent(14,15)
        assert b.is_adjacent(1,1)
        assert b.is_adjacent(5,10)
        assert b.is_adjacent(1,4)

    def test_four_by_four(self):
        b = boggle(5,3)
        assert b.is_adjacent(0,1)
        assert b.is_adjacent(6,7)
        assert b.is_adjacent(12,13)
        assert b.is_adjacent(0,7) is False
        assert b.is_adjacent(3,13) is False
        assert b.is_adjacent(0,14) is False
        assert b.is_adjacent(1,7)
        assert b.is_adjacent(9,13)
        assert b.is_adjacent(4,8)

    def test_get_adjacent53(self):
        b = boggle(5,3)
        # middle
        adj = b.get_adjacent(6)
        t = [0,1,2,5,7,10,11,12]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # side
        adj = b.get_adjacent(9)
        t = [3,4,8,13,14]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # corner
        adj = b.get_adjacent(0)
        t = [1,5,6]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

    def test_get_adjacent44(self):
        b = boggle(4,4)

        # middle
        adj = b.get_adjacent(6)
        t = [1,2,3,5,7,9,10,11]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # side
        adj = b.get_adjacent(7)
        t = [2,3,6,10,11]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # corner
        adj = b.get_adjacent(12)
        t = [8,9,13]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

class test_add_word(unittest.TestCase):

    def test_hi(self):
        ed = e_dict()
        ed.add_word("hi")
        assert(ed.is_word("hi"))

    def test_casesensetive(self):
        ed = e_dict()
        ed.add_word("ThEoDoRe")
        assert(ed.is_word("theodore"))
        assert(ed.is_word("THEODORE"))
        assert(ed.is_word("THEOdore"))
        
    def test_multiplewordswithsameroot(self):
        ed = e_dict()
        ed.add_word("he")
        ed.add_word("HELL")
        ed.add_word("HELLo")
        assert(ed.is_word("he"))
        assert(ed.is_word("hell"))
        assert(ed.is_word("hello"))
        assert(False is ed.is_word("h"))
        assert(False is ed.is_word("hel"))

    def test_get_all_words(self):
        ed = e_dict()
        t = open(test_name)
        i = 0
        lines = t.readlines()
        #for i,word in enumerate(lines):
        #    ed.add_word(word)

        #all_words = ed.get_words(ed.dictionary_root)
        #assert len(all_words) is len(lines)

        #for word in lines:
        #    assert word in all_words
        

if __name__ == '__main__':
    unittest.main()
