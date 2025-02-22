#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - "GoogleSitemap" action

    This action generates a google sitemap file when called using /?action=GoogleSitemap
    This module can also be called from the command line to generate a sitemap file
    that can be served directly when using a webserver such as Apache.
    

    @copyright: 2000-2005 by Alan Snelson <Alan@Wave2.co.uk>
    @license: GNU GPL, see COPYING for details.
"""
__version__ = "0.3"
import sys, os, time, gzip
import xml.sax.saxutils
from MoinMoin import config, util, wikiutil
from MoinMoin.Page import Page
from MoinMoin.scripts import _util
from MoinMoin.request import RequestCLI

def execute(pagename, request):
    """
    Entry point for action when called via MoinMoin wiki.
    
    @type  pagename: pagename
    @param pagename: name of page requested along with action.
    @type  request: request
    @param request: request object.
    """
    request.http_headers(["Content-Type: application/xml"])

    # Get list of user readable pages
    pages = request.rootpage.getPageList()
    pages.sort()

    request.write('<?xml version="1.0" encoding="%s"?>\r\n' % (config.charset,))
    request.write('<urlset xmlns="http://www.google.com/schemas/sitemap/0.84">\r\n')
    for name in pages:
        #ignore system pages        
	if wikiutil.isSystemPage(request, name):
	    continue
	request.write('<url>\r\n')
	request.write('<loc>%s</loc>\r\n' % (xml.sax.saxutils.escape(request.getBaseURL()+'/'+name),))
        request.write('<lastmod>%s</lastmod>\r\n' % (util.TranslateCDATA(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.strptime(Page(request,name).lastEditInfo()["time"], "%Y-%m-%d %H:%M:%S"))),))
	request.write('</url>\r\n')
    request.write('</urlset>\r\n')

    raise util.MoinMoinNoFooter

class GoogleSitemap(_util.Script):
    """
    Command line script to generate a Google Sitemap.
    """
    def __init__(self):
        _util.Script.__init__(self,__name__,"[options] <target-directory>")
        self.parser.add_option(
            "--config-dir", metavar="DIR", dest="config_dir",
            help=("Path to the directory containing the wiki "
                "configuration files. [default: current directory]")
        )
        self.parser.add_option(
            "--base-url", metavar="BASEURL", dest="base_url",
            help=("URL to be prefixed to all pages for indexing "
                "e.g. http://www.mywiki.com")
        )

    def mainloop(self):
        """
        Main function for command line script.
        """
        if len(sys.argv) == 1:
            self.parser.print_help()
            sys.exit(1)

        outputdir = self.args[0]       
 
        # Insert config dir or the current directory to the start of the path. 
        config_dir = self.options.config_dir
        if config_dir and os.path.isfile(config_dir):
             config_dir = os.path.dirname(config_dir)
        if config_dir and not os.path.isdir(config_dir):
            _util.fatal("bad path given to --config-dir option")
        sys.path.insert(0, os.path.abspath(config_dir or os.curdir))

        # Create request
        request = RequestCLI()
        
        # Get all existing pages in the wiki
        pages = request.rootpage.getPageList(user='')
        pages.sort()

        sitemapfile = os.path.join(outputdir, 'sitemap.xml.gz')
        sitemap = gzip.GzipFile(sitemapfile, 'w')

        sitemap.write('<?xml version="1.0" encoding="%s"?>\n' % (config.charset,))
        sitemap.write('<urlset xmlns="http://www.google.com/schemas/sitemap/0.84">\n')
        for name in pages:
            if wikiutil.isSystemPage(request, name):
                continue
            sitemap.write('<url>\n')
            sitemap.write('<loc>%s</loc>\n' % (xml.sax.saxutils.escape(self.options.base_url+'/'+name.encode('utf-8')),))
            sitemap.write('<lastmod>%s</lastmod>\n' % (util.TranslateCDATA(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.strptime(Page(request,name).lastEditInfo()["time"], "%Y-%m-%d %H:%M:%S"))),))
            sitemap.write('</url>\n')
        sitemap.write('</urlset>\n')
        sitemap.close()

def createSiteMap():
    """
    Entry point when run from command line.
    """
    GoogleSitemap().run()
    
if __name__ == "__main__":
    createSiteMap()
