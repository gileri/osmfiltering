import textwrap

from .compat import etree
from threading import Lock


class Writer():
    osc_header = b'''<?xml version='1.0' encoding='UTF-8'?>\n<osmChange version="0.6" generator="info.linuxw.osmfilter">\n  <modify>\n'''
    osc_footer = b'''  </modify>\n</osmChange>\n'''

    def __init__(self, output):
        self.output = output
        self.items_wrote = 0
        self.lock = Lock()

    def initialize_document(self):
        with self.lock:
            self.output.write(self.osc_header)

    def finalize_document(self):
        with self.lock:
            self.output.write(self.osc_footer)

    def write(self, item):
        s = etree.tostring(item.toXML(), encoding='unicode', pretty_print=True)
        s = textwrap.indent(s, "    ")
        with self.lock:
            self.output.write(str.encode(s, encoding="utf-8"))


