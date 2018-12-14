# RTB-Ontology-Release-Tools
Tools and guidelines for creating releases for RTB ontologies.

## Ontology Release Versioning Guidelines
Ontology release tags should follow the format `v{a}.{b}.{c}` where `{a}`, `{b}`, and `{c}` are the major, minor, and patch versions, respectively (e.g. `v1.27.5`). The versioning scheme of this repository roughly follows [semantic versioning v2.0.0](https://semver.org/):


> Given a version number MAJOR.MINOR.PATCH, increment the:  
>     MAJOR version when you make incompatible API changes,  
>     MINOR version when you add functionality in a backwards-compatible manner, and.  
>     PATCH version when you make backwards-compatible bug fixes.  

This is applied in the following fashion:

### Patch

> From SemVer v2.0.0: Patch version Z (x.y.Z | x > 0) MUST be incremented if only backwards compatible bug fixes are introduced. A bug fix is defined as an internal change that fixes incorrect behavior.

Patch versions **must not introduce, modify, or remove** terms, relationships, or relationship types. Patch version must not modify original _meaning_ of existing content.

The following are examples of patch-level changes:

- Fixing a typo in a term definition
- Clarifying term definitions or names

The following are NOT examples of patch-level changes:

- Introduction of a new synonym
- Modifying an existing but incorrect `is_a` relationship.

### Minor

> From SemVer v2.0.0: Minor version Y (x.Y.z | x > 0) MUST be incremented if new, backwards compatible functionality is introduced to the public API. It MUST be incremented if any public API functionality is marked as deprecated. It MAY be incremented if substantial new functionality or improvements are introduced within the private code. It MAY include patch level changes. Patch version MUST be reset to 0 when minor version is incremented.

Minor versions **may introduce** new terms, relationships, or relationship types. Minor versions **must not modify or remove** existing terms, relationships, or relationship types. Minor versions must not modify original _meaning_ of existing content.

The following are examples of minor-level changes:

- Introduction of a new trait
- Introduction of a new relationship types
- Introduction of a new relationship `is_a` to a new trait
- Introduction of a new synonym

The following are NOT examples of minor-level changes:

- Introduction of an `is_a` relationship to an existing trait. (This modifies the meaning of the trait)
- Modifying an existing but incorrect `is_a` relationship.


### Major

> From SemVer v2.0.0: Major version X (X.y.z | X > 0) MUST be incremented if any backwards incompatible changes are introduced to the public API. It MAY include minor and patch level changes. Patch and minor version MUST be reset to 0 when major version is incremented.

Major versions **may introduce, remove, or modify** new terms, relationships, or relationship types.  Major versions **may modify original _meaning_** of existing content.

The following are examples of major-level changes:

- Introduction of an `is_a` relationship to an existing trait.
- Removing a trait or relationship.
- Modifying an existing synonym. 
- Modifying an existing but incorrect `is_a` relationship.
