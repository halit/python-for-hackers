def get_password(file_name):
    with open(file_name) as fp:
        while True:
            data = fp.readline()
            if not data:
                break
            yield data

passwords = get_password('rockyou.txt')
for password in passwords:
    print password
