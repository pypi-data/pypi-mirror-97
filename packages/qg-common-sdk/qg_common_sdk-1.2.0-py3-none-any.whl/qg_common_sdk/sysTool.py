import os
from multiprocessing import Process, Manager
import socket


def omit(target: dict,  *args):
    return dict(list(filter(lambda x: not x[0] in args, target.items())))


def find(func, array):
    for item in array:
        if func(item):
            return item
    return None


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def process_run(queue, callback):
    for i in iter(queue.get, 'STOP'):
        callback(i)


class ProcessExec():

    def __init__(self, callback):
        self._callback = callback
        self._p_list = []

    def start(self):
        self._manager = Manager()
        self.queue = self._manager.Queue()
        for i in range(os.cpu_count()):
            p = Process(target=process_run, args=(
                self.queue, self._callback))
            p.start()
            self._p_list.append(p)
        return self

    def put(self, body):
        self.queue.put(body)

    def join(self):
        for p in self._p_list:
            self.queue.put('STOP')
        for p in self._p_list:
            p.join()

    def shutdown(self):
        self._manager.shutdown()

    def _process_run(self, queue, callback):
        for i in iter(queue.get, 'STOP'):
            callback(i)

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.join()
        self.shutdown()
