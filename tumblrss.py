#! /usr/bin/python

# Copyright (C) 2009 Ross Burton <ross@burtonini.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# St, Fifth Floor, Boston, MA 02110-1301 USA

import ConfigParser, datetime, os, sys, re, urllib, urllib2, cookielib
from BeautifulSoup import BeautifulSoup, SoupStrainer
from PyRSS2Gen import RSS2, RSSItem

config = ConfigParser.ConfigParser()
config.read(os.path.expanduser("~/.config/tumblrss"))

if not config.has_section("Auth"):
    print "Invalid configuration file"
    sys.exit(1)

auth = {
    "email": config.get("Auth", "email"),
    "password": config.get("Auth", "password")
    }

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

opener.open("http://www.tumblr.com/login", urllib.urlencode(auth))
page = opener.open("http://www.tumblr.com/dashboard").read()
soup = BeautifulSoup(page, parseOnlyThese=SoupStrainer('li'))

last_author = None
items = []

for post in soup.findAll(attrs={"class": re.compile("not_mine")}):
    n = post.find("div", "post_info")
    if n:
        author = n.a.string
        last_author = author
        n.extract()
    else:
        author = last_author
    

    n = post.find("div", "post_title")
    if n:
        title = n.a.string
        n.extract()
    else:
        title = ""

    url = post.find("a", attrs={"title": "Permalink"})["href"]

    post.find("div", "post_controls").extract()
    post.find("div", "so_ie_doesnt_treat_this_as_inline").extract()
    post.find("div", id=re.compile("notes_outer_container_")).extract()

    items.append(RSSItem(title=title,
                         author=author,
                         link=url,
                         guid=url,
                         description=str(post)))



rss = RSS2(
    title = "Tumblr",
    description="My Tumblr contacts",
    link = "http://www.tumblr.com/dashboard",
    lastBuildDate = datetime.datetime.now(),
    items=items)
rss.write_xml(open("tumblr.xml", "w"))
