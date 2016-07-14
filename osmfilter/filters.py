class BaseFilter():
    def __init__(self):
        pass

    def node(self, node):
        return True

    def way(self, way):
        return True

    def relation(self, relation):
        return True


class VersionIncrementor(BaseFilter):
    def increment_version(self, e):
        e.version += 1
        return e

    def node(self, e):
        return self.increment_version(e)

    def way(self, e):
        return self.increment_version(e)

    def relation(self, e):
        return self.increment_version(e)
