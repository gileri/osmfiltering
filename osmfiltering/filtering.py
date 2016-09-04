import logging

from threading import Thread
from queue import Queue

from .parsing import Reader


class Worker(Thread):
    # TODO use a single thread for writing files

    def __init__(self, in_queue, filters=()):
        super().__init__()
        self.in_queue = in_queue
        self.filters = filters

    def run(self):
        while True:
            tags = []
            item = self.in_queue.get()

            if item is None:
                break

            # TODO Pre-process actions to only call what's callable
            # TODO Allow deletion of entities

            for action in self.filters:
                if "discard" in tags:
                    continue
                item, tags = getattr(action, item.__class__.__name__.lower())(item, tags)


def run(input_file, output_file, filters=(), threads=4, finalize_xml=True):
    logging.info("Starting")

    in_queue = Queue(maxsize=300)

    reader = Reader(input_file, in_queue)
    logging.info("Started parsing")
    reader.start()

    workers = []
    for _ in range(threads):
        t = Worker(in_queue, filters)
        workers.append(t)
        t.start()

    reader.join()
    logging.info("Finished parsing")

    for _ in range(len(workers)):
        in_queue.put(None)

    for w in workers:
        w.join()
