import queue
from threading import Thread


class TaskQueue(queue.Queue):

    def __init__(self, num_workers=1):
        queue.Queue.__init__(self)
        self.num_workers = num_workers
        self.workers = []
        # self.start_workers()

    def add_task(self, task):
        if not 'args' in task:
            task['args'] = {}

        # self.put(task)
        self.execute(task)

    def start_workers(self):
        for i in range(self.num_workers):
            # worker_thread = Process(target=self.worker)
            worker_thread = Thread(target=self.worker)
            worker_thread.daemon = True
            worker_thread.start()
            self.workers.append(worker_thread)

    def stop_workers(self):
        for worker_thread in self.workers:
            try:
                pass
                # worker_thread
            except Exception as e:
                pass

    def worker(self):
        while True:
            task = self.get()
            self.execute(task)

    def execute(self, task):
        fn = task['fn']
        args = task['args']

        result = fn(**args)
        # self.task_done()

        # handle the callback when exist
        if 'callback' in task:
            task['callback'](result)