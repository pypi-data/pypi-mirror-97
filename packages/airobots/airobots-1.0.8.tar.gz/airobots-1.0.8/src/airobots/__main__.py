import argparse
import os
import sys
import pytest
from airobots import __description__, __version__
from httprunner.cli import main_run
from airtest.core.settings import Settings as ST


def main():
    """ API test: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-v", "--version", dest="version", action="store_true", help="show version"
    )
    parser.add_argument(
        "-t", "--type", dest="test type", required=True, default='api', choices=['api', 'web', 'ios', 'android'], help="auto test type, api, web, ios, android"
    )
    parser.add_argument(
        "-r", "--remote-url", dest="remote url", default=None, help="web test's remote url, eg. http://localhost:4444/wd/hub"
    )
    if len(sys.argv) == 1:
        # httprunner
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        # print help for sub-commands
        if sys.argv[1] in ["-v", "--version"]:
            # httprunner -V
            print(f"{__version__}")
        else:
            parser.print_help()
        sys.exit(0)
    elif (
        len(sys.argv) == 3 and sys.argv[1] in ["-t", "--type"] and sys.argv[2] in ['api', 'web', 'ios', 'android']
    ):
        # httprunner run -h
        pytest.main(["-h"])
        sys.exit(0)
    elif (
        len(sys.argv) == 4 and sys.argv[1] in ["-t", "--type"] and sys.argv[2] in ['api', 'web', 'ios', 'android'] and sys.argv[3] in ["-r", "--remote-url"]
    ):
        parser.print_help()
        sys.exit(0)

    extra_args = []
    if len(sys.argv) >= 2:
        args, extra_args = parser.parse_known_args()
    else:
        args = parser.parse_args()

    if args.version:
        print(f"{__version__}")
        sys.exit(0)

    if sys.argv[2] == "api":
        sys.exit(main_run(extra_args))
    elif sys.argv[2] in ['web', 'ios', 'android']:
        if len(sys.argv) == 6: ST.REMOTE_URL = sys.argv[4] or None
        ST.LOG_DIR = os.path.join('Results', 'log')
        if not os.path.exists(ST.LOG_DIR): os.makedirs(ST.LOG_DIR)
        sys.exit(pytest.main(extra_args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()