# linkchecker-third-twin

Find the links that occur more than once in  any DITA topic file. A link might have been inserted manually as an `xref` or `related-links` tag, or generated automatically during the DITA build through the `collection type` attribute or a `reltable` entry.

For any specified directory, this script checks all of the links in a DITA files and maps. It identifies cross-references that occur more than once, and reports them.  

Relationship tables, topicref collections, inline cross-references, and links in the related-links tag are all reckoned.

## Usage instructions

#### Prerequisite

Download and install Python 2.7.5. Later versions of Python should work.

#### Steps

1. Download this entire repository as a `.zip` file, extract the contents to any folder, and double-click `third_twin.py`.
2. When prompted, enter the full path of the directory to be scanned, for example, `c:\documentation`.
3. When the checking is complete, you see a message on the console: `Press any key to exit.` Press any key.
4. Go to the folder where the script resides. You see a file called `RepeatedLinks.html`. This is the report file for you to read and act upon.  

## Limitations

The script assumes that all DITA topic files have the `.dita` extension and all DITA map files have the `.ditamap` extension. If your files are `.xml` files, this script will not work.

## Bugs and enhancements

Use GitHub's issue tracking feature.

## Licensing

The script is under [GPL 3](https://opensource.org/licenses/GPL-3.0), which is a copyleft licence. You are free to use and distribute this code as-is. You are also free to modify and distribute this code provided you distribute such modified code in its entirety under the same licence as this one, that is GPL 3.
