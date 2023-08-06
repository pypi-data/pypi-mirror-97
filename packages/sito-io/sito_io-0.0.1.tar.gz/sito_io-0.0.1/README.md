# sito-io
Standard Interfaces for Transforming Objects - File I/O

The goal of this library is to provide data structures and interfaces which are 
at least as ergonomic as existing file I/O and path primitives (`open`, `Path`, etc),
while providing strongly typed functionality to facilitate transformations of collections of
files. 

### Core concepts

#### Resource

A Resource is the core unit of abstraction. It is kind of like a sum type of a `os.Path` and `urllib.parse.ParseResult`. 
Its essence is to act as a handle to a more sophisticated resource, such as a file, directory, 
URL, endpoint, transaction, FIFO, special file, etc. 

#### Context

A Context is a Resource that can be used to "anchor" another Resource. For example, a context might be 
`http://example.com`, `/home/user`, or even `.`. A context can be: 
- Fully qualified - `file:///home/user/foo/bar`, `http://example.com/foo/bar`, `ftp://example.com/foo/bar`
- Absolute - `/home/user/foo/bar`, `/home/user/arch.tar::/foo/bar`
- Relative - `./bar` - Relative contexts must be rooted before they can be fully 
resolved
- Naive - `bar` - Naive contexts must be rooted before they can be fully resolved

#### Manifest

A Manifest is a collection of Resources. This might be files on disk (or a description thereof, it need not exist),
or files in a TAR file, or endpoints. The primary purpose is to facilitate moving collections of files atomically, 
capturing I/O of a process, and "slurping up" the data, thus allowing stateful processes to be modeled as a transaction. 
This makes a process behave less like a mutation and more like a lambda, improving referential transparency 
in pipelines. 

A Manifest can be used to generate a ManifestFile, a serialized index of the manifest. This can be packed 
with the files and give an easy handle to verify the contents of a transaction. 