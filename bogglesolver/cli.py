#!/usr/bin/env python

"""Command-line interface for boggle solver."""

import argparse
import time

from bogglesolver.solve_boggle import SolveBoggle


def main(args=None):
    """
    Main entry point for the Command-line-interface.

    Looking at this for good idea of command line interface.
    http://manpages.ubuntu.com/manpages/trusty/man6/boggle.6.html
    """
    min_length = 3
    column = 4
    row = 4
    game_time = 180

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--play', action='store_true',
                        help="True if you want to play boggle.")
    parser.add_argument('-b', '--board', type=str,
                        help="String representing the Boggle Board.\
                              Must be used with -p.")
    parser.add_argument('-t', '--time', type=int,
                        help="int game time in seconds.")
    parser.add_argument('-l', '--length', type=int,
                        help="Change the minimum word length.")
    parser.add_argument('-w', '--words', type=str,
                        help="Get all words for a given list of letters.")

    args = parser.parse_args(args=args)

    if args.words:
        solver = SolveBoggle()
        solver.set_board(column, row, args.words.split())
        words = solver.solve(normal_adj=False)
        print(words)
        print("Found %s words." % len(words))

    if args.time:
        game_time = args.time

    if args.length:
        min_length = args.length

    if args.play:
        solver = SolveBoggle()
        solver.set_board(column, row)
        if args.board:
            solver.set_board(column, row, args.board.split())
        else:
            solver.boggle.generate_boggle_board()
        words = solver.solve()
        print(solver.boggle)
        print("Play Boggle!!")
        time.sleep(game_time)
        # cont = input('Press enter to see the solution.')
        i = 0
        for i, word in enumerate(words):
            if len(word) >= min_length:
                print(word)
        print(str(i) + " words found.")
        exit()


if __name__ == '__main__':
    main()
