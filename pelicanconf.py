#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from collections import OrderedDict

AUTHOR = u'woniu17'
AUTHOR_EMAIL = u'qinglucklin@foxmail.com'
SITENAME = u'woniu17, 我牛气'
SITEURL = 'http://linqingxiang.com'
DEFAULT_DATE_FORMATE = ('%Y-%m-%d')
DEFAULT_DATE = 'fs'  # use filesystem's mtime
LOCALE = ('zh_CN.utf8',)
DEFAULT_LANG = u'zh_CN'

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
         ('LIN Qingxiang', 'http://linqingxiang.com/'),
        )

# Social widget
SOCIAL = (
          ('github', 'https://github.com/woniu17'),
         )

THEME = 'pelican-themes/niu-x2-sidebar'
NIUX2_DEBUG = False

# niu-x2 theme config
FILENAME_METADATA = '(?P<slug>.*)'
GOOGLE_ANALYTICS = 'XXXXXX'
# feed config
FEED_DOMAIN = SITEURL
FEED_ALL_RSS = 'feed.xml'
FEED_MAX_ITEMS = 20
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
# use directory name as category if not set
USE_FOLDER_AS_CATEGORY = True
DELETE_OUTPUT_DIRECTORY = True
DEFAULT_CATEGORY = 'uncategorized'
DEFAULT_PAGINATION = 7

READERS = {
        'html': None,
}

STATIC_PATHS = [
        'static',
        'extra',
]
EXTRA_PATH_METADATA = {
    'extra/CNAME': { 'path': 'CNAME' },
    'extra/.nojekyll': { 'path': '.nojekyll' },
    'extra/README': { 'path': 'README.md' },
    'extra/favicon.ico': { 'path': 'favicon.ico' },
    'extra/LICENSE.txt': { 'path': 'LICENSE.txt' },
    'extra/robots.txt': { 'path': 'robots.txt' },
    'extra/BingSiteAuth.xml': {'path': 'BingSiteAuth.xml' },
}

ARTICLE_URL = '{category}/{slug}.html'
ARTICLE_SAVE_AS = ARTICLE_URL
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = PAGE_URL
CATEGORY_URL = '{slug}/index.html'
CATEGORY_SAVE_AS = CATEGORY_URL
TAG_URL = 'tag/{slug}.html'
TAG_SAVE_AS = TAG_URL
TAGS_SAVE_AS = 'tag/index.html'
# disable author pages
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''

JINJA_EXTENSIONS = ['jinja2.ext.ExprStmtExtension',]
NIUX2_AUTHOR_TRANSL = '作者'
NIUX2_404_TITLE_TRANSL = '404错误 页面未找到!'
NIUX2_404_INFO_TRANSL = '请求页面未找到!'
NIUX2_TAG_TRANSL = '标签'
NIUX2_ARCHIVE_TRANSL = '存档'
NIUX2_ARCHIVE_UPDATEDATE_TRANSL = '存档 (按修改时间)'
NIUX2_CATEGORY_TRANSL = '分类'
NIUX2_TAG_CLEAR_TRANSL = '清空'
NIUX2_TAG_FILTER_TRANSL = '过滤标签，不妨试试[0-9]{3}'
NIUX2_HEADER_TOC_TRANSL = '目录'
NIUX2_SEARCH_TRANSL = '搜索'
NIUX2_SEARCH_PLACEHOLDER_TRANSL = '按回车开始搜索 ...'
NIUX2_COMMENTS_TRANSL = '评论'
NIUX2_PUBLISHED_TRANSL = '发布时间'
NIUX2_LASTMOD_TRANSL = '最后修改'
NIUX2_PAGE_TITLE_TRANSL = '页面'
NIUX2_RECENT_UPDATE_TRANSL = '最近修改'
NIUX2_HIDE_SIDEBAR_TRANSL = '隐藏侧边栏'
NIUX2_SHOW_SIDEBAR_TRANSL = '显示侧边栏'
NIUX2_REVISION_HISTORY_TRANSL = '修订历史'
NIUX2_VIEW_SOURCE_TRANSL = '查看源文件'

