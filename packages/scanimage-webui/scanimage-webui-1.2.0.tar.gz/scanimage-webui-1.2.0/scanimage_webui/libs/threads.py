import time
from threading import Thread


class CommonThread (Thread):
    def __init__(self, thread_id, thread_function, thread_kwars={}):
        super().__init__()
        self.thread_id = thread_id
        self.thread_function = thread_function
        self.thread_kwargs = thread_kwars
        self.thread_data = None
        self.thread_finished = False

    def run(self):
        print("{}: Starting ".format(self.thread_id))
        self.thread_data = self.thread_function(**self.thread_kwargs)
        self.thread_finished = True
        print("{}: Exiting ".format(self.thread_id))


class CommonThreadManager:
    POOL_SIZE = 5

    def __init__(self):
        self.thread_pool = []
        self.threads = []

    def add_thread(self, t):
        self.threads.append(t)

    def execute_threads(self):
        for thr in self.threads:
            thr.start()
        while True:
            if all([_.thread_finished for _ in self.threads]):
                break
            time.sleep(0.1)
