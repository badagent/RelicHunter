# RelicHunter
## A File relict indexing tool

This tool uses either a given directory or a filelist to create a searchlist of
files. Then it looks for finding these files and variations of their filenames
on a given Webserver.

This can be used to test your webserver for file relicts often left by Editors.
(e.g. vim leaves files with an additional ~ in their filename).

### Todo:
    - Get Extension from external fle or based on user input
    - Find more possible modiers for relicts
    - Optimize and Cleanup Code ;)

### Dependencies:
    - Python 2.7
    - Python Argparse
    - Python Requests

===============================
'''
usage: hunt.py [-h] [-v] [-s] [-l] [-j]
               <file|dir> <filelist|directory> baseurl

Searches for Relicts of Editors in WebApplications based on File-List or known
structure of cms

positional arguments:
  <file|dir>            Set indexing mode (either Filelist or Folder)
  <filelist|directory>  Either Filelist or directory to create search index
                        (depends on mode)
  baseurl               Base-URL of WebApplication

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose Mode
  -s, --strip           Additionaly try with stripped extensions e.g.
                        index.bak instead of index.htm.bak
  -l, --storelist       Index directory and output Filelist only (Instead of
                        Url provide output file)
  -j, --juicy           Juicy extensions only (php, php4, php5, php6, php7,
                        htm, html, js, pl, py, txt, cfg, lst, xml or None)
'''
