#!/usr/bin/env python3

import logging
import sys
import re

from osmfiltering.filters import BaseFilter, VersionIncrementor
from osmfiltering.filtering import run
from osmfiltering.writing import OSMWriter, OSCWriter


class PhoneFilter(BaseFilter):
    def __init__(self):
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

    def act(self, e, tags):
        for tag in ('phone', 'contact:phone', 'fax', 'contact:fax'):
            if tag in e.tags.keys():
                new_phone = self.test_phone(e.tags[tag])
                if new_phone is True:
                    continue
                if new_phone is False:
                    tags.append("check")
                else:
                    tags.append("modified")
                    e.tags[tag] = new_phone

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

    writer = OSCWriter(output_file, "modified")
    check_writer = OSMWriter(bad_phone_file, "check")
    writer.initialize_document()
    check_writer.initialize_document()

    filters = (PhoneFilter(), VersionIncrementor(), writer, check_writer)

    try:
        run(input_file, output_file, filters, threads=20)
    finally:
        writer.finalize_document()
        input_file.close()
        output_file.close()
        logging.debug("Closed files")
