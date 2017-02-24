#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals
import platform

def is_windows():
    if platform.system() == 'Windows': return True
    else: return False

def system_path(path):
    """Return path with forward or backwards slashes as necessary based on OS"""
    if is_windows(): return path.replace('/', '\\')
    else: return path.replace('\\', '/')

########################### General Settings ###################################

AUTHOR = u'Zhoudshu'
SITENAME = u'Zhoudshu\'s Blog'
SITESUBTITLE = u"a personal blog which writes technology or life record."
SITEURL = 'https://zhouds.cn'
#SITEURL = 'http://zhoudshu.github.io'

PATH = 'content'
DELETE_OUTPUT_DIRECTORY = True

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh-cn'

USE_FOLDER_AS_CATEGORY = True
DEFAULT_DATE_FORMAT = '%a %d %B %Y'
DEFAULT_DATE = 'fs'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (
        ('GitHub', 'https://github.com'),
        ('Http2.0','https://http2.github.io/'),
        ('Nginx',  'http://nginx.org/'),
        ('NetMap', 'http://info.iet.unipi.it/~luigi/netmap/'),
        ('Python', 'http://python.org'),
         )

# Social widget

#('CSDN', 'http://blog.csdn.net/zhoudshu'),
SOCIAL = (('github', 'http://github.com/zhoudshu'),
         ('weibo', 'http://weibo.com/zhoudshu'),
         ('stack-overflow', 'http://stackoverflow.com/users/6472103/zhoudshu'),
         ('professional site', 'https://zhouds.cn'),
         )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

ARTICLE_URL = '{category}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{slug}/index.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
TAG_URL = 'tags/{slug}.html'
TAG_SAVE_AS = 'tags/{slug}.html'
TAGS_URL = 'tags.html'

# Generate archive
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'

################## Add custom css #########################
CUSTOM_CSS = 'static/custom.css'
STATIC_PATHS = ['images', 'extra/custom.css', 'extra/href_scroll.js', 'extra/jquery.zoom.js']
EXTRA_PATH_METADATA = {'extra/custom.css':{'path':'static/custom.css'},
                    'extra/href_scroll.js':{'path':'theme/js/href_scroll.js'},
                    'extra/jquery.zoom.js':{'path':'theme/js/jquery.zoom.js'},
                       }
for k in EXTRA_PATH_METADATA.keys(): # Fix backslash paths to resources if on Windows
    EXTRA_PATH_METADATA[system_path(k)] = EXTRA_PATH_METADATA.pop(k)


##################### Exterior Services ############################
DISQUS_SITENAME = u"zhoudshu"
DISQUS_SHORTNAME = 'zhoudshu'
DISQUS_DISPLAY_COUNTS = True

#DISQUS_DISPLAY_COUNTS = True

#GOOGLE_ANALYTICS = "UA-54524020-1"

#ADDTHIS_PROFILE = 'ra-5420884b27b877bf'
#ADDTHIS_DATA_TRACK_ADDRESSBAR = False


####################### Theme-Specific Settings #########################
THEME = 'pelican-bootstrap3'#'html5-dopetrope'

# Pelican Theme-Specific Variables
BOOTSTRAP_THEME = 'cosmo'#'sandstone'#'lumen'
SHOW_ARTICLE_CATEGORY = True

SITELOGO = 'images/logo.png'
SITELOGO_SIZE = 32
FAVICON = 'images/favicon.png'

ABOUT_ME = "I'm a programmer and engineer and family with Python,Java,C Language. Currently, I am learning Big Data technology.\
<p>Find out more about me at <strong><a href=\"https://zhouds.cn\" title=\"Professional Website\">zhouds.cn</a></strong></p>\
<p>You can also contact me <a href=\"mailto:zhoudshu@sohu.com\">here</a> </p>"

AVATAR = "/images/headshot.png"

BANNER = "/images/banner.png"

DISPLAY_ARTICLE_INFO_ON_INDEX = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
SHOW_ARTICLE_CATEGORY = True
TAG_CLOUD_MAX_ITEMS = 8

PYGMENTS_STYLE = 'monokai'

############################ Plugins ######################################
PLUGIN_PATHS = ['plugins']
PLUGINS = ['simple_footnotes', 'extract_toc', 'feed_summary', 'sitemap']

FEED_USE_SUMMARY = True
SUMMARY_MAX_LENGTH = 100

SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.7,
        "indexes": 0.5,
        "pages": 0.3,
    },
    "changefreqs": {
        "articles": "monthly",
        "indexes": "daily",
        "pages": "monthly",
    }
}

MD_EXTENSIONS = ['toc', 'fenced_code', 'codehilite(css_class=highlight)', 'extra']
#MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra']
