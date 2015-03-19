import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser("tool", description="My Perfect Tool")
    parser.add_argument("--server", "-s", help="Run the server", action="store_true")
    parser.add_argument("--port", "-p", help="Set the server port number", type=int, default=8000)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        pass