class BaseFilter():
    def __init__(self):
        pass

    def node(self, node, tags):
        return (node, ())

    def way(self, way, tags):
        return (way, ())

    def relation(self, relation, tags):
        return (relation, ())


class VersionIncrementor(BaseFilter):
    def increment_version(self, e, tags):
        if "modified" in tags:
            e.version += 1
        return (e, tags)

    def node(self, e, tags):
        return self.increment_version(e, tags)

    def way(self, e, tags):
        return self.increment_version(e, tags)

    def relation(self, e, tags):
        return self.increment_version(e, tags)
