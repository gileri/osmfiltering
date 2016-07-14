import logging

from threading import Thread
from queue import Queue

from .entities import Node, Way, Relation
from .writing import Writer
from .parsing import parse


def act(actions, item):
    # TODO Pre-process actions to only call what's callable
    # TODO Allow deletion of entities

    for action in actions:
        if item is False:
            # Deletion requested
            return False
        if item is True:
            # No action made by filter
            continue
        item = getattr(action, item.__class__.__name__.lower())(item)

    return item


class Worker(Thread):
    # TODO use a single thread for writing files
    def __init__(self, in_queue, writer, filters=()):
        super().__init__()
        self.in_queue = in_queue
        self.writer = writer
        self.filters = filters

    def run(self):
        while True:
            input_item = self.in_queue.get()

            if input_item is None:
                break

            output_item = act(self.filters, input_item)

            if not isinstance(output_item, bool):
                # TODO allow deletion
                self.writer.write(output_item)


def run(input_file, output_file, filters=(), threads=4):
    logging.info("Starting")
    writer = Writer(output_file)
    writer.initialize_document()

    in_queue = Queue(maxsize=300)

    workers = []
    for i in range(threads):
        t = Worker(in_queue, writer, filters)
        workers.append(t)
        t.start()

    for i in parse(input_file):
        in_queue.put(i)
    logging.info("Finished parsing")

    for i in range(len(workers)):
        in_queue.put(None)

    for w in workers:
        w.join()

    writer.finalize_document()
    logging.info("Terminating")
