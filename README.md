![license: GPL 3.0](https://img.shields.io/badge/license-GPL%203.0-lightgrey.svg)  ![python 3.7](https://img.shields.io/badge/python-3.7.0-blue.svg)

# linkchecker-third-twin

Find the links that occur more than once in  any DITA topic file. A link might have been inserted manually as an `xref` or `related-links` tag, or generated automatically during the DITA build through the `collection type` attribute or a `reltable` entry.

For any specified directory, this script checks all of the links in a DITA files and maps. It identifies cross-references that occur more than once, and reports them.  

Relationship tables, topicref collections, inline cross-references, and links in the related-links tag are all reckoned.

## Usage scenario

When DITA topics are transformed to HTML, the following links are auto-generated and inserted inside the topic:

- Links to nested `topicref` elements in a DITA map file
- Links to topics in the same row in a relationship table

Additionally, DITA topics might have the following links inserted manually in the topic:

- Through an `xref` tag
- Through the `related-links` tag

The net effect is, after the transforms, a topic might contain a link to the same target more than once. Maybe yours is a multi-writer team, maybe you inherited the files and haven't done a link check, maybe you yourself linked to a topic twice: once through a `.ditamap` file and once again through an in-topic related link.

This script will find all such links: links that occur more than once in a topic. The script will, then, generate a report for you. Read the report and delete the extra insertions.

## Documentation

See [Anin's Documentation Tools](https://doc-tools.readthedocs.io/en/latest/).
 
## Limitations

It is assumed that all DITA topic files have the `.dita` extension. If your files use the `.xml` extension, this script will not work in its present form.

## Acknowledgments

The code was converted from `.py` to `.exe` through [auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe).

## Licensing

The script is under [GPL 3](https://opensource.org/licenses/GPL-3.0), which is a copyleft licence. You are free to use and distribute this code as-is. You are also free to modify and distribute this code provided you distribute such modified code in its entirety under the same licence as this one, that is GPL 3.