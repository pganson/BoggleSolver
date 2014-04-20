import sys
import unittest
import os.path
import time
import sqlite3
import os

sys.path.insert(0,'..\\')
from load_english_dictionary import e_dict

f_name = "..\\..\\docs\\english_words.txt"
test_name = "..\\..\\docs\\test_words.txt"

class test_everything(unittest.TestCase):
    def test_search_speed_vs_raw_read(self):
        d = e_dict()
        d.read_dictionary(f_name)

        t = open(test_name)
        test_words = t.readlines()

        f = open(f_name)
        p = open(f_name)
        allwords = f.read()
        alllines = p.readlines()

        t1 = time.time()
        t2 = time.time()
        for a_word in test_words:
            word = a_word
            lower = a_word.lower()
            
            t1 = time.time()
            assert d.is_word(lower)
            t2 = time.time()
            dict_time = t2-t1

            t1 = time.time()
            if word not in allwords:
                assert False
            t2 = time.time()
            all_time = t2-t1

            t1 = time.time()
            if word not in alllines:
                assert False
            t2 = time.time()
            line_time = t2-t1

            if dict_time > all_time:
                print (word)
                assert False
            if dict_time > line_time:
                print (word)
                assert False

    def test_loads_all_words(self):
        d = e_dict()
        d.read_dictionary(f_name)

        f = open(f_name)

        for line in f.readlines():
            d.is_word(line.lower())
            assert d.is_word(line.lower())

    def test_against_my_sql(self):
        d = e_dict()
        d.read_dictionary(f_name)

        f = open(f_name)

        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE my_dict (word text)''')
        
        for word in f.readlines():
            c.execute("INSERT INTO my_dict VALUES (?)",[word])
            # c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")


        conn.commit()

        t = open(test_name)
        test_words = t.readlines()

        t1 = time.time()
        t2 = time.time()
        for word in test_words:
            t1 = time.time()
            d.is_word(word)
            t2 = time.time()
            d_time = t2-t1

            t1 = time.time()
            c.execute('SELECT * FROM my_dict WHERE word=?',[word])
            t2 = time.time()
            b_time = t2-t1

            if d_time > b_time:
                print "D time is: " + str(d_time)
                print "B time is: " + str(b_time)
        c.close()
        conn.close()

        os.remove("example.db")

if __name__ == '__main__':
    unittest.main()
