import textwrap

from threading import Lock

from .compat import etree
from .filters import BaseFilter


class XMLWriter(BaseFilter):
    xml_header = b'''<?xml version='1.0' encoding='UTF-8'?>\n<osmChange version="0.6" generator="info.linuxw.osmfilter">\n  <modify>\n'''
    xml_footer = b'''  </modify>\n</osmChange>\n'''

    def __init__(self, output, filt):
        super().__init__()
        self.output = output
        self.items_wrote = 0
        self.lock = Lock()
        self.filt = filt

    def initialize_document(self):
        with self.lock:
            self.output.write(self.xml_header)

    def node(self, n, tags):
        if not self.filt or (self.filt and self.filt in tags):
            self.write(n)
        return (n, tags)

    def way(self, w, tags):
        if not self.filt or (self.filt and self.filt in tags):
            self.write(w)
        return (w, tags)

    def relation(self, r, tags):
        if not self.filt or (self.filt and self.filt in tags):
            self.write(r)
        return (r, tags)

    def finalize_document(self):
        with self.lock:
            self.output.write(self.xml_footer)

    def write(self, item):
        s = etree.tostring(item.toXML(), encoding='unicode', pretty_print=True)
        s = textwrap.indent(s, "    ")
        with self.lock:
            self.output.write(str.encode(s, encoding="utf-8"))


class OSCWriter(XMLWriter):
    xml_header = b'''<?xml version='1.0' encoding='UTF-8'?>\n<osmChange version="0.6" generator="info.linuxw.osmfilter">\n  <modify>\n'''
    xml_footer = b'''  </modify>\n</osmChange>\n'''


class OSMWriter(XMLWriter):
    xml_header = b'''<osm version="0.6" generator="osmfiltering" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">\n'''
    xml_footer = b'''\n</osm>\n'''