NIUX2_DUOSHUO_SHORTNAME = 'xxxxxx'
#NIUX2_DUOSHUO_THREAD_KEY = 'slug'
#autumn, borland, bw, colorful, default,
#emacs, friendly, fruity, github, manni,
#monokai, murphy, native, pastie, perldoc,
#tango, trac, vim, vs, zenburn
NIUX2_PYGMENTS_THEME = 'github'
NIUX2_PAGINATOR_LENGTH = 11
NIUX2_RECENT_UPDATE_NUM = 10
NIUX2_FAVICON_URL = '/favicon.ico'
NIUX2_GOOGLE_CSE_ID = '000541811106443708772:dked6ziq4qq'
NIUX2_DISPLAY_TITLE = True
NIUX2_LAZY_LOAD = True
NIUX2_LAZY_LOAD_TEXT = 'orz 努力加载中'
NIUX2_LAZY_LOAD_ICON = 'icon-spin icon-spinner2'
NIUX2_TOOLBAR = True
NIUX2_TOOLBAR_LOAD_ICON = 'icon-spin icon-4x icon-spinner9'

#NIUX2_LIB_JQUERY = 'http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.11.0.min.js'
#NIUX2_LIB_BOOTSTRAP = 'https://maxcdn.bootstrapcdn.com/bootstrap/3.1.1/'

NIUX2_CATEGORY_MAP = {
    'code': ('代码', 'icon-code'),
    'collection': ('搜藏', 'icon-briefcase'),
    'essay': ('随笔', 'icon-leaf'),
    'life': ('日常', 'icon-coffee'),
    'note': ('笔记', 'icon-book'),
    'research': ('研究', 'icon-flask'),
}

NIUX2_HEADER_SECTIONS = [
    ('关于', 'about me', '/about.html', 'icon-anchor'),
    ('待办', 'TODO', '/todo.html', 'icon-rocket'),
    #('使用协议', 'agreement', '/agreement.html', 'icon-exclamation-circle'),
    #('项目', 'my projects', '/my_projects.html', 'icon-rocket'),
    ('标签', 'tags', '/tag/', 'icon-tag'),
]

TEMPLATE_PAGES = {
    '404.html' : '404.html',
    'archives_updatedate.html' : 'archives_updatedate.html',
}
NIUX2_HEADER_DROPDOWN_SECTIONS = OrderedDict()
NIUX2_HEADER_DROPDOWN_SECTIONS[('存档', 'icon-archive')] = [
    ('存档 (按发布时间)', 'archives order by publish time', '/archives.html', 'icon-calendar'),
    ('存档 (按修改时间)', 'archives order by modify time', '/archives_updatedate.html', 'icon-pencil'),
]

NIUX2_FOOTER_LINKS = [
    ('关于', 'about me', '/pages/about.html', ''),
    #('使用协议', 'terms, license and privacy etc.', '/agreement.html', ''),
    ('闽ICP备15002376号', '备案号', 'http://www.miitbeian.gov.cn/', ''),
]

NIUX2_FOOTER_ICONS = [
    #('icon-key', 'my public key', '/my_gnupg.html'),
    ('icon-envelope-o', 'my email address', 'mailto: qinglucklin@foxmail.com'),
    ('icon-github-alt', 'my github page', 'http://github.com/woniu17'),
    #('icon-rss', 'subscribe my blog', '/feed.xml'),
]

#plugin
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['latex', 'pelican-update-date']

#markdown
from markdown.extensions import codehilite
MD_EXTENSIONS = [
    #'codehilite(css_class=highlight)',
    codehilite.CodeHiliteExtension(configs=[('linenums', False), ('guess_lang', False)]),
    'extra',
    'tables',
]

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

