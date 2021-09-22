import threading

FIRST = 'FIRST '
SECOND = 'SECOND'

class worker(threading.Thread):
    def __init__(self, thread_name):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.start()

    def run(self):
        """thread worker function"""
        for i in range(10):
            print(self.thread_name)
        return

t1 = worker(FIRST)
t1.join()
t2 = worker(SECOND)
t2.join()