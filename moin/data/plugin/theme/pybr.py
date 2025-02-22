# -*- coding: utf-8 -*-
"""
    MoinMoin - Python Brasil theme

    @copyright: 2003-2005 by Osvaldo Santana Neto
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.theme import ThemeBase
from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.action import get_available_actions

from MoinMoin import log
logging = log.getLogger(__name__)

class Theme(ThemeBase):
    name = "pybr"

    def headscript(self, d):
        return self.cfg.custom_html_head

    def get_partners(self):
        return u'  <span class="partners">\n    %s\n  </span>' % (u'\n    '.join(self.cfg.partners))

    def login(self, d):
        request = self.request
        _ = request.getText
        
        userlinks = [
            u'    <a href="/" title="Volta para a página inicial">',
            u'       <img src="%s" alt="Início" />' % (self.img_url("home.png")),
            u'    </a> Logado como ',
        ]

        if request.user.valid and request.user.name:
            interwiki = wikiutil.getInterwikiHomePage(request)
            name = request.user.name
            aliasname = request.user.aliasname
            if not aliasname:
                aliasname = name
            title = "%s @ %s" % (aliasname, interwiki[0])
            # link to (interwiki) user homepage
            homelink = (request.formatter.interwikilink(1, title=title, id="userhome", css_class="user_preference", generated=True, *interwiki) +
                        request.formatter.text(name) +
                        request.formatter.interwikilink(0, title=title, id="userhome", *interwiki))
            userlinks.append(homelink)        
            # link to userprefs action
            userlinks.append(" (")
            userlinks.append(d['page'].link_to(request, text=_('Preferences', formatted=False),
                                               querystr={'action': 'userprefs'}, css_class="user_preference"))
            userlinks.append(" / ")
           
        if request.cfg.show_login:
            if request.user.valid:
                userlinks.append(d['page'].link_to(request, text=_('Logout', formatted=False),
                                                   querystr={'action': 'logout', 'logout': 'logout'}, css_class="user_preference"))
            else:
                userlinks.append("(")
                userlinks.append(d['page'].link_to(request, text=_("Login", formatted=False),
                                                   querystr={'action': 'login'}, css_class="user_preference"))
        userlinks.append(")")

        html = u'<span class="login">%s</span>' % ''.join(userlinks)
        return html

    def logo(self, d):
        ret = [
            u'    <div id="logo" style="display:inline;">',
            u'      %s' % (wikiutil.link_tag(self.request, d['page_front_page'], self.cfg.logo_string)),
            u'    </div>',
        ]
        if self.cfg.logo_complement is not None:
            ret.append(self.cfg.logo_complement)

        return u'\n'.join(ret)

    def search(self):
        return u"""    <div id="search">
<!-- Google CSE Search Box Begins  -->
  <form id="searchbox_002985189122681080462:mbs3iwwbsrs" action="http://www.google.com/cse">
    <input type="hidden" name="cx" value="002985189122681080462:mbs3iwwbsrs" />
    <input type="hidden" name="cof" value="FORID:1" />
    <input name="q" type="text" size="20" />
    <input type="submit" name="sa" value="Search" />
  </form>
  <script type="text/javascript" src="http://www.google.com/coop/cse/brand?form=searchbox_002985189122681080462%3Ambs3iwwbsrs"></script>
