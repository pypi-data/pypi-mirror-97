import argparse
import json
import os
import sys

from .. import jenkins
from .. import __version__


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--json", action="store_true", help="Emit JSON")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase verbosity")
    parser.add_argument("-V", "--version", action="store_true", help="Show version")
    parser.add_argument("logfile", nargs='?', help="Path to Jenkins log file")

    args = parser.parse_args()

    if args.version:
        print(__version__)
        exit(0)

    if not args.logfile:
        print(f"{os.path.basename(sys.argv[0])}: error: the following arguments are required: logfile")
        parser.print_help()
        exit(1)

    if not os.path.exists(args.logfile):
        print(f"{args.logfile}: does not exist")
        exit(1)

    if args.verbose:
        jenkins.verbose_enable()

    data = jenkins.parse_log(args.logfile)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        for x in data:
            print("#" * 79)
            print(f"{x['type']} - {x['name']} (line @ {x['line']})")
            print("#" * 79)
            print(f"{x['data']}")


if __name__ == "__main__":
    sys.exit(main())
