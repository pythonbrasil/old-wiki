# Import a RSS Feed into MoinMoin
# Ian Wienand <ianw@ieee.org>
# (C) 2006 - Public Domain

# Using this macro
# [[RSSReader(url[,allow_html])]]
# where
# * url is the url of the RSS/ATOM feed to read
# * allow_html is an optional argument if you trust the feed to put
#   the HTML directly into the page

# CAUTION: this could be an attack vector, although feedparser should
# strip most "bad" HTML.

# this tells MoinMoin not to cache the page, as we don't know when it
# changes.
Dependencies = ["time"]

from MoinMoin import util, wikiutil, config
from MoinMoin.Page import Page

class RSStoWiki:
    def __init__(self, macro, title, url, allow_html, max):
        self.macro = macro
        self.fmt = macro.formatter
        self.allow_html = allow_html
        self.max = max
        self.title = title
        # in debian package python-feedparser
        import feedparser
        self.f = feedparser.parse(url)
        self.result = []
        if self.f.feed == {}:
            self.result.append (self.fmt.icon('info') + \
                                self.fmt.strong(1) + \
                                self.fmt.text(' Unable to retreive feed %s' % url) + \
                                self.fmt.strong(0))
            self.valid = False
        else:
            self.valid = True
                          

    def get_title(self):
        self.result.append(self.fmt.heading(on=1, depth=2) + \
                           self.fmt.text(self.title) + \
                           self.fmt.heading(on=0, depth=2))

    def get_subtitle(self):
        if not self.f.feed.has_key('subtitle'):
            return
        self.result.append(self.fmt.heading(on=1, depth=2) + \
                           self.fmt.text(self.f.feed.subtitle) + \
                           self.fmt.heading(on=0, depth=2))

    def get_paragraph(self, text):
        self.result.append(self.fmt.paragraph(on=1) + \
                           self.fmt.text(text) + \
                           self.fmt.paragraph(on=0))

    def get_link(self, link):
        self.result.append(self.fmt.url(on=1, href=link) + \
                           self.fmt.icon('www') + \
                           self.fmt.text(" "+link) + \
                           self.fmt.url(on=0))
        
    def get_feedlink(self):
        if not self.f.feed.has_key('link'):
            return
        self.get_link(self.f.feed.link)

    def get_description(self):
        if not self.f.feed.has_key('description'):
            return
        self.get_paragraph(self.f.feed.description)

    def get_rule(self):
        self.result.append(self.fmt.rule(size=1))

    def get_entry_header(self, title):
        self.result.append(self.fmt.listitem(on=1) + \
                           self.fmt.text(title) + \
                           self.fmt.listitem(on=0))

    def get_entry_body(self, body):
        self.result.append(self.fmt.paragraph(on=1))
        if (self.allow_html):
            self.result.append(self.fmt.rawHTML(body))
        else:
            self.result.append(self.fmt.text(body))
        self.result.append(self.fmt.paragraph(on=0))

    def get_entries(self):
        for i, entry in enumerate(self.f.entries):
            if self.max != 0 and i > self.max:
                break
            if 'title' in entry:
                if 'link' in entry:
                    self.result.append(self.fmt.url(on=1, href=entry.link))
                self.get_entry_header(entry.title)
                if 'link' in entry:
                    self.result.append(self.fmt.url(on=0))
            #if entry.has_key('updated'):
            #    self.get_paragraph(entry.updated)
            #if entry.has_key('description'):
            #    self.get_entry_body(entry.description)
            #if entry.has_key('link'):
            #    self.get_link(entry.link)

    def get_output(self):
        if self.valid:
            self.get_title()
            #self.get_subtitle()
            #self.get_description()
            #self.get_feedlink()
            #self.get_rule()
            self.result.append(self.fmt.bullet_list(on=1))
            self.get_entries()
            self.result.append(self.fmt.bullet_list(on=0))
            #self.get_rule()
        return ''.join(self.result)

def execute(macro, args):
    macro_args = args.split(",")
    allow_html = "allow_html" in macro_args
    try:
        max = int(macro_args[-1])
    except:
        max = 0

    rss = RSStoWiki(macro, macro_args[0], macro_args[1], allow_html, max)
    return rss.get_output()

# vim:ts=4:sw=4:et:sm
