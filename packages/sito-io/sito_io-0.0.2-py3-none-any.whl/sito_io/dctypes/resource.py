#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A pure python implementation of the Resource interface, based on dataclasses
"""

import os
import json
from typing import Optional, Union, Dict
from enum import Enum
from urllib.parse import urlsplit, SplitResult
from pathlib import Path
import dataclasses


class ResourceKind(Enum):
    Naive = 0  # we don't know how it's rooted
    Relative = 1  # it's a relative tree, base may lack context
    Absolute = 2  # it's a local absolute path
    FullyQualified = 3  # base is a full URI with scheme
    # todo: relative http urls?


class LocationKind(Enum):
    Naive = 0  # we don't know how it's stored
    Local = 1  # it's a local file we can immediately open
    Archive = 2  # represents part of an archive tar/zip/etc
    Network = 3  # it's a network resource with a protocol
    NoProtoFile = 4  # it's a file but it is not local (no access scheme)


class UnrootedResource(Exception):
    ...


def kind_from_uriparts(parts: SplitResult) -> ResourceKind:
    if parts.scheme:
        return ResourceKind.FullyQualified
    elif os.path.isabs(parts.path):
        return ResourceKind.Absolute
    else:
        return ResourceKind.Relative


def location_kind_from_uriparts(parts: SplitResult) -> LocationKind:
    # todo: archive?
    if parts.scheme == "":
        return LocationKind.Local
    elif parts.scheme == "file":
        if parts.netloc in ("", "localhost"):
            return LocationKind.Local
        return LocationKind.NoProtoFile
    else:
        return LocationKind.Network


def path_from_file_uri(uri: str) -> str:
    """Convert a file URI to a local path. Idempotent on regular paths.
    Raises if presented with a scheme besides file://
    """
    if uri.startswith("file://"):
        return uri.replace("file://", "")

    if "://" in uri:
        raise ValueError(f"Cannot convert URI to path: {uri}")
    return uri


@dataclasses.dataclass(frozen=True)
class Resource(object):
    """Describes some local or remote resource"""

    uri: str
    id: Optional[str] = ""  # some abstract identifier
    type: str = ""  # mimetype
    attrs: Dict[str, str] = dataclasses.field(default_factory=dict)
    meta: str = ""
    kind: ResourceKind = dataclasses.field(default=ResourceKind.Naive, init=True)
    location_kind: LocationKind = dataclasses.field(
        default=LocationKind.Naive, init=True
    )
    _parts: SplitResult = dataclasses.field(init=False, repr=False)

    def __post_init__(self):
        if isinstance(self.uri, Resource):
            object.__setattr__(self, "uri", str(self.uri.uri))
        parts = urlsplit(self.uri)
        object.__setattr__(self, "_parts", parts)
        object.__setattr__(self, "kind", kind_from_uriparts(parts))
        object.__setattr__(self, "location_kind", location_kind_from_uriparts(parts))

    def __str__(self):
        return self.uri

    def retrieve(self, filename=None, reporthook=None, data=None) -> "LocalResource":
        import urllib

        path, meta = urllib.request.urlretrieve(
            self.uri, filename=filename, reporthook=reporthook, data=data
        )
        assert os.path.isfile(path)
        attrs = self.attrs.copy()
        attrs.update(
            {
                "user.origin.uri": self.uri,
                "user.charsets": json.dumps(meta.get_charsets()),
            }
        )
        path = "file://" + path
        return LocalResource(
            path,
            id=self.id,
            type=meta.get_content_type(),
            attrs=attrs,
            kind=ResourceKind.FullyQualified,
            location_kind=LocationKind.Local,
        )

    def is_localized(self):
        """Path is resolvable as a local resource, NOT necessarily existing locally"""
        if self.kind in (ResourceKind.Absolute, ResourceKind.Relative):
            # todo: I dunno if I wanna deal with relative squirrelyness here
            return True

        elif self.kind is ResourceKind.FullyQualified:
            if self.location_kind in (LocationKind.Local, LocationKind.Archive):
                return True

        return False

    def __fspath__(self):
        if self.is_localized():
            return self._parts.path
        raise UnrootedResource(f"Cannot resolve absolute path: {self.uri}")


class LocalResource(Resource):
    def is_localized(self):
        return True

    def path(self) -> Path:
        return Path(self._parts.path)
