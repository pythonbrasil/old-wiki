#
# vim:ts=4:sw=4:et

import urllib
import re
import random

def getbanner():
    banner = []
    banner.append('<a href="http://makezine.com/go/ugsub"><img src="http://makezine.com/images/ug/make_UG_468x60.gif" alt="Subscribe to MAKE and save!" width="468" height="60" border="0" /></a>')

    banner.append("""<script type="text/javascript"><!--
google_ad_client = "pub-6247019971210113";
google_alternate_color = "FFFFFF";
google_ad_width = 234;
google_ad_height = 60;
google_ad_format = "234x60_as";
google_ad_type = "text_image";
//2006-10-16: PythonBrasil
google_ad_channel = "1165095299";
google_color_border = "336699";
google_color_bg = "FFFFFF";
google_color_link = "0000FF";
google_color_text = "000000";
google_color_url = "008000";
//--></script>
<script type="text/javascript"
  src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>""")
    return u'<span class="ads">%s&nbsp;&nbsp;%s</span>' % tuple(banner[:2])
