#!/usr/bin/env python3

import logging
import sys
import re

from osmfilter.filters import BaseFilter, VersionIncrementor
from osmfilter.filtering import run, FilteringModifier
from osmfilter.writing import OSMWriter


class WebsiteFilter(BaseFilter):
    def __init__(self):
        self.protocol_re = re.compile("^https?://")
    def clean_url(self, url):
        if not self.protocol_re.search(url):
            url = "http://" + url
        return url

    def act(self, e):
        state = FilteringModifier.discard
        for tag in ('website', 'contact:website'):
            if tag in e.tags.keys():
                state = FilteringModifier.modified
                e.tags[tag] = self.clean_url(e.tags[tag])
        return (e, state)

    def node(self, e, flags):
        return self.act(e)

    def way(self, e, flags):
        return self.act(e)

    def relation(self, e, flags):
        return self.act(e)


class PhoneFilter(BaseFilter):
    def __init__(self, writer):
        self.writer = writer

        self.parsable_re = re.compile(".*([1-9]).*?(\d).*?(\d).*?(\d).*?(\d).*?(\d).*?(\d).*?(\d).*?(\d)$")
        self.france_re = re.compile("^\+33 ?[1-9]( ?[0-9]){8}$")
    def test_phone(self, number):
        if self.france_re.match(number):
            return True
        match = self.parsable_re.search(number)
        if match:
            return "+33 {0} {1}{2} {3}{4} {5}{6} {7}{8}".format(*match.groups())
        else:
            return False

    def act(self, e):
        state = FilteringModifier.discard
        for tag in ('phone', 'contact:phone', 'fax', 'contact:fax'):
            if tag in e.tags.keys():
                new_phone = self.test_phone(e.tags[tag])
                if new_phone is True:
                    continue
                if new_phone is False:
                    self.writer.write(e)
                else:
                    state = FilteringModifier.modified
                    e.tags[tag] = new_phone

        return (e, state)

    def node(self, e, flags):
        return self.act(e)

    def way(self, e, flags):
        return self.act(e)

    def relation(self, e, flags):
        return self.act(e)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    input_file = open(input_file_path, "rb")
    output_file = open(output_file_path, "wb")

    bad_phone_file = open("bad_phone.osm", "wb")
    writer = OSMWriter(bad_phone_file)
    writer.initialize_document()

    #filters = (PhoneFilter(writer), VersionIncrementor())
    filters = (WebsiteFilter(), VersionIncrementor())

    try:
        run(input_file, output_file, filters, threads=20)
    finally:
        writer.finalize_document()
        input_file.close()
        output_file.close()
        logging.debug("Closed files")
