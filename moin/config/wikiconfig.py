# -*- coding: iso-8859-1 -*-
# IMPORTANT! This encoding (charset) setting MUST be correct! If you live in a
# western country and you don't know that you use utf-8, you probably want to
# use iso-8859-1 (or some other iso charset). If you use utf-8 (a Unicode
# encoding) you MUST use: coding: utf-8
# That setting must match the encoding your editor uses when you modify the
# settings below. If it does not, special non-ASCII chars will be wrong.

"""
    MoinMoin - Configuration for a single wiki

    If you run a single wiki only, you can omit the farmconfig.py config
    file and just use wikiconfig.py - it will be used for every request
    we get in that case.

    Note that there are more config options than you'll find in
    the version of this file that is installed by default; see
    the module MoinMoin.config.multiconfig for a full list of names and their
    default values.

    Also, the URL http://moinmo.in/HelpOnConfiguration has
    a list of config options.

    ** Please do not use this file for a wiki farm. Use the sample file
    from the wikifarm directory instead! **
"""

from MoinMoin.config.multiconfig import DefaultConfig

class Config(DefaultConfig):

    # Wiki identity ----------------------------------------------------
    #show_timings = True
    # Site name, used by default for wiki name-logo [Unicode]
    sitename = u'PythonBrasil'

    # Wiki logo. You can use an image, text or both. [Unicode]
    # For no logo or text, use '' - the default is to show the sitename.
    # See also url_prefix setting below!
    logo_string = """<img src="/pybr/img/pythonbrasil_logo.png" title="PythonBrasil" alt="PythonBrasil" />"""
    logo_complement = ""
    logo_complement_old = """
    <div style="text-align:center">
    <a href="http://www.pythonbrasil.org.br/2011/inscricoes"
       target="_blank"
       title="Envolva-se! Participe da PythonBrasil [7] - palestrantes internacionas!"
       alt="Envolva-se! Participe da PythonBrasil [7] - palestrantes internacionas!">
      <img src="/banners-pythonbrasil/pythonbrasil7-fullbanner.gif"
           title="Envolva-se! Participe da PythonBrasil [7] - palestrantes internacionas!"
	   alt="Envolva-se! Participe da PythonBrasil [7] - palestrantes internacionas!"/>
    </a>
    </div>
    """

    # name of entry page / front page [Unicode], choose one of those:

    # a) if most wiki content is in a single language
    page_front_page = u"PythonBrasil"

    # b) if wiki content is maintained in many languages
    # page_front_page = u"FrontPage"

    # The interwiki name used in interwiki links
    interwikiname = u'pythonbr'
    # Show the interwiki name (and link it to page_front_page) in the Theme,
    # nice for farm setups or when your logo does not show the wiki's name.
    #show_interwiki = 1

    xapian_search = True
    xapian_stemming = True

    # Critical setup  ---------------------------------------------------

    # Misconfiguration here will render your wiki unusable. Check that
    # all directories are accessible by the web server or moin server.

    # If you encounter problems, try to set data_dir and data_underlay_dir
    # to absolute paths.

    moinmoin_dir = '/var/www/.virtualenvs/wiki.python.org.br/lib/python2.7/site-packages/MoinMoin'

    # Where your mutable wiki pages are. You want to make regular
    # backups of this directory.
    data_dir = '/srv/wiki.python.org.br/www/moin/data'

    # Where read-only system and help page are. You might want to share
    # this directory between several wikis. When you update MoinMoin,
    # you can safely replace the underlay directory with a new one. This
    # directory is part of MoinMoin distribution, you don't have to
    # backup it.
    data_underlay_dir = '/srv/wiki.python.org.br/www/moin/underlay'

    # The URL prefix we use to access the static stuff (img, css, js).
    # NOT touching this is maybe the best way to handle this setting as moin
    # uses a good internal default (something like '/moin_static180' for moin
    # version 1.8.0).
    # For Twisted and standalone server, the default will automatically work.
    # For others, you should make a matching server config (e.g. an Apache
    # Alias definition pointing to the directory with the static stuff).
    url_prefix_static = '/static'


    # Security ----------------------------------------------------------

    # This is checked by some rather critical and potentially harmful actions,
    # like despam or PackageInstaller action:
    superuser = [u"OsvaldoSantanaNeto", u"RudaPorto", u"EricoAndrei", u"avelino",u"TaniaAndrea", u"humrochagf"]

    # IMPORTANT: grant yourself admin rights! replace YourName with
    # your user name. See HelpOnAccessControlLists for more help.
    # All acl_rights_xxx options must use unicode [Unicode]
    acl_rights_default = u"Known:read,write All:read +AdminGroup:read,write,revert,delete,admin"
    acl_rights_before = u"+AdminGroup:read,write,revert,delete,admin RudaPorto:read,write,revert,delete,admin NiloMenezes:read,write,revert,delete,admin ViniciusAssef:read,write,revert,delete,admin OsvaldoSantanaNeto:read,write,revert,delete,admin erichideki:read,write,revert,delete,admin TaniaAndrea:read,write,revert,delete,admin"
    actions_excluded = ['xmlrpc', 'moinexec', 'twikidraw', 'anywikidraw']

    # The default (ENABLED) password_checker will keep users from choosing too
    # short or too easy passwords. If you don't like this and your site has
    # rather low security requirements, feel free to DISABLE the checker by:
    #password_checker = None # None means "don't do any password strength checks"

    # Link spam protection for public wikis (Uncomment to enable)
    # Needs a reliable internet connection.

    from MoinMoin.security.antispam import SecurityPolicy


    #textchas_disabled_group = u"AdminGroup" # members of this don't get textchas
    textchas = {
        'en': { # silly english example textchas (do not use them!)
            u"Enter the first 3 digits of Pi.": ur"3\.14",
            u"What is the opposite of 'day'?": ur"(night|nite)",
            # ...
        },
        'de': { # some german textchas
            u"Gib die ersten 9 Stellen von Pi ein.": ur"3\.14",
            u"Was ist das Gegenteil von 'Tag'?": ur"nacht",
            # ...
        },
        'pt-br': { # some german textchas
            u"Informe os tr\xeas primeiros d\xedgitos do n\xfamero Pi (apenas n\xfameros)": ur"314",
            u"Qual o oposto de 'dia'?": ur"noite",
	    u"Quantas copas do mundo o Brasil venceu? (por extenso)": ur"cinco",
            u"Quantas edi\xe7\xf5es do evento PythonBrasil j\xe1 foram realizados? (por extenso)": ur"dez",
            # ...
        },
 
        # you can add more languages if you like
    }
    # Forca o uso do editor texto
    # Solucao do bug com browsers baseados no webkit e que usam o editor grafico
    # Discutido na issue 21 no github
    # Modificado por Nilo Menezes - em 09-02-2013  
    editor_default = 'text'
    editor_force = True

    # Mail --------------------------------------------------------------

    # Configure to enable subscribing to pages (disabled by default)
    # or sending forgotten passwords.
    # Usando gmail
    # Modificado por Humberto Rocha - em 21-07-2015

    # SMTP server, e.g. "mail.provider.com" (None to disable mail)
    mail_smarthost = "smtp.gmail.com:587"

    # The return address, e.g u"Jrgen Wiki <noreply@mywiki.org>" [Unicode]
    mail_from = u"Python Brasil Wiki <wiki@python.org.br>"

    # "user pwd" if you need to use SMTP AUTH
    mail_login = "webmaster@python.org.br sfr47ujhg" # "site@pythonbrasil.com.br $1t3$123"


    # User interface ----------------------------------------------------

    partners = [
        u'<a href="http://associacao.python.org.br" title="Associa&ccedil;&atilde;o Python Brasil">associa&ccedil;&atilde;o</a>',
        u'<a href="http://2015.pythonbrasil.org.br" title="Confer&ecirc;ncia PythonBrasil[11]">pythonbrasil[11]</a>',
        u'<a href="http://www.djangobrasil.org" title="Django Brasil">django</a>',
        u'<a href="http://www.plone.org.br" title="Plone Brasil">zope/plone</a>',
        u'<a href="/planet/" title="Planet PythonBrasil">planet</a>',
    ]

    hosting_partners = [
        #u'<a href="http://www.simplesconsultoria.com.br"><img src="/pybr/img/simples.png" alt="Simples Consultoria" /></a>',
	u'<a href="http://moinmo.in/"><img src="/pybr/img/logo_moin.png" alt="Powered by MoinMoin" /></a>',
        u'<a rel="license" href="https://creativecommons.org/licenses/by/2.5/br/"><img alt="Creative Commons License" style="border-width:0" src="https://creativecommons.org/images/public/somerights20.png" /></a>',
    ]


    # Add your wikis important pages at the end. It is not recommended to
    # remove the default links.  Leave room for user links - don't use
    # more than 6 short items.
    # You MUST use Unicode strings here, but you need not use localized
    # page names for system and help pages, those will be used automatically
    # according to the user selected language. [Unicode]
    navi_bar = [
        # Will use page_front_page, (default FrontPage)
        u'%(page_front_page)s',
        u'RecentChanges',
        u'TitleIndex',
        u'DocumentacaoPython',
        u'CookBook',
        u'OutrasSecoes',
    ]


    # The default theme anonymous or new users get
    theme_default = 'pybr'
    theme_force = True
    show_login = True

    # Language options --------------------------------------------------

    # See http://moinmo.in/ConfigMarket for configuration in
    # YOUR language that other people contributed.

    # The main wiki language, set the direction of the wiki pages
    language_default = 'pt-br'
    language_ignore_browser = True

    # the following regexes should match the complete name when used in free text
    # the group 'all' shall match all, while the group 'key' shall match the key only
    # e.g. CategoryFoo -> group 'all' ==  CategoryFoo, group 'key' == Foo
    # moin's code will add ^ / $ at beginning / end when needed
    # You must use Unicode strings here [Unicode]
    page_category_regex = ur'(?P<all>Categoria(?P<key>(?!Template)\S+))'
    page_template_regex = ur'(?P<all>TemplateDe(?P<key>\S+))'
    page_dict_regex = ur'(?P<all>Dic(?P<key>\S+))'
    page_group_regex = ur'(?P<all>Grupo(?P<key>\S+))'
    
    # Content options ---------------------------------------------------

    # Show users hostnames in RecentChanges
    show_hosts = 1

    # Enumerate headlines?
    show_section_numbers = 0

    # Enable graphical charts, requires gdchart.
    chart_options = {'width': 600, 'height': 300}

    surge_action_limits = None # disable surge protection
    umask = 0777
    trail_size = 0
    check_i18n = True
    bang_meta = True
    allow_doubleclick = False
    nonexist_qm = False
    backtick_meta = True
    allow_extended_names = True
    #custom_html_head = u'''  <meta name="robots" content="index,follow">
  #<meta name="verify-v1" content="t1sDnHnrdfaAYQAqBnYdtxtlouWtKKqzBHG1MMVkRRs=" />
