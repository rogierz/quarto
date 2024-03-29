import argparse
from players import PLAYERS

parser = argparse.ArgumentParser()
parser.add_argument(
    '-b',
    '--benchmark',
    action='store_true',
    dest='benchmark',
    help='execute 100 iterations')

parser.add_argument(
    '-t',
    '--tournament',
    action='store_true',
    dest='tournament',
    help='execute a tournament among all agents except random')

parser.add_argument(
    '-tr',
    '--tournament_against_random',
    action='store_true',
    dest='tournament_against_random',
    help='execute a tournament of all agents against random')

parser.add_argument(
    '-p0',
    choices=PLAYERS.keys(),
    help='selects player 0',
    required=True)
parser.add_argument(
    '-p1',
    choices=PLAYERS.keys(),
    help='selects player 1',
    required=True)

parser.add_argument('-v', '--verbose', action='count',
                    default=0, help='increase log verbosity')
parser.add_argument('-d',
                    '--debug',
                    action='store_const',
                    dest='verbose',
                    const=2,
                    help='log debug messages (same as -vv)')
