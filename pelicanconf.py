#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'qingluck'
AUTHOR_EMAIL = u'qinglucklin@foxmail.com'
SITENAME = u'qingtech'
SITEURL = 'http://woniu17.github.io'
DEFAULT_DATE_FORMATE = ('%Y-%m-%d')

PATH = 'content'

#TIMEZONE = 'Europe/Paris'
TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
         ('LIN Qingxiang', 'http://www.linqingxiang.com/'),
        )

# Social widget
SOCIAL = (
          ('github', 'https://github.com/woniu17'),
         )

THEME = 'pelican-themes/simple-bootstrap'
DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
