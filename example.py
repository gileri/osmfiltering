#!/usr/bin/env python3

from osmfilter.filters import BaseFilter, VersionIncrementor
from osmfilter.filtering import run
import logging
import sys


class WebsiteFilter(BaseFilter):
    def website(self, e):
        modified = False
        for tag in ('website', 'contact:website'):
            if tag in e.tags.keys():
                modified = True
                e.tags[tag] = "Modified"
        if modified:
            e.version += 1
            return e
        else:
            return True

    def node(self, e):
        return self.website(e)

    def way(self, e):
        return self.website(e)

    def relation(self, e):
        return self.website(e)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    input_file = open(input_file_path, "rb")
    output_file = open(output_file_path, "wb")

    filters = (WebsiteFilter(), VersionIncrementor())

    try:
        run(input_file, output_file, filters, threads=20)
    finally:
        input_file.close()
        output_file.close()
        logging.debug("Closed files")