<!-- Google CSE Search Box Ends -->
    </div>\n"""

    def get_optional_header(self):
        return u"""    <div id="optional_header">
      <table>
        <tbody><tr>
          <td>
            <a href="/ImpressioneSe"><strong>Impressione-se&nbsp;»</strong><br/>
            Python pode ser usada em diversos tipos de desenvolvimento.
          </a></td><td>
            <a href="/InicieSe"><strong>Inicie-se&nbsp;»</strong><br/>
            Python pode ser usada livremente por qualquer desenvolvedor.
          </a></td><td>
            <a href="/AprendaMais"><strong>Aprenda mais&nbsp;»</strong><br/>
            Python tem uma sintaxe muito simples e também é fácil de aprender.
          </a></td><td>
            <a href="/EnvolvaSe"><strong>Envolva-se&nbsp;»</strong><br/>
            Participe da comunidade brasileira de desenvolvedores Python.
          </a></td>
        </tr></tbody>
      </table>
    </div>\n"""

    def sidebar(self, d, **kw):
        page = d['page']
        if page.request.getPragma("ad", "yes").lower().startswith('y'):
            ad =  u'      <p class="ad">%s</p>' % (self.cfg.get_ad('sidebar'))
        else:
            ad = u''

        ret = [
            u'  <div id="sidebar">',
            u'      <p><a href="?action=edit" title="Editar esta página">',
            u'          <img src="%s" alt="Editar esta página" />' % (self.img_url("edit.png")),
            u'      </a></p>',
            u'      <h1>Veja também:</h1>',
            self.navibar(d),
            u'      <p><a href="/planet/" title="Planet PythonBrasil">Planet PythonBrasil</a></p>',
            u'      <p><a href="/Mais">Mais...</a></p>',
            ad,
            u'  </div>',
        ]
        return u'\n'.join(ret)

    def edit_sidebar(self, d, **kw):
        ret = [
            u'  <div id="sidebar">',
            u'      <h1>Veja também:</h1>',
            self.navibar(d),
            u'      <p><a href="/Mais">Mais...</a></p>',
            u'      <p class="ad">%s</p>' % (self.cfg.get_ad('sidebar')),
            u'  </div>',
        ]
        return u'\n'.join(ret)


    def navibar(self, d):
        request = self.request
        found = {} # pages we found. prevent duplicates
        items = [] # navibar items
        item = u'<li>%s</li>'
        current = d['page_name']

        # Process config navi_bar
        if request.cfg.navi_bar:
            for text in request.cfg.navi_bar:
                pagename, link = self.splitNavilink(text)
                if pagename == current:
                    cls = 'wikilink current'
                else:
                    cls = 'wikilink'
                items.append(item % (link))
                found[pagename] = 1

        # Add user links to wiki links, eliminating duplicates.
        userlinks = request.user.getQuickLinks()
        for text in userlinks:
            # Split text without localization, user knows what he wants
            pagename, link = self.splitNavilink(text, localize=0)
            if not pagename in found:
                if pagename == current:
                    cls = 'userlink current'
                else:
                    cls = 'userlink'
                items.append(item % (link))
                found[pagename] = 1

        # Add current page at end
        if not current in found:
            title = d['page'].split_title(request)
            title = self.shortenPagename(title)
            link = d['page'].link_to(request, title)
            items.append(item % (link))

        # Assemble html
        items = u''.join(items)
        html = u'''
<ul>
%s
</ul>
''' % items
        return html

    def title(self, d):
        _ = self.request.getText
        content = []
        if d['title_text'] == d['page'].split_title(): # just showing a page, no action
            curpage = ''
            segments = d['page_name'].split('/') # was: title_text
            for s in segments[:-1]:
                curpage += s
                content.append("<span>%s</span> / " % Page(self.request, curpage).link_to(self.request, s))
                curpage += '/'
            link_text = segments[-1]
            link_title = _('Click to do a full-text search for this title')
            link_query = {
                'action': 'fullsearch',
                'value': 'linkto:"%s"' % d['page_name'],
                'context': '180',
            }
            # we dont use d['title_link'] any more, but make it ourselves:
            link = d['page'].link_to(self.request, link_text, querystr=link_query, title=link_title, css_class='backlink', rel='nofollow')
            content.append(('<span>%s</span>') % link)
        else:
            content.append('<span>%s</span>' % wikiutil.escape(d['title_text']))

        html = '<h1 id="pagelocation">%s</h1>' % ("".join(content))
        logging.debug("AQUI!" + unicode(html))
        return html

    def header(self, d, **kw):
        if d['page_front_page'] == d['page_name']:
            opt_head = self.get_optional_header()
        else:
            opt_head = ""
        #opt_head = u"" # TODO: remove this line!!!
        try:
            title = self.title(d)
        except Exception, e:
            logging.debug("AQUI!" + str(e))
        html = [
            self.emit_custom_html(self.cfg.page_header1),
            u'<div id="head_bar">',
            self.get_partners(),
            self.login(d),
            u'</div>',
            u'<div id="core">',
            #self.search(),
	        self.searchform(d),
            self.logo(d),
            opt_head,
            self.sidebar(d, **kw),
            u'  <div id="page">',
            self.msg(d),
            self.title(d),
            u'<!-- INICIO -->',
        ]
        return u'\n'.join(html)

    def editorheader(self, d, **kw):
        html = [
            self.emit_custom_html(self.cfg.page_header1),
            u'<div id="head_bar">',
            self.get_partners(),
            self.login(d),
            u'</div>',
            u'<div id="core">',
            self.logo(d),
            self.edit_sidebar(d, **kw),
            u'  <div id="page">',
            self.msg(d),
            self.title(d),
            u'<!-- INICIO -->',
        ]
        return u'\n'.join(html)

    def foot_partners(self):
        return u'    <div class="partners"><p>\n      %s\n    </p></div>' % (u'\n      '.join(self.cfg.hosting_partners))

    def actionsMenu(self, page):
        request = self.request
        _ = request.getText
        
        menu = [
            'raw',
            'print',
            'info',
            'RenamePage',
            'DeletePage',
            'SubscribeUser',
            'AttachFile',
        ]

        titles = {
            'raw': _('Raw Text', formatted=False),
            'print': _('Print View', formatted=False),
            'info': _('Information', formatted=False),
            'RenamePage': _('Rename Page', formatted=False),
            'DeletePage': _('Delete Page', formatted=False),
            'SubscribeUser': _('Subscribe User', formatted=False),
            'AttachFile': _('Attachments', formatted=False),
            }

        options = []
        option = u'<a href="?action=%(action)s">%(title)s</a>'
	available = get_available_actions(request.cfg, page, request.user)

        #available = request.getAvailableActions(page)
        for action in menu:
            data = {'action': action, 'title': titles[action]}
	
            if action[0].isupper() and not action in available:
                continue
	
            options.append(option % (data))

        more = [item for item in available if not item in titles and not item in ('AttachFile',)]
        more.sort()

        """
        if more:
            separator = {'action': 'show', 'disabled': disabled, 'title': titles['__separator__']}
            options.append(separator)
            for action in more:
                data = {'action': action, 'disabled': ''}
                title = Page(request, action).split_title(request, force=1)
                data['title'] = _(title, formatted=False)
                options.append(data)
        """

        return u'<p>%s</p>' % (u' | '.join(options))
 
    def copyright(self, pafe):
        return u"<p>%s</p>" % ('</p>\n<p>'.join(self.request.cfg.copyright))

    def footer(self, d, **keywords):
        page = d['page']
        html = [
            u'<!-- FIM -->',
            u'  </div> <!-- page -->',
            u'</div> <!-- core -->',
            u'<div id="footer">',
            self.foot_partners(),
            u'<div class="information">',
            u'    <p><span style="font-weight: bold;">Sobre esta página</span></p>',
            self.pageinfo(page),
            self.actionsMenu(page),
            self.copyright(page),
            u'</div> <!-- information -->',
            u'</div> <!-- footer -->\n',
        ]

        return u'\n'.join(html)

def execute(request):
    return Theme(request)


# vim:bg=dark:ts=4:sw=4:et:showmatch:ai:si
