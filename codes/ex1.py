import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "[*] Usage: {} <parameter>".format(__file__)
    else:
        print "[*] {}".format(sys.argv[1])