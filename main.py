from Game import Game
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='Process arguments about an NBA game.')
parser.add_argument('--path', type=str,
                    help='a path to json file to read the events from',
                    required = True)
parser.add_argument('--event', type=int, default=0,
                    help="""an index of the event to create the animation to
                            (the indexing start with zero, if you index goes beyond out
                            the total number of events (plays), it will show you the last
                            one of the game)""")
parser.add_argument('--out', type=str,
                    help='file name out output', required = True)
                    
args = parser.parse_args()

game = Game(path_to_json=args.path, event_index=args.event)
total_shots = game.read_json()

game.start(args.out)