#<!--  <script src="http://www.google-analytics.com/urchin.js" type="text/javascript"></script>
#  <script type="text/javascript"> _uacct = "UA-184296-1"; urchinTracker(); </script> -->
#  <!--[if lt IE 7]>
#  <script defer type="text/javascript" src="/pybr/js/pngfix.js"></script>
#  <![endif]-->\n'''

    #Google Analytics
    custom_html_head = u"""<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-136790801-2"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-136790801-2');
</script>
    """

    copyright = [
        u'&nbsp;',
        u'''"Python" e os logos de Python s&atilde;o marcas registradas da
        <a href="http://www.python.org/psf">Python Software Foundation</a>, usadas aqui mediante permiss&atilde;o da mesma. O conte&uacute;do deste site est&aacute; dispon&iacute;vel sob os termos da <a href="http://creativecommons.org/licenses/by/2.5/br/">Creative Commons Attribution 2.5</a> exceto quando explicitamente especificado outra licen&ccedil;a.''',]

    def get_ad(self, adtype):
        return u''

        return u'''<a href="http://www.pythonbrasil.org.br/" title="PythonBrasil[9]"><img src="http://2013.pythonbrasil.org.br/divulgue/no-seu-site/pythonbrasil9_pt_BR_rectangle.gif" alt="PythonBrasil[9]" /> </a>'''

        return u"""<script type="text/javascript"><!--
            google_ad_client = "pub-6247019971210113";
            google_ad_width = 160;
            google_ad_height = 600;
            google_ad_format = "160x600_as";
            google_ad_type = "text_image";
            //2007-01-02: PythonBrasil, Pythonbrasil Sidebar
            google_ad_channel = "1165095299+7737869662";
            google_color_border = "FFFFFF";
            google_color_bg = "FFFFFF";
            google_color_link = "303030";
            google_color_text = "303030";
            google_color_url = "0000FF";
            //--></script>
            <script type="text/javascript"
              src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
              </script>"""

# vim:ts=4:sw=4:et:si:ai:sm:bg=dark
