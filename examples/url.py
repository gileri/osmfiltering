#!/usr/bin/env python3

import logging
import sys
import re

from osmfiltering.filters import BaseFilter, VersionIncrementor
from osmfiltering.filtering import run
from osmfiltering.writing import OSMWriter


class WebsiteFilter(BaseFilter):
    def __init__(self):
        self.protocol_re = re.compile("^https?://")

    def clean_url(self, url):
        if not self.protocol_re.search(url):
            url = "http://" + url
        return url

    def act(self, e, tags):
        tags = []
        for tag in ('website', 'contact:website'):
            if tag in e.tags.keys():
                tags = ["modified"]
                e.tags[tag] = self.clean_url(e.tags[tag])
        return (e, tags)

    def node(self, e, tags):
        return self.act(e, tags)

    def way(self, e, tags):
        return self.act(e, tags)

    def relation(self, e, tags):
        return self.act(e, tags)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    input_file = open(sys.argv[1], "rb")
    output_file = open(sys.argv[2], "wb")
    bad_phone_file = open(sys.argv[3], "wb")

    writer = OSMWriter(output_file, "modified")
    check_writer = OSMWriter(bad_phone_file, "check")
    writer.initialize_document()
    check_writer.initialize_document()

    filters = (WebsiteFilter(), VersionIncrementor(), writer, check_writer)

    try:
        run(input_file, output_file, filters, threads=20)
    finally:
        writer.finalize_document()
        input_file.close()
        output_file.close()
        logging.debug("Closed files")
