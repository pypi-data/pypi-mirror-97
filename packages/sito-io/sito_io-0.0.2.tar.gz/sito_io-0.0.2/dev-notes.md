# Dev Notes 
Stuff that doesn't belong in README.md but I still want to keep around to track my thoughts. 

- Context should subtype Resource 
- Resource should implement __fspath__
- Resource and ManifestTree can have Context as a Context (does that mean ManifestTree is a resource?
    I think so!)
- Context objects can be shared between Resources  
- Resource should probably implement some abstract Node interface 
- Want some sort of .map(), .flatmap(), etc methods. Ideally immutable. 
- Maybe a `.mutmap()` for mutating in place.   