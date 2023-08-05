#! /usr/bin/env python
# -*- coding: utf8 -*-

"""
This conversion script converts one or more FoLiA documents to a semi-interactive HTML document for
visualisation in a web-browser.
"""


from __future__ import print_function, unicode_literals, division, absolute_import

import foliatools.xslt as xslt

def main():
    usage = """folia2html
  by Maarten van Gompel (proycon)
  Centre for Language and Speech Technology, Radboud University Nijmegen
  2016-2019 - Licensed under GPLv3

""" + __doc__ + """

Usage: folia2html [options] file-or-dir1 file-or-dir2 ..etc.."""

    xslt.main('folia2html.xsl','html',usage)

if __name__ == "__main__":
    main()
