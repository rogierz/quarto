import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='count',
                        default=0, help='increase log verbosity')
parser.add_argument('-d',
                    '--debug',
                    action='store_const',
                    dest='verbose',
                    const=2,
                    help='log debug messages (same as -vv)')