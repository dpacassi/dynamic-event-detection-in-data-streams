import sys
import time
import argparse

from process_twitter import ProcessTwitter


def mainLoop(source, limitRuns=None, timeToSleep=60):
    if source == "twitter":
        processor = ProcessTwitter()
    # elif source == 'newsapi':
    #    processor = ProcessNewsapi()
    else:
        print("No implementation found for {}".format(source), file=sys.stderr)
        return 1

    print("===================================")
    print("Start processing data from {}".format(source))

    runs = 0
    while limitRuns is None or limitRuns > runs:
        runs += 1
        processor.run()
        time.sleep(timeToSleep)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("source", choices=["twitter", "newsapi"])
    parser.add_argument("-t", type=int, help="Time in seconds between runs.", nargs='?', default=60)
    parser.add_argument("-l", type=int, help="Limit number of runs (default is infinite).", nargs='?')
    args = parser.parse_args()

    try:
        mainLoop(args.source, args.l, args.t)
    except KeyboardInterrupt:
        print("Quit on users behalf.")
        sys.exit(0)
