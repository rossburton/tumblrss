#! /usr/bin/env python

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

import datetime, sys, re, urllib, urllib2, cookielib
from BeautifulSoup import BeautifulSoup, SoupStrainer
from PyRSS2Gen import RSS2, RSSItem

def load_config():
    import ConfigParser, os

    config = ConfigParser.ConfigParser()
    # TODO: do xdg-dirs properly
    config.read(os.path.expanduser("~/.config/tumblrss"))

    if not config.has_section("Auth"):
        return None

    return {
        "email": config.get("Auth", "email"),
        "password": config.get("Auth", "password")
        }

def tumblrss(html):
    """
    Parse the HTML and return (list of RSSItem items, URL of next page).
    """

    soup = BeautifulSoup(html, parseOnlyThese=SoupStrainer(['li', 'a']))

    last_author = None
    items = []

    # TODO: make skipping your an option
    for post in soup.findAll(attrs={"class": re.compile("not_mine")}):
        n = post.find("div", "post_info")
        if n:
            author = n.a.string
            last_author = author
            n.extract()
        else:
            author = last_author
        
        # TODO: extract the source from quotes as title?
        n = post.find("div", "post_title")
        if n:
            if n.a:
                title = n.a.string.strip()
            else:
                title = n.string.strip()
            n.extract()
        else:
            n = post.find("td", "quote_source")
            if n:
                title = "".join(n.findAll(text=True)).strip()
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
    
    next_url = "http://tumblr.com" + soup.find("a", id="next_page_link")["href"]
    
    return (items, next_url)

if __name__ == "__main__":
    auth = load_config()
    if auth is None:
        print "Invalid configuration file, see the documentation"
        sys.exit(1)

    if len(sys.argv) > 1:
        html = open(sys.argv[1]).read()
        items = tumblrss(html)[0]
    else:
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        
        # Login
        opener.open("http://www.tumblr.com/login", urllib.urlencode(auth))

        url = "http://www.tumblr.com/dashboard"
        items = []
        
        # First page
        (i, url) = tumblrss(opener.open(url).read())
        items.extend(i)

        # Second page
        (i, url) = tumblrss(opener.open(url).read())
        items.extend(i)

        # Third page
        (i, url) = tumblrss(opener.open(url).read())
        items.extend(i)

    rss = RSS2(
        title = "Tumblr",
        description="My Tumblr contacts",
        link = "http://www.tumblr.com/dashboard",
        lastBuildDate = datetime.datetime.now(),
        items=items)
    
    rss.write_xml(open("tumblr.xml", "w"), encoding="UTF-8")
