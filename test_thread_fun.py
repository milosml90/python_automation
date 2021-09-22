import threading

FIRST = 'FIRST '
SECOND = 'SECOND'

def worker(thread_name):
    """thread worker function"""
    for i in range(10):
        print(thread_name)
    return


t1 = threading.Thread(target=worker, args=(FIRST,))
t2 = threading.Thread(target=worker, args=(SECOND,))
t1.start()
t1.join()
t2.start()
t2.join()
