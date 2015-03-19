import cmd
import threading
import subprocess
from xml.dom import minidom


class WorkerThread(threading.Thread):
    def __init__(self, name, host):
        threading.Thread.__init__(self)
        self.name = name
        self.host = host
        self.result = None

    def run(self):
        nmap_params = ['nmap', '-sV', '-n', '--open', self.host, '-oX', '-']
        process = subprocess.Popen(nmap_params, stdout=subprocess.PIPE)
        self.result, _ = process.communicate()


class Console(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "$> "
        self.work_count = 0
        self.workers = {}

    def do_exit(self, line):
        alive_threads = [(name, worker) for name, worker in self.workers.items() if worker.isAlive()]
        for name, worker in alive_threads:
            print "[!] {0:10} waiting.".format(name)
            worker.join()

    def do_EOF(self, line):
        print
        self.do_exit(line)
        return True

    def do_quit(self, line):
        self.do_exit(line)

    def emptyline(self):
        pass

    def do_scan(self, line):
        name = "worker{}".format(self.work_count)
        worker = WorkerThread(name, line)
        worker.start()
        self.work_count += 1
        self.workers[name] = worker

    def do_status(self, line):
        for name, worker in self.workers.items():
            status = "COMPLETED" if worker.result else "RUNNING"
            print "[*] {0:10} : {1:20} : {2:10}".format(name, worker.host, status)

    def do_result(self, line):
        if line in self.workers:
            worker = self.workers[line]
            if worker.result:
                xml = minidom.parseString(worker.result)
                ports = xml.lastChild.getElementsByTagName('port')
                hosts = xml.lastChild.getElementsByTagName('hosts')[0]
                host_status = "Up" if int(hosts.attributes['up'].value) else "Down"
                print "[*] Host is {}".format(host_status)
                for port in ports:
                    port_id = port.attributes['portid'].value
                    protocol = port.attributes['protocol'].value
                    print "[*] Open Port: {0:5} {1:5}".format(port_id, protocol)
            else:
                print "[*] Worker is running."

    def complete_result(self, text, line, begidx, endidx):
        if not text:
            completions = [name for name, worker in self.workers.items()]
        else:
            completions = [name for name, worker in self.workers.items() if name.startswith(text)]
        return completions

if __name__ == "__main__":
    console = Console()
    console.cmdloop()