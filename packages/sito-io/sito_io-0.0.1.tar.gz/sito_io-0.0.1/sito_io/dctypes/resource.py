from enum import Enum
from pathlib import Path
from typing import Optional, Union, Dict

from pydantic import BaseModel, FilePath, AnyUrl

from sito_io.errors import UnrootedResource


class UriKind(Enum):
    """Describes the kind of URI. URIs exist on a continuum, from simply a uniform identifier,
    to a fully-qualified URL.
    """
    Naive = 0  # we don't know anything really, it's just some identifier
    Urn = 1  # it's a Uniform Resource Name, the red-headed stepchild of the URI family
    Relative = 2  # it's a relative URI, we can resolve iff we have context
    Absolute = 3  # it's an absolute path, with the implication of locality, but not necessarily local file system
    FullyQualified = 4  # base is a full URI with scheme


class LocationKind(Enum):
    """Describes where to actually find the resource"""
    Naive = 0  # we don't know how it's stored
    Abstract = 1  # it's not really a tangible thing, more of a concept, such as a Graph
    LocalArtifact = 2  # it's a local file we can immediately open
    ArchiveArtifact = 3  # represents part of an archive tar/zip/etc
    Network = 4  # it's a local absolute path


class ResourceKind(Enum):
    """Describes what the resource actually is.
    Artifact is a file/directory, or blob of bytes. It is basically anything you could "rsync".
    """
    Naive = 0  # we don't know what it is yet
    Artifact = 1  # a file or directory, existing on some filesystem, somewhere.
    File = 2  # a file on a filesystem
    Directory = 3  # a directory on a filesystem


class Resource(BaseModel):
    """ A Resource is anything identified by a Uniform Resource Identifier.
    For those who don't like recursive definitions, a Resource is a logical or physical resource used by
    web technologies. URIs may be used to identify anything, including real-world objects, such as people and places,
    concepts, or information resources such as web pages and books.
    URIs are UNIFORM, not UNIVERSAL, meaning they have a specific structure. They may be fully qualified or relative.
    A URL is a uniform resource locator. All URLs are URIs, but not all URIs are URLs. Relative URIs and
    URNs are URIs without a strict locator, but they can be resolved to URLs.
    """

    id: Optional[str]  # some abstract identifier
    uri: Union[FilePath, AnyUrl, Path]
    type: str = ""  # mimetype
    kind: UriKind = UriKind.Naive
    attrs: Dict[str, str] = {}
    meta: str = ""

    def is_localized(self):
        """Path is resolvable as a local resource, NOT necessarily existing locally"""
        if self.kind in (UriKind.Absolute, UriKind.Relative):
            # todo: I dunno if I wanna deal with relative squirrelyness here
            return True

        elif self.kind is UriKind.FullyQualified:
            if self.uri.startswith('file://'):
                return True

    def __fspath__(self):
        if self.is_localized():
            return str(self.uri)
        raise UnrootedResource(f"Cannot resolve absolute path: {self.uri}")