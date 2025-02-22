# -*- coding: iso-8859-1 -*-
u"""
    MoinMoin - RSSREader macro Version 2.1
               Output an RSS/ATOM Feed
               http://moinmo.in/MacroMarket/RSSReader

    @copyright: 2006 by Ian Wienand <ianw@ieee.org>
                2010 by Marcel Häfner http://moinmo.in/MarcelH%C3%A4fner
    @license:   Public Doman / GNU GPL

    Version:
     * 1.0 default Version from Ian Wienand
     * 2.0 first version from Marcel Häfner
     * 2.1 Bugfix
     * 2.2 Updates from Matthijs Kooijman

    Examples:
    * <<RSSReader("http://www.example.dot/feed.rss")>>
    * <<RSSReader(feed="http://www.example.dot/feed.rss", maxEntries=30, allowHtml=False,includeStyle=True)>>

    Description:
    <<RSSReader(url, maxEntries, allowHtml, includeStyle, dateFormat, linkEntries>>
     * url is the url of the RSS/ATOM feed to read, it's the only MUST field
     * maxEntries define how many items the entire feed should display. Default is 30.
     * allowHtml is an optional argument if you trust the feed to put the HTML
       directly into the page. CAUTION: this could be an attack vector,
       although feedparser should strip most "bad" HTML. Default ist False
     * includeStyle per default True, so a nice css is added before the maco,
       normaly you may say false and but in your own e.g. common.css some style
       definition.
     * dateFormat is a date format to use for the last updated /
       published date and time of the entry. This format must be in strftime
       format (see http://docs.python.org/2/library/time.html#time.strftime).
       By default, whatever format is used in the feed is displayed as-is.
     * linkEntries indicates whether the title of a post should be a
       link to the actual post (as indicated by the "link" field for the
       entry in the feed). Defaults to True.
"""

#do not chache the macro, so you receive updates without clearing the cache of the page.
#or if you like caching, add this: Dependencies = []
Dependencies = ["time"]


