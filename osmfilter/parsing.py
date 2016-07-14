from .compat import etree
from .entities import Node, Way, Relation


def parse(fp):
    context = etree.iterparse(fp, events=('end',))

    for action, elem in context:
        # Act only on node, ways and relations
        if elem.tag not in ('node', 'way', 'relation'):
            continue

        tags = {t.get('k'): t.get('v') for t in elem if t.tag == 'tag'}
        osmid = int(elem.get('id'))
        version = int(elem.get('version'))

        if elem.tag == 'node':
            e = Node(osmid, tags, version, elem.get('lat'), elem.get('lon'))
        elif elem.tag == 'way':
            nodes = [n.get('ref') for n in elem if n.tag == 'nd']
            e = Way(osmid, tags, version, nodes)
        elif elem.tag == 'relation':
            members = [(m.get('type'), m.get('ref'), m.get('role')) for m in elem if m.tag == 'member']
            e = Relation(osmid, tags, version, members)

        xml_node_cleanup(elem)
        yield e


def xml_node_cleanup(elem):
    elem.clear()
    while elem.getprevious() is not None:
        del elem.getparent()[0]
