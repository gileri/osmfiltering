from .compat import etree

# TODO Extract XML processing from here


class OSMEntity():
    def __init__(self, osmid, tags, version):
        self.tags = tags
        self.osmid = osmid
        self.version = version

    def add_common_XML(self, root):
        root.set('id', str(self.osmid))
        root.set('version', str(self.version))

        for key, value in self.tags.items():
            t = etree.SubElement(root, "tag")
            t.set("k", key)
            t.set("v", value)
        return root


class Node(OSMEntity):
    def __init__(self, osmid, tags=(), version=-1, lat=0, lon=0):
        super().__init__(osmid, tags, version)
        self.lat = lat
        self.lon = lon

    def toXML(self):
        root = super().add_common_XML(etree.Element('node'))
        for prop in ("lat", "lon"):
            root.set(prop, getattr(self, prop))
        return root


class Way(OSMEntity):
    def __init__(self, osmid, tags=(), version=-1, nodes=[]):
        super().__init__(osmid, tags, version)
        self.nodes = nodes

    def toXML(self):
        root = super().add_common_XML(etree.Element('way'))
        for ref in self.nodes:
            nd = etree.SubElement(root, "nd")
            nd.set('ref', ref)
        return root


class Relation(OSMEntity):
    def __init__(self, osmid, tags=(), version=-1, members=[]):
        super().__init__(osmid, tags, version)
        self.members = members

    def toXML(self):
        root = super().add_common_XML(etree.Element('relation'))
        for osmtype, ref, role in self.members:
            m = etree.SubElement(root, "nd")
            m.set('type', osmtype)
            m.set('ref', ref)
            m.set('role', role)
        return root
