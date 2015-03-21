import subprocess
import sys


def get_password(file_name):
    with open(file_name) as fp:
        while True:
            data = fp.readline().strip()
            if not data:
                break
            yield data


def steghide_cracker(file_name, password):
    steghide_cmd = ["steghide", "extract", "-sf", file_name, "-p", password]
    process = subprocess.Popen(steghide_cmd, stdout=subprocess.PIPE)
    result, _ = process.communicate()
    if "extracted" in result:
        print "[*] Password cracked: {}".format(password)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "[*] Usage: {} <file_name> <wordlist>".format(__file__)
    else:
        file_name = sys.argv[1]
        wordlist = sys.argv[2]
        passwords = get_password(wordlist)
        for password in passwords:
            steghide_cracker(file_name, password)