import sys
import time
import argparse

from process_twitter import ProcessTwitter


def mainLoop(source, timeToSleep=60):
    if source == "twitter":
        processor = ProcessTwitter()
    # elif source == 'newsapi':
    #    todo
    else:
        print("No implementation found for {}".format(source), file=sys.stderr)
        return 1

    print("===================================")
    print("Start processing data from {}".format(source))
    while True:
        processor.run()
        time.sleep(timeToSleep)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("source", choices=["twitter", "newsapi"])
    parser.add_argument("seconds", type=int, help="Time in seconds between runs.")
    args = parser.parse_args()

    try:
        mainLoop(args.source, args.seconds)
    except KeyboardInterrupt:
        print("Quit on users behalf.")
        sys.exit(0)
