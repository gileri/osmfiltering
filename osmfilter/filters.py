from .filtering import FilteringModifier

class BaseFilter():
    def __init__(self):
        pass

    def node(self, node, flags):
        return (node, FilteringModifier.noop)

    def way(self, way, flags):
        return (way, FilteringModifier.noop)

    def relation(self, relation, flags):
        return (relation, FilteringModifier.noop)


class VersionIncrementor(BaseFilter):
    def increment_version(self, e, flags):

        if flags & FilteringModifier.modified:
            e.version += 1
            return (e, FilteringModifier.modified)
        else:
            return (e, FilteringModifier.noop)

    def node(self, e, flags):
        return self.increment_version(e, flags)

    def way(self, e, flags):
        return self.increment_version(e, flags)

    def relation(self, e, flags):
        return self.increment_version(e, flags)
