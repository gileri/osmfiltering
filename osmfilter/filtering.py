import logging

from threading import Thread
from queue import Queue

from .entities import Node, Way, Relation
from .writing import OSCWriter
from .parsing import parse

class FilteringModifier():
    noop = 0
    discard = 1
    modified = 2
    skip = 4

def act(actions, item):
    # TODO Pre-process actions to only call what's callable
    # TODO Allow deletion of entities

    state = FilteringModifier.noop
    for action in actions:
        if state & FilteringModifier.skip:
            break
        elif state & FilteringModifier.discard:
            return (item,state)
        item, state = getattr(action, item.__class__.__name__.lower())(item, state)

    return (item, state)


class Worker(Thread):
    # TODO use a single thread for writing files

    def __init__(self, in_queue, filters=()):
        super().__init__()
        self.in_queue = in_queue
        self.filters = filters

    def run(self):
        while True:
            input_item = self.in_queue.get()

            if input_item is None:
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
