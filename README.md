# linkchecker-third-twin

The script reports links that occur more than once in  any DITA topic file. A link might have been inserted manually as an `xref` link or `related-links` link, or generated automatically during the DITA build through the `collection type` attribute or a `reltable` entry.

For any specified directory, the script checks all links in a DITA file, and all links in DITA maps. It identifies cross-references that occur more than once, and reports them.  

Relationship tables, topicref collections, inline Xrefs, links in the related-links tag are all reckoned.

## Usage instructions

To run the script, you need Python 2.7.5. Later versions of Python should also be able to run the script.

1. Download the script to any folder on your computer. Double-click the script.
2. When prompted, enter the full path of the directory to be scanned, for example, c:\documentation.
3. When the checking is complete, you see a message on the console: "Press any key to exit." Press any key.
4. Go to the folder where you saved the script. You see a file called `RepeatedLinks.html`. This is the report file for you to read and act upon.  

## Limitations

The script assumes that all DITA topic files have the `.dita` extension and all DITA map files have the `.ditamap` extension. If your files are `.xml` files, this script will not work.
