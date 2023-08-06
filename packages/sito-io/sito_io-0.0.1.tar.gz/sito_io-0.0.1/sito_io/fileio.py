from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, FilePath, DirectoryPath, AnyUrl

from sito_io.dctypes.resource import UriKind, Resource

UriT = Union[FilePath, AnyUrl]
OptionsT = Optional[Union[Dict[str, str], List[Tuple[str, str]], List[str]]]
# todo: pending optional directories for output dirs that will be created,
# see: https://github.com/samuelcolvin/pydantic/issues/1254
# https://github.com/samuelcolvin/pydantic/issues/1983


class Manifest(BaseModel):
    """A loose collection of elements"""

    base: Union[DirectoryPath, AnyUrl, Path]  # base of the manifest tree
    kind: UriKind = UriKind.Naive  # how is the manifest rooted?
    elements: List[Resource]  # manifest contents


class ManifestMap(BaseModel):
    """A Manifest which can be addressed by the relative paths"""

    base: Union[DirectoryPath, AnyUrl, Path]  # base of the manifest tree
    kind: UriKind = UriKind.Naive  # how is the manifest rooted?
    elements: Dict[Path, Resource]  # manifest contents


class SitoFileToFile(BaseModel):
    """File-in, file-out. Takes a single file (or URI), emits a single file (or URI) """

    input_uri: UriT
    output_uri: Optional[Union[FilePath, AnyUrl, str]]
    options: OptionsT


class SitoDirToDir(BaseModel):
    """Directory-in, directory-out. """

    input_dir: DirectoryPath
    output_dir: Optional[Union[DirectoryPath, str]]
    options: OptionsT


class SitoFileToDir(BaseModel):
    """Single file in, directory of files out. """

    input_uri: UriT
    output_dir: Optional[Union[DirectoryPath, str]]
    options: OptionsT


class SitoCoreUtil(BaseModel):
    """Emulates the interface of common coreutils tools, mv, tar, etc. E.g.:
    tool [options] [output] <input> [inputs...]"""

    inputs: List[UriT]
    output: Optional[UriT]
    options: OptionsT
