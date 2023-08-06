from collections.abc import MutableMapping
from .fileio import ManifestMap


class MutableManifestTree(MutableMapping):
    """An abstract (but possibly concrete) representation of a collection of resources
    MMT acts much like a dict, but manages side-effects and invariants

    todo: we may want to lazily eval Resource returns in order to populate the absolute
    path on demand. Or do other side-effecty things. For now, Resource just contains
    redundant info for abspath, for simplicity

    idea: in-place file interfaces to be able to write to virtual "files" in the tree and
    then save the whole manifest. This could be useful for manipulating archives or interacting
    with a remote endpoint.
    """

    def __init__(self, base):
        self._manifest = ManifestMap(base=base, elements={})

    def __getitem__(self, key):
        """Given a relative path, return its Resource"""
        return self._manifest.elements.__getitem__(key)

    def __setitem__(self, key, resource):
        """Insert a resource"""
        self._manifest.elements.__setitem__(key, resource)

    def __delitem__(self, key):
        """Remove a resource"""
        self._manifest.elements.__delitem__(key)

    def __len__(self):
        """Count of files (not dirs) in manifest"""

    def __iter__(self):
        """Iterate over keys"""

    # def add(self, resource):
    #     """Add a resource to the tree"""
    #
    # def discard(self, element):
    #     """Remove a resource"""
    def items(self):
        yield from self._manifest.elements.items()

    def keys(self):
        """Iterates over relative paths"""

        yield from self._manifest.elements.keys()

    def values(self):
        """Iterates over Resource objects"""
        yield from self._manifest.elements.values()
