#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""RelicHunter - A File relict indexing tool

This tool uses either a given directory or a filelist to create a searchlist of
files. Then it looks for finding these files and variations of their filenames
on a given Webserver.

This can be used to test your webserver for file relicts often left by Editors.
(e.g. vim leaves files with an additional ~ in their filename).

Todo:
    * Get Extension from external fle or based on user input
    * Find more possible modiers for relicts
    * Optimize and Cleanup Code ;)


"""


import sys
import os
import argparse
import requests

__author__ = "Carsten Cordes"
__copyright__ = "Copyright 2016, Carsten Cordes"
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Carsten Cordes"
__email__ = "badagent@gmx.de"



#
# TODO: Get Extension from external fle or based on user input
#
juicy_extensions = ['.php', '.php4', '.php5', '.php6', '.php7', '.htm',
                    '.html', '.js', '.pl', '.py', '.rb', '.txt', '.cfg',
                    '.lst', '.xml', '.ini', '']

#
# TODO: Find more possible modiers for relicts
#
modifiers = ['', '~', '.bak', '.swp']


def is_juicy(filename):
    filen, ext = os.path.splitext(filename)
    if ext in juicy_extensions:
        return True
    else:
        return False


def pretty_print(some_list):
    for line in some_list:
        print line


def create_directory_index(directory, prefix):
    files = []
    for filename in os.listdir(directory + prefix):
        fullname = directory + prefix + os.sep + filename
        if(os.path.isdir(fullname)):
            files = files + create_directory_index(directory, prefix + os.sep +
                                                   filename)
        else:
            if(args.juicy):
                if not is_juicy(filename):
                    continue
            files.append(prefix + os.sep + filename)
    return files


def modify_slashes(filelist):
    modded_list = []
    for filename in filelist:
        filename = filename.replace(os.sep, '/')
        modded_list.append(filename)
    return modded_list


def strip_extension(filename):
    name_without_extension = os.path.splitext(filename)[0]
    return name_without_extension


def do_request(url):
    response = requests.get(url)
    if((response.status_code != 404 and response.status_code != 403) or
       args.verbose):
        print "[+] %s - %d - %d (bytes)" % (url, response.status_code,
                                            len(respost.content))


parser = argparse.ArgumentParser(description='Searches for Relicts of Editors \
                                              in WebApplications based on \
                                              File-List or known structure \
                                              of cms')

parser.add_argument('mode', metavar="<file|dir>", help='Set indexing mode \
                                                        (either Filelist or \
                                                        Folder)')

parser.add_argument('filelist_or_directory', metavar="<filelist|directory>",
                    help='Either Filelist or directory to create search index \
                          (depends on mode)')

parser.add_argument("baseurl", help='Base-URL of WebApplication')

parser.add_argument('-v', '--verbose', help='Verbose Mode',
                    action="store_true")

parser.add_argument('-s', '--strip', help='Additionaly try with stripped \
                                           extensions e.g. index.bak instead \
                                           of index.htm.bak',
                    action="store_true")
parser.add_argument('-l', '--storelist', help='Index directory and output \
                                               Filelist only (Instead of Url \
                                               provide output file)',
                    action="store_true")
parser.add_argument('-j', '--juicy', help='Juicy extensions only \
                                           (php, php4, php5, php6, php7, htm, \
                                           html, js, pl, py, txt, cfg, lst, \
                                           xml or None)', action="store_true")


args = parser.parse_args()

if args.verbose:
    print "[*] Using verbose mode"

args.mode = args.mode.lower()

if args.mode == 'file':
    print "[*] Loading list from File %s" % (args.filelist_or_directory)
    if(os.path.exists(args.filelist_or_directory) and
       os.path.isfile(args.filelist_or_directory)):
        filelist = []
        with open(args.filelist_or_directory, 'r') as tmp:
            for line in tmp:
                filelist.append(line.rstrip())
    else:
        print "[-] File %s does not exist." % (args.filelist_or_directory)
        print "[-] Quitting."
        sys.exit(0)

elif args.mode == 'dir':
    if(os.path.exists(args.filelist_or_directory) and
       os.path.isdir(args.filelist_or_directory)):
        # TODO String slash
        print "[*] Indexing directory %s" % (args.filelist_or_directory)
        filelist = create_directory_index(args.filelist_or_directory, '')
        filelist = modify_slashes(filelist)
        if(args.verbose):
            pretty_print(filelist)
        if(args.storelist):
            with open(args.baseurl, 'w') as tmp:
                for filename in filelist:
                    tmp.write(filename+"\n")
            print "[+] Written Indexed directory to %s" % (args.baseurl)
            print "[+] Bye."
            sys.exit(0)

    else:
        print "[-] Directory %s does not exist or \
               is no directory." % (args.filelist_or_directory)
        print "[-] Quitting."
        sys.exit(0)

else:
    print "[-] Mode must be either 'dir' or 'file'"
    print "[-] Quitting."
    sys.exit(0)

print "[*] Got Filelist. Trying to discovery files on server"

for filename in filelist:
    for modifier in modifiers:
        do_request(args.baseurl + filename + modifier)
        if(args.strip):
            do_request(args.baseurl + strip_extension(filename) + modifier)