class RSStoWiki:
    def __init__(self, macro, url, maxEntries, allowHtml, includeStyle, dateFormat, linkEntries):

        #initial stuff for the whole class
        import feedparser
        self.f = feedparser.parse(url)
        self.macro = macro
        self.fmt = macro.formatter
        self.allowHtml = allowHtml
        self.includeStyle = includeStyle
        self.maxEntries = maxEntries
        self.dateFormat = dateFormat
        self.linkEntries = linkEntries
        self.request = macro.request
        self._ = self.request.getText
        self.result = []

        #check if feed exist or display an error message
        if self.f.feed == {}:
            self.result.append(self.fmt.div(True, css_class="error rssError") + \
                                self.fmt.icon('info') + \
                                self.fmt.text(" ") + \
                                self.fmt.strong(True) + \
                                self.fmt.text(self._('Unable to retreive feed')) + \
                                self.fmt.strong(False) + \
                                self.fmt.text(' "%s"' % url) + \
                                self.fmt.div(False))
            self.valid = False
        else:
            self.valid = True

    #generate content for the main (header) feed
    def get_title(self):
        if 'title' not in self.f.feed:
            return
        self.result.append(self.fmt.heading(True, depth=1, css_class="rssTitle") + \
                           self.fmt.text(self.f.feed.title) + \
                           self.fmt.heading(False, depth=1))

    def get_subtitle(self):
        if 'subtitle' not in self.f.feed:
            return
        self.result.append(self.fmt.paragraph(True, css_class="rssSubTitle") + \
                           self.fmt.text(self.f.feed.subtitle) + \
                           self.fmt.paragraph(False))

    def get_description(self):
        if 'description' not in self.f.feed:
            return
        #only desiplay description if its different compare to subtitel, mostly not
        if ('subtitle' in self.f.feed) and ('description' in self.f.feed):
            if self.f.feed.subtitle == self.f.feed.description:
                return
        self.result.append(self.fmt.paragraph(True, css_class="rssDescription") + \
                           self.fmt.text(self.f.feed.description) + \
                           self.fmt.paragraph(False))

    def get_feedlink(self):
        if 'link' not in self.f.feed:
            return
        self.get_link(self.f.feed.link)

    #generate content for a single feed item (entries)
    def get_entries(self):
        import time
        entriesCount = 0
        for entry in self.f.entries:
            # count and check maxEntries
            entriesCount = entriesCount + 1
            if entriesCount > self.maxEntries:
                break
            # start with generating the entry (title, link, update, description, ..)
            self.result.append(self.fmt.div(True, css_class="rssEntry"))
            if 'title' in entry:
                if self.linkEntries and 'link' in entry:
                    self.get_entry_header(entry.title, entry.link)
                else:
                    self.get_entry_header(entry.title)
            #if self.dateFormat and 'updated_parsed' in entry:
            #    self.result.append(self.fmt.paragraph(True, css_class="rssEntryUpdated") + \
            #                       self.fmt.text(time.strftime(self.dateFormat, entry.updated_parsed)) + \
            #                       self.fmt.paragraph(False))
            #elif 'updated' in entry:
            #    self.result.append(self.fmt.paragraph(True, css_class="rssEntryUpdated") + \
            #                       self.fmt.text(entry.updated) + \
            #                       self.fmt.paragraph(False))
            #if 'description' in entry:
            #    self.get_entry_body(entry.description)
            #if ('link' in entry) and 'title' not in entry:
            #    self.get_link(entry.link)
            self.result.append(self.fmt.div(False))

    #helper functions
    def get_paragraph(self, text):
        self.result.append(self.fmt.paragraph(True) + \
                           self.fmt.text(text) + \
                           self.fmt.paragraph(False))

    def get_link(self, link):
        self.result.append(self.fmt.url(True, href=link) + \
                           self.fmt.text(" ") + \
                           self.fmt.icon('www') + \
                           self.fmt.text(" " + link) + \
                           self.fmt.url(False))

    #helper function for the entry / item
    def get_entry_header(self, title, link=None):
        if link:  # if link exist, make the entry title with a link
            self.result.append(self.fmt.listitem(True, css_class="rssEntryTitle") + \
                               self.fmt.url(True, href=link) + \
                               self.fmt.text(title) + \
                               self.fmt.url(False) + \
                               self.fmt.listitem(False))
        else:
            self.result.append(self.fmt.paragraph(True, css_class="rssEntryTitle") + \
                               self.fmt.text(title) + \
                               self.fmt.paragraph(False))

    def get_entry_body(self, body):
        self.result.append(self.fmt.paragraph(True, css_class="rssEntryBody"))
        if (self.allowHtml):  # check if html is allow, for raw html output
            self.result.append(self.fmt.rawHTML(body))
        else:
            self.result.append(self.fmt.text(body))
        self.result.append(self.fmt.paragraph(False))

    def get_css(self):
        if not self.includeStyle:
            return
        self.result.append(self.fmt.rawHTML("""
<style type="text/css" media="all">
    /* macro RSSReader start*/
    div.rssReader .rssHeader {
        margin-top: 1em;
        margin-bottom: 1em;
        border-bottom: 1px dotted gray;
    }
    div.rssReader .rssSubTitle, div.rssReader .rssDescription {
        font-size: bold;
    }
    div.rssReader div.rssEntries {
        margin-top: 1em;
        margin-bottom: 1em;
        border-bottom: 1px dotted gray;
    }
    div.rssReader div.rssEntry {
        margin-top: 1em;
        margin-bottom: 1em;
    }
    div.rssReader p.rssEntryTitle {
        font-weight: bold;
        margin: 0em;
    }
    div.rssReader p.rssEntryUpdated {
        color: gray;
        font-size: 0.75em;
        margin: 0em;
    }
    div.rssReader p.rssEntryBody {
        margin: 0em;
        padding-top: 1em;
    }
    /* macro RSSReader end*/
</style>
        """))

    #output content
    def get_output(self):
        if self.valid:
            #start
            self.result.append(self.fmt.div(True, css_class="rssReader"))
            self.get_css()
            #header
            self.result.append(self.fmt.div(True, css_class="rssHeader"))
            self.get_title()
            #self.get_subtitle()
            #self.get_description()
            #self.result.append(self.fmt.linebreak(False))
            #self.get_feedlink()
            #self.result.append(self.fmt.div(False))
            #entries
            self.result.append(self.fmt.div(True, css_class="rssEntries"))
	    self.get_entries()
            self.result.append(self.fmt.div(False))
            #end
            self.result.append(self.fmt.div(False))
        return ''.join(self.result)


def macro_RSSReader(macro, feed, maxEntries=30, allowHtml=False, includeStyle=True, dateFormat=None, linkEntries=True):
    rss = RSStoWiki(macro, feed, maxEntries, allowHtml, includeStyle, dateFormat, linkEntries)
    return rss.get_output()

