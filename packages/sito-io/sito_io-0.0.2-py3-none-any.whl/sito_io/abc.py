from collections.abc import Mapping, MutableSet


class AbstractManifestTree(Mapping):
    ...


class AbstractMutableManifestTree(Mapping, MutableSet):
    ...
